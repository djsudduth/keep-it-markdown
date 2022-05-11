from dataclasses import dataclass
import os
import gkeepapi
import keyring
import getpass
import requests
import imghdr
import shutil
import re
import configparser
import click
from os.path import join
from pathlib import Path
from datetime import datetime
from collections import namedtuple

KEEP_CACHE = 'kdata.json'
KEEP_KEYRING_ID = 'google-keep-token'
KEEP_NOTE_URL = "https://keep.google.com/#NOTE/"
CONFIG_FILE = "settings.cfg"
DEFAULT_SECTION = "SETTINGS"
USERID_EMPTY = 'add your google account name here'
OUTPUTPATH = 'mdfiles'
MEDIADEFAULTPATH = "media"
MAX_FILENAME_LENGTH = 99

TECH_ERR = " Technical Error Message: "

CONFIG_FILE_MESSAGE = ("Your " + CONFIG_FILE + " file contains to the following [" 
                        + DEFAULT_SECTION + "] values. Be sure to edit it with "
                        " your information.")
MALFORMED_CONFIG_FILE = ("The " + CONFIG_FILE + " default settings file exists "
                        "but has a malformed header - header should be [SETTINGS]")
UNKNOWNN_CONFIG_FILE = ("There is an unknown configuration file issue - " 
                        + CONFIG_FILE + " or file system may be locked or "
                        "corrupted. Try deleting the file and recreating it.")
MISSING_CONFIG_FILE = ("The configuration file - " + CONFIG_FILE + " is missing. "
                        "Please check the documention on recreating it")
BADFILE_CONFIG_FILE = ("Unable to create " + CONFIG_FILE + ". "
                        "The file system issue such as locked or corrupted")
KEYERR_CONFIG_FILE = ("Configuration key in " + CONFIG_FILE + " not found. "
                        "Key passed is: ")


ILLEGAL_FILE_CHARS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '&', '\n', '\r', '\t']
ILLEGAL_TAG_CHARS = ['~', '`', '!', '@', '$', '%', '^', '(', ')', '+', '=', '{', '}', '[', ']', '<', '>', ';', ':', ',', '.', '"', '/', '\\', '|', '?', '*', '&', '\n', '\r']

default_settings = {
    'google_userid': USERID_EMPTY,
    'output_path': OUTPUTPATH,
    'media_path': MEDIADEFAULTPATH,
}

media_downloaded = False

name_list = []
keep_name_list = []
notes = []


class ConfigurationException(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class Config:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
            cls.instance._config = configparser.ConfigParser()
            cls.instance._configdict = {}
            cls.instance.__read()
            cls.instance.__load()
        return cls.instance

    def __read(self):
        try:
            self._cfile = self._config.read(CONFIG_FILE)
            if not self._cfile:
                self.__create()
        except configparser.MissingSectionHeaderError:
            raise ConfigurationException(MALFORMED_CONFIG_FILE)
        except Exception:
            raise ConfigurationException(UNKNOWNN_CONFIG_FILE)
    
    def __create(self):
        self._config[DEFAULT_SECTION] = default_settings
        try:
            with open(CONFIG_FILE, 'w') as configfile:
                self._config.write(configfile)
        except Exception as e:
            raise ConfigurationException(BADFILE_CONFIG_FILE)

    def __load(self):
        options = self._config.options(DEFAULT_SECTION)
        for option in options:
            self._configdict[option] = \
                self._config.get(DEFAULT_SECTION, option)

    def get(self, key):
        try:
            return(self._configdict[key])
        except Exception as e:
            raise ConfigurationException(KEYERR_CONFIG_FILE + key)



class Markdown:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Markdown, cls).__new__(cls)
        return cls.instance

    #Note that the use of temporary %%% is because notes 
    #   can have the same URL repeated and replace would fail

    def convert_urls(self, text):
        # pylint: disable=anomalous-backslash-in-string
        urls = re.findall(
            "http[s]?://(?:[a-zA-Z]|[0-9]|[~#$-_@.&+]"
                "|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            text
        )

        for url in urls:
            text = text.replace(url, 
                "[" + url[:1] + "%%%" + url[2:] + 
                "](" + url[:1] + "%%%" + url[2:] + ")", 1)

        return text.replace("h%%%tp", "http")


    def format_checkboxes(self, text):
        md_text = text.replace(u"\u2610", '- [ ]') \
            .replace(u"\u2611", ' - [x]')
        return md_text

    #this feels more like a file utility than a markdown utility
    def format_title(self, title):
        title = re.sub(
            '[' + re.escape(''.join(ILLEGAL_FILE_CHARS)) + ']', 
            ' ', 
            title[0:MAX_FILENAME_LENGTH]
        ) 
        return title


def keep_init():
    keepapi = gkeepapi.Keep()
    return keepapi


def keep_token(keepapi, userid):
    keep_token = keyring.get_password(KEEP_KEYRING_ID, userid)
    return keep_token


def keep_clear_keyring(keepapi, userid):
    try:
        keyring.delete_password(KEEP_KEYRING_ID, userid)
    except:
        return None
    else:
        return True


def keep_login(keepapi, userid, pw, keyring_reset):
    try:
        keepapi.login(userid, pw)
    except:
        return None
    else:
        keep_token = keepapi.getMasterToken()
        if keyring_reset == False:
            keyring.set_password(KEEP_KEYRING_ID, userid, keep_token)
        return keep_token


def keep_resume(keepapi, keeptoken, userid):
    keepapi.resume(userid, keeptoken)


def keep_save_token(keeptoken, userid):
    keyring.set_password(KEEP_KEYRING_ID, userid, keeptoken)


def keep_download_blob(blob_url, blob_name, blob_path):

    try:

        dest_path = blob_path + "/" + blob_name
        data_file = blob_name + ".dat"

        r = requests.get(blob_url)
        if r.status_code == 200:

            with open(data_file, 'wb') as f:
                f.write(r.content)

            if imghdr.what(data_file) == 'png':
                media_name = blob_name + ".png"
                blob_final_path = dest_path + ".png"
            elif imghdr.what(data_file) == 'jpeg':
                media_name = blob_name + ".jpg"
                blob_final_path = dest_path + ".jpg"
            elif imghdr.what(data_file) == 'gif':
                media_name = blob_name + ".gif"
                blob_final_path = dest_path + ".gif"
            elif imghdr.what(data_file) == 'webp':
                media_name = blob_name + ".webp"
                blob_final_path = dest_path + ".webp"
            else:
                extension = ".aac"
                media_name = blob_name + extension
                blob_final_path = dest_path + extension

            shutil.copyfile(data_file, blob_final_path)
        else:
            media_name = data_file
            blob_final_path = "Media could not be retrieved"

        if os.path.exists(data_file):
            os.remove(data_file)

        media_name = media_name.replace(" ", "%20")
        mediapath = Config().get("media_path").rstrip("/") + "/"
        #mediapath = load_config().get("media_path").rstrip("/") + "/"
        return ("![" + mediapath + media_name + "](" + mediapath + media_name + ")")
    except:
        print("Error in keep_download_blob()")
        raise


def keep_note_name(note_title, note_date):
    if note_title in keep_name_list:
        note_title = note_title + note_date
        note_title = keep_note_name(note_title, note_date)
    return (note_title)


def keep_md_exists(md_file, outpath, note_title, note_date):
    #md_file = Path(outpath, note_title + ".md")
    keep_name_list.remove(note_title)
    while md_file.exists():
        note_title = keep_note_name(note_title, note_date)
        keep_name_list.append(note_title)
        md_file = Path(outpath, note_title + ".md")
    return (note_title)


def keep_save_md_file(keepapi, gnote, note_labels, note_date, overwrite, skip_existing):

    try:

        md_text = gnote.text.replace(u"\u2610", '- [ ]').replace(u"\u2611", ' - [x]')

        # TBD setup_folders()

        outpath = Config().get("output_path").rstrip("/")
        mediapath = Config().get("media_path").rstrip("/")

        if not os.path.exists(outpath):
            os.mkdir(outpath)

        mediapath = outpath + "/" + mediapath + "/"
        if not os.path.exists(mediapath):
            os.mkdir(mediapath)

        gnote.title = keep_note_name(gnote.title, note_date)
        keep_name_list.append(gnote.title)

        md_file = Path(outpath, gnote.title + ".md")
        if not overwrite:
            if md_file.exists():
                if skip_existing:
                    return (0)
                else:
                    gnote.title = keep_md_exists(md_file, outpath, gnote.title, note_date)
                    md_file = Path(outpath, gnote.title + ".md")

        for idx, blob in enumerate(gnote.blobs):
            try:
                image_url = keepapi.getMediaLink(blob)
            except AttributeError as e:
                if "'NoneType' object has no attribute 'type'" in str(e):
                    print(f"continuing, despite note {gnote.title} raising:", repr(e))
                    continue
                raise e
            #print (image_url)
            image_name = gnote.title + str(idx)
            blob_file = keep_download_blob(image_url, image_name, mediapath)
            md_text = blob_file + "\n" + md_text

        print(gnote.title)
        print(note_labels)
        print(note_date + "\r\n")

        f = open(md_file, "w+", encoding='utf-8', errors="ignore")
        f.write(Markdown().convert_urls(md_text) + "\n")
        f.write("\n" + note_labels + "\n\n")
        f.write("Created: " + str((gnote.timestamps.created).strftime("%Y-%m-%d %H:%M:%S")) + 
            "   ---   Updated: " + str((gnote.timestamps.updated).strftime("%Y-%m-%d %H:%M:%S")) + "\n\n")
        f.write("[" + KEEP_NOTE_URL + str(gnote.id) + "](" + KEEP_NOTE_URL + str(gnote.id) + ")\n\n")
        f.close
        return (1)
    except Exception as e:
        raise Exception("Problem with markdown file creation: " + str(md_file) + " -- " + TECH_ERR + repr(e))


def keep_query_convert(keepapi, keepquery, overwrite, archive_only, preserve_labels, skip_existing, text_for_title):

    try:
        count = 0
        ccnt = 0

        if keepquery == "--all":
            gnotes = keepapi.all()
        else:
            if keepquery[0] == "#":
                gnotes = keepapi.find(labels=[keepapi.findLabel(keepquery[1:])], archived=archive_only, trashed=False)
            else:
                gnotes = keepapi.find(query=keepquery, archived=archive_only, trashed=False)
                #for gnote in gnotes:
                #    n = Note(gnote.title)
                #    notes.append(n)

        for gnote in gnotes:
            note_date = re.sub('[^A-z0-9-]', ' ', str(gnote.timestamps.created).replace(":", "").replace(".", "-"))

            if gnote.title == '':
                if text_for_title:
                    gnote.title = re.sub('[' + re.escape(''.join(ILLEGAL_FILE_CHARS)) + ']', '', gnote.text[0:50])  #.replace(' ',''))
                else:
                    gnote.title = note_date

            gnote.title = re.sub('[' + re.escape(''.join(ILLEGAL_FILE_CHARS)) + ']', ' ', gnote.title[0:99])  #re.sub('[^A-z0-9-]', ' ', gnote.title)[0:99]
            #note_text = gnote.text #gnote.text.replace('”','"').replace('“','"').replace("‘","'").replace("’","'").replace('•', "-").replace(u"\u2610", '[ ]').replace(u"\u2611", '[x]').replace(u'\xa0', u' ').replace(u'\u2013', '--').replace(u'\u2014', '--').replace(u'\u2026', '...').replace(u'\u00b1', '+/-')

            note_label_list = gnote.labels
            labels = note_label_list.all()
            note_labels = ""
            if preserve_labels:
                for label in labels:
                    note_labels = note_labels + " #" + str(label)
            else:
                for label in labels:
                    note_labels = note_labels + " #" + str(label).replace(' ', '-').replace('&', 'and')
                note_labels = re.sub('[' + re.escape(''.join(ILLEGAL_TAG_CHARS)) + ']', '-', note_labels)  #re.sub('[^A-z0-9-_# ]', '-', note_labels)

            if archive_only:
                if gnote.archived and gnote.trashed == False:
                    ccnt = keep_save_md_file(keepapi, gnote, note_labels, note_date, overwrite, skip_existing)
                else:
                    ccnt = 0
            else:
                if gnote.archived == False and gnote.trashed == False:
                    ccnt = keep_save_md_file(keepapi, gnote, note_labels, note_date, overwrite, skip_existing)
                else:
                    ccnt = 0

            count = count + ccnt

        name_list.clear()
        if overwrite or skip_existing:
            keep_name_list.clear()

        return (count)
    except:
        print("Error in keep_query_convert()")
        raise


#--------------------- UI / CLI ------------------------------


def ui_login(keepapi, keyring_reset, master_token):

    try:
        userid = Config().get("google_userid").strip().lower()

        if userid == USERID_EMPTY:
            userid = click.prompt('Enter your Google account username', type=str)
        else:
            print("Your Google account name in the " + CONFIG_FILE + " file is: " + userid + " -- Welcome!")

        if keyring_reset:
            print("Clearing keyring")
            keep_clear_keyring(keepapi, userid)

        if master_token:
            ktoken = master_token
            keep_save_token(ktoken, userid)
        else:
            ktoken = keep_token(keepapi, userid)
        if ktoken == None:
            pw = getpass.getpass(prompt='Enter your Google Password: ', stream=None)
            print("\r\n\r\nOne moment...")

            ktoken = keep_login(keepapi, userid, pw, keyring_reset)
            if ktoken:
                if keyring_reset:
                    print("You've succesfully logged into Google Keep!")
                else:
                    print("You've succesfully logged into Google Keep! Your Keep access token has been securely stored in this computer's keyring.")
            #else:
            #  print ("Invalid Google userid or pw! Please try again.")

        else:
            print("You've succesfully logged into Google Keep using local keyring access token!")

        keep_resume(keepapi, ktoken, userid)
        return (ktoken)

    except Exception as e:
        print("\r\nUsername or password is incorrect (" + repr(e) + ")")
        raise


def ui_query(keepapi, search_term, overwrite, archive_only, preserve_labels, skip_existing, text_for_title):

    try:
        if search_term != None:
            count = keep_query_convert(keepapi, search_term, overwrite, archive_only, preserve_labels, skip_existing, text_for_title)
            print("\nTotal converted notes: " + str(count))
            return
        else:
            kquery = "kquery"
            while kquery:
                kquery = click.prompt("\r\nEnter a keyword search, label search or '--all' to convert Keep notes to md or '--x' to exit", type=str)
                if kquery != "--x":
                    count = keep_query_convert(keepapi, kquery, overwrite, archive_only, preserve_labels, skip_existing, text_for_title)
                    print("\nTotal converted notes: " + str(count))
                else:
                    return
    except Exception as e:
        print("Conversion to markdown error - " + repr(e) + " ")
        raise


def ui_welcome_config():
    try:
        mp = Config().get("media_path")

        if ((":" in mp) or (mp[0] == '/')):
            raise ValueError("Media path: '" + mp + "' within your config file - " + CONFIG_FILE +
                             " - must be relative to the output path and cannot start with / or a drive-mount")
        #return defaults
    except Exception as e:
        print("\r\nConfiguration file error - " + CONFIG_FILE + " - " + repr(e) + " ")
        raise


@click.command()
@click.option('-r', is_flag=True, help="Will reset and not use the local keep access token in your system's keyring")
@click.option('-o', is_flag=True, help="Overwrite any existing markdown files with the same name")
@click.option('-a', is_flag=True, help="Search and export only archived notes")
@click.option('-p', is_flag=True, help="Preserve keep labels with spaces and special characters")
@click.option('-s', is_flag=True, help="Skip over any existing notes with the same title")
@click.option('-c', is_flag=True, help="Use starting content within note body instead of create date for md filename")
@click.option('-b', '--search-term', help="Run in batch mode with a specific Keep search term")
@click.option('-t', '--master-token', help="Log in using master keep token")
def main(r, o, a, p, s, c, search_term, master_token):

    try:

        click.echo("\r\nWelcome to Keep it Markdown or KIM!\r\n")

        if o and s:
            print("Overwrite and Skip flags are not compatible together -- please use one or the other...")
            exit()

        kapi = keep_init()

        ui_welcome_config()

        ui_login(kapi, r, master_token)

        ui_query(kapi, search_term, o, a, p, s, c)

    except:
        print("Could not excute KIM")


#Version 0.4.3

if __name__ == '__main__':

    main()  # pylint: disable=no-value-for-parameter
