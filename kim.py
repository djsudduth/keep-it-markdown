import os
import gkeepapi
import keyring
import getpass
import requests
import shutil
import re
import configparser
import click
import datetime
from os.path import join
from pathlib import Path
from dataclasses import dataclass
from xmlrpc.client import boolean
from PIL import Image


KEEP_KEYRING_ID = 'google-keep-token'
KEEP_NOTE_URL = "https://keep.google.com/#NOTE/"
CONFIG_FILE = "settings.cfg"
DEFAULT_SECTION = "SETTINGS"
USERID_EMPTY = 'add your google account name here'
OUTPUTPATH = 'mdfiles'
MEDIADEFAULTPATH = "media"
INPUTDEFAULTPATH = "import/markdown_files"
DEFAULT_LABELS = "my_label"
DEFAULT_SEPARATOR = "/"
MAX_FILENAME_LENGTH = 99
MISSING = 'null value'

TECH_ERR = " Technical Error Message: "

CONFIG_FILE_MESSAGE = ("Your " + CONFIG_FILE + " file contains to the following [" 
                        + DEFAULT_SECTION + "] values. Be sure to edit it with "
                        " your information.")
MALFORMED_CONFIG_FILE = ("The " + CONFIG_FILE + " default settings file exists but "
                        "has a malformed header - header should be [" + DEFAULT_SECTION + "]")
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
ILLEGAL_TAG_CHARS = ['~', '`', '!', '@', '$', '%', '^', '(', ')', '+', '=', '{', '}', '[', \
        ']', '<', '>', ';', ':', ',', '.', '"', '/', '\\', '|', '?', '*', '&', '\n', '\r']

default_settings = {
    'google_userid': USERID_EMPTY,
    'output_path': OUTPUTPATH,
    'media_path': MEDIADEFAULTPATH,
    'input_path': INPUTDEFAULTPATH,
    'input_labels': DEFAULT_LABELS,
    'folder_separator': DEFAULT_SEPARATOR
}


notes = []

@dataclass
class Options:
    overwrite: boolean
    archive_only: boolean
    preserve_labels: boolean
    skip_existing: boolean 
    text_for_title: boolean
    logseq_style: boolean
    joplin_frontmatter: boolean
    move_to_archive: boolean
    import_files: boolean

@dataclass
class Note:
    id: str
    title: str
    text: str
    archived: boolean
    trashed: boolean
    timestamps: dict
    labels: list
    blobs: list
    blob_names: list
    media: list
    header: str




class ConfigurationException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


# This is a singleton class instance - not really necessary but saves a tiny bit of memory 
# Very useful for single connections and loading config files once
class Config:
    _config = configparser.ConfigParser()
    _configdict = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
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


#All conversions to markdown are static methods 
class Markdown:
    @staticmethod
    def convert_urls(text):
        # pylint: disable=anomalous-backslash-in-string
        urls = re.findall(
            "http[s]?://(?:[a-zA-Z]|[0-9]|[~#$-_@.&+]"
                "|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            text
        )
        #Note that the use of temporary %%% is because notes 
        #   can have the same URL repeated and replace would fail
        for url in urls:
            text = text.replace(url, 
                "[" + url[:1] + "%%%" + url[2:] + 
                "](" + url[:1] + "%%%" + url[2:] + ")", 1)

        return text.replace("h%%%tp", "http")

    @staticmethod
    def format_checkboxes(text):
        md_text = text.replace(u"\u2610", '- [ ]') \
            .replace(u"\u2611", ' - [x]')
        return md_text

    #this feels more like a file utility than a markdown utility
    @staticmethod
    def format_title(title):
        title = re.sub(
            '[' + re.escape(''.join(ILLEGAL_FILE_CHARS)) + ']', 
            ' ', 
            title[0:MAX_FILENAME_LENGTH]
        ) 
        return title

    @staticmethod
    def format_check_boxes(text):
        return(text.replace(u"\u2610", '- [ ]').replace(u"\u2611", ' - [x]'))

    @staticmethod
    def format_path(path, name, media, replacement):
        if media:
            header = "!["
        else:
            header = "["
        path = path.replace(" ", replacement)
        if name:
            return (header + name + "](" + path + ")")
        else:
            return (header + path + "](" + path + ")")

  


class SecureStorage:
    def __init__(self, userid, keyring_reset, master_token):
        self._userid = userid
        if keyring_reset:
            self._clear_keyring()
        if master_token:
            self.set_keyring(master_token)

    def get_keyring(self):
        self._keep_token = keyring.get_password(
            KEEP_KEYRING_ID, self._userid)
        return self._keep_token

    def set_keyring(self, keeptoken):
        keyring.set_password(
            KEEP_KEYRING_ID, self._userid, keeptoken)

    def _clear_keyring(self):
        try:
            keyring.delete_password(
                KEEP_KEYRING_ID, self._userid)
        except:
            return None
        else:
            return True




class KeepService:
    def __init__(self, userid):
        self._keepapi = gkeepapi.Keep()
        self._userid = userid

    def get_ref(self):
        return(self._keepapi)

    def keep_sync(self):
        self._keepapi.sync()

    def set_token(self, keyring_reset, master_token):
        self._securestorage = SecureStorage(
            self._userid, keyring_reset, master_token)
        if master_token:
            self._keep_token = master_token
        else:
            self._keep_token = self._securestorage.get_keyring()
        return self._keep_token

    def set_user(self, userid):
        self._userid = userid

    def login(self, pw, keyring_reset):
        try:
            self._keepapi.login(self._userid, pw)
        except:
            return None
        else:
            self._keep_token = self._keepapi.getMasterToken()
            if keyring_reset == False:
                self._securestorage.set_keyring(self._keep_token)
            return self._keep_token

    def resume(self):
        self._keepapi.resume(self._userid, self._keep_token)

    def getnotes(self):
        return(self._keepapi.all())

    def findnotes(self, kquery, labels, archive_only):
        if labels:
            return(self._keepapi.find(labels=[self._keepapi.findLabel(kquery[1:])], 
                archived=archive_only, trashed=False))
        else:
            return(self._keepapi.find(query=kquery, 
                archived=archive_only, trashed=False))

    def createnote(self, title, notetext):
        self._note = self._keepapi.createNote(title, notetext)
        return(None)
    
    def appendnotes(self, kquery, append_text):
        gnotes = self.findnotes(kquery, False, False)
        for gnote in gnotes:
            gnote.text += "\n\n" + append_text
        self.keep_sync()
        return(None)

    def setnotelabel(self, label):
        try:
            self._labelid = self._keepapi.findLabel(label)
            self._note.labels.add(self._labelid)
        except Exception as e:
            print('Label doesn\'t exist! - label: ' +  label + "  Use pre-defined labels when importing")
            raise

    def getmedia(self, blob):
        try:
            link = self._keepapi.getMediaLink(blob)
            return(link)
        except Exception as e:
            return(None)





class NameService:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(NameService, cls).__new__(cls)
            cls.instance._namelist = []
        return cls.instance

    def clear_name_list(self):
        self._namelist.clear()

    def check_duplicate_name(self, note_title, note_date):
        if note_title in self._namelist:
            note_title = note_title + note_date
            note_title = self.check_duplicate_name(note_title, note_date)
        self._namelist.append(note_title)
        return (note_title)

    def check_file_exists(self, md_file, outpath, note_title, note_date):
        #md_file = Path(outpath, note_title + ".md")
        self._namelist.remove(note_title)
        while md_file.exists():
            note_title = self.check_duplicate_name(note_title, note_date)
            self._namelist.append(note_title)
            md_file = Path(outpath, note_title + ".md")
        return (note_title)



class FileService:
    def media_path (self):
        outpath = Config().get("output_path").rstrip("/")
        mediapath = outpath + "/" + Config().get("media_path").rstrip("/") + "/"
        return(mediapath)

    def outpath (self):
        outpath = Config().get("output_path").rstrip("/")
        return(outpath)

    def inpath (self):
        inpath = Config().get("input_path").rstrip("/") + "/"
        return(inpath)

    def create_path(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def write_file(self, file_name, data):
        try:
            f = open(file_name, "w+", encoding='utf-8', errors="ignore")
            f.write(data)
            f.close
        except Exception as e:
            raise Exception("Error in write_file: " + " -- " + TECH_ERR + repr(e))

    def download_file(self, file_url, file_name, file_path):
        try:
            data_file = file_path + file_name 
            r = requests.get(file_url)
            if r.status_code == 200:
                with open(data_file, 'wb') as f:
                    f.write(r.content)
                    f.close
                return (data_file)
    
            else:
                blob_final_path = "Media could not be retrieved"
                return ("")

        except:
            print("Error in download_file()")
            raise

    def set_file_extensions(self, data_file, file_name, file_path):
        dest_path = file_path + file_name

        try:
            image = Image.open(data_file)
            what = image.format.lower()
            image.close()
        except:
            what = ".m4a"


        if what == 'png':
            media_name = file_name + ".png"
            blob_final_path = dest_path + ".png"
        elif what == 'jpeg':
            media_name = file_name + ".jpg"
            blob_final_path = dest_path + ".jpg"
        elif what == 'gif':
            media_name = file_name + ".gif"
            blob_final_path = dest_path + ".gif"
        elif what == 'webp':
            media_name = file_name + ".webp"
            blob_final_path = dest_path + ".webp"
        else:
            extension = ".m4a"
            media_name = file_name + extension
            blob_final_path = dest_path + extension

        shutil.copyfile(data_file, blob_final_path)

        if os.path.exists(data_file):
            os.remove(data_file)

        return (media_name)



def save_md_file(note, note_tags, note_date, overwrite, skip_existing):
    try:
        fs = FileService()

        md_text = Markdown().format_check_boxes(note.text)
        note.title = NameService().check_duplicate_name(note.title, note_date)

        for media in note.media:
            md_text = Markdown().format_path(Config().get("media_path") + 
                "/" + media, "", True, "_") + "\n" + md_text
 

        md_file = Path(fs.outpath(), note.title + ".md")
        if not overwrite:
            if md_file.exists():
                if skip_existing:
                    return (0)
                else:
                    note.title = NameService().check_file_exists(
                            md_file, fs.outpath(), note.title, note_date)
                    md_file = Path(fs.outpath(), note.title + ".md")

        print(note.title)
        print(note_tags)
        print(note_date + "\r\n")

        if not (note.timestamps):
            timestamps = ""
        else:
            timestamps = ("Created: " + note.timestamps["created"]
                        [ : note.timestamps["created"].rfind('.') ] + "   ---   " + 
                        "Updated: " + note.timestamps["updated"]
                        [ : note.timestamps["updated"].rfind('.') ] + "\n\n")

        markdown_data = (
            note.header + 
            Markdown().convert_urls(md_text) + "\n" + 
            "\n" + note_tags + "\n\n" + 
            timestamps + 
            Markdown().format_path(KEEP_NOTE_URL + str(note.id), "", False, "%20") + "\n\n")

        fs.write_file(md_file, markdown_data)
        return (1)
    except Exception as e:
        raise Exception("Problem with markdown file creation: " + str(md_file) + " -- " + TECH_ERR + repr(e))



def keep_import_notes(keep):
    try:
        dir_path = FileService().inpath()
        in_labels = Config().get("input_labels").split(",")
        for file in os.listdir(dir_path):
            if os.path.isfile(dir_path + file) and file.endswith('.md'):
                with open(dir_path + file, 'r', encoding="utf8") as md_file:
                    mod_time = datetime.datetime.fromtimestamp(
                        os.path.getmtime(dir_path + file)).strftime('%Y-%m-%d %H:%M:%S')
                    crt_time = datetime.datetime.fromtimestamp(
                        os.path.getctime(dir_path + file)).strftime('%Y-%m-%d %H:%M:%S')
                    data=md_file.read()
                    data += "\n\nCreated: " + crt_time + "   -   Updated: " + mod_time
                    print('Importing note:', file.replace('.md', '') + " from " + file)
                    keep.createnote(file.replace('.md', ''), data)
                    for in_label in in_labels:
                        keep.setnotelabel(in_label.strip())
                    keep.keep_sync()
    except Exception as e:
        print('Error on note import:', str(e))



def keep_get_blobs(keep, note):
    fs = FileService()
    for idx, blob in enumerate(note.blobs):
        note.blob_names[idx] = note.title.replace(" ", "_") + str(idx)
        if blob != None:
            url = keep.getmedia(blob)
            blob_file = None
            if url:
                blob_file = fs.download_file(url, note.blob_names[idx] + ".dat", fs.media_path()) 
                if blob_file:
                    data_file = fs.set_file_extensions(blob_file, note.blob_names[idx], fs.media_path())
                    note.media.append(data_file)
                else:
                    print ("Download of Keep media failed...")



def keep_query_convert(keep, keepquery, opts):
    try:
        count = 0
        ccnt = 0

        if keepquery == "--all":
            gnotes = keep.getnotes()
        else:
            if keepquery[0] == "#":
                gnotes = keep.findnotes(keepquery, True, opts.archive_only)
            else:
                gnotes = keep.findnotes(keepquery, False, opts.archive_only)
               
        notes = []

        for gnote in gnotes:
            notes.append(
                Note(
                    gnote.id, 
                    gnote.title, 
                    gnote.text, 
                    gnote.archived,
                    gnote.trashed,
                    {"created": str(gnote.timestamps.created), 
                        "updated": str(gnote.timestamps.updated)},
                    [str(label) for label in gnote.labels.all()],
                    [blob for blob in gnote.blobs],
                    ['' for blob in gnote.blobs], 
                    [],
                    ""
                   )
            )
            if opts.move_to_archive:
                gnote.archived = True

 
        for note in notes:

            note_date = re.sub('[^A-z0-9-]', ' ', note.timestamps["created"].replace(":", "").replace(".", "-"))

            if note.title == '':
                if opts.text_for_title:
                    if note.text == '':
                        note.title = note_date
                    else:
                        note.title = re.sub('[' + re.escape(''.join(ILLEGAL_FILE_CHARS)) + ']', '', note.text[0:50])  #.replace(' ',''))
                else:
                    note.title = note_date

            note.title = re.sub('[' + re.escape(''.join(ILLEGAL_FILE_CHARS)) + ']', ' ', note.title[0:99]) 

            labels = note.labels
            note_labels = ""
            if opts.preserve_labels:
                for label in labels:
                    note_labels = note_labels + " #" + str(label)
            else:
                for label in labels:
                    note_labels = note_labels + " #" + str(label).replace(' ', '-').replace('&', 'and')
                note_labels = re.sub('[' + re.escape(''.join(ILLEGAL_TAG_CHARS)) + 
                                     ']', '-', note_labels)  

            if opts.logseq_style:
                c = note.text[:1]
                if c == u"\u2610" or c == u"\u2611":
                    note.text.replace("\n\n", "\n- ")
                else:
                    note.text = "- " + note.text.replace("\n\n", "\n- ")

            if opts.joplin_frontmatter:
                joplin_labels = ""
                for label in note_labels.replace("#", "").split():
                    joplin_labels += "  - " + label + "\n"
                note.header = ("---\ntitle: " + note.title + 
                            "\nupdated: " + note.timestamps["updated"] + 
                            "Z\ncreated: " + note.timestamps["created"] + 
                            "Z\ntags:\n" + joplin_labels + 
                            "---\n\n")
                note_labels = ""
                note.timestamps = {}


            if opts.archive_only:
                if note.archived and note.trashed == False:
                    keep_get_blobs(keep, note)
                    ccnt = save_md_file(note, 
                                        note_labels, 
                                        note_date, 
                                        opts.overwrite, 
                                        opts.skip_existing)
                else:
                    ccnt = 0
            else:
                if note.archived == False and note.trashed == False:
                    keep_get_blobs(keep, note)
                    ccnt = save_md_file(note, 
                                        note_labels, 
                                        note_date, 
                                        opts.overwrite, 
                                        opts.skip_existing)
                else:
                    ccnt = 0

            count = count + ccnt

        if opts.overwrite or opts.skip_existing:
            NameService().clear_name_list()

        if opts.move_to_archive:
            keep.keep_sync()

        return (count)
    except:
        print("Error in keep_query_convert()")
        raise



#--------------------- UI / CLI ------------------------------


def ui_login(keyring_reset, master_token):
    try:
        userid = Config().get("google_userid").strip().lower()

        if userid == USERID_EMPTY:
            userid = click.prompt('Enter your Google account username', type=str)
        else:
            print("Your Google account name in the " + CONFIG_FILE + " file is: " + userid + " -- Welcome!")

        #0.5.0 work
        keep = KeepService(userid)
        ktoken = keep.set_token(keyring_reset, master_token)

        if ktoken == None:
            pw = getpass.getpass(prompt='Enter your Google Password: ', stream=None)
            print("\r\n\r\nOne moment...")

            ktoken = keep.login(pw, keyring_reset)
            if ktoken:
                if keyring_reset:
                    print("You've succesfully logged into Google Keep!")
                else:
                    print("You've succesfully logged into Google Keep! " + 
                        "Your Keep access token has been securely stored in this computer's keyring.")
            #else:
            #  print ("Invalid Google userid or pw! Please try again.")

        else:
            print("You've succesfully logged into Google Keep using local keyring access token!")

        keep.resume()
        return keep

    except Exception as e:
        print("\r\nUsername or password is incorrect (" + repr(e) + ")")
        raise


def ui_query(keep, search_term, opts):
    try:
        if search_term != None:
            count = keep_query_convert(keep, search_term, opts)
            print("\nTotal converted notes: " + str(count))
            return
        else:
            kquery = "kquery"
            while kquery:
                kquery = click.prompt("\r\nEnter a keyword search, label search or " + 
                    "'--all' to convert Keep notes to md or '--x' to exit", type=str)
                if kquery != "--x":
                    count = keep_query_convert(keep, kquery, opts)
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

        #Make sure paths are set before doing anything
        fs = FileService()
        fs.create_path(fs.outpath())
        fs.create_path(fs.media_path())

 
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
@click.option('-l', is_flag=True, help="Prepend paragraphs with Logseq style bullets")
@click.option('-j', is_flag=True, help="Prepend notes with Joplin front matter tags and dates")
@click.option('-m', is_flag=True, help="Move any exported Keep notes to Archive")
@click.option('-i', is_flag=True, help="Import notes from markdown files EXPERIMENTAL!!")
@click.option('-b', '--search-term', help="Run in batch mode with a specific Keep search term")
@click.option('-t', '--master-token', help="Log in using master keep token")
def main(r, o, a, p, s, c, l, j, m, i, search_term, master_token):

    try:

        #m = True
        opts = Options(o, a, p, s, c, l, j, m, i)
        click.echo("\r\nWelcome to Keep it Markdown or KIM!\r\n")

        if i and (r or o or a or s or p or c or m):
            print ("Importing markdown notes with export options is not compatible -- please use -i only to import")
            exit()

        if o and s:
            print("Overwrite and Skip flags are not compatible together -- please use one or the other...")
            exit()

        ui_welcome_config()

        keep = ui_login(r, master_token)


        if i:
            keep_import_notes(keep)
        else:
            ui_query(keep, search_term, opts)

    except:
        print("Could not excute KIM")
    #except Exception as e:
    #    raise Exception("Problem with markdown file creation: " + repr(e))


#Version 0.5.4

if __name__ == '__main__':

    main()  # pylint: disable=no-value-for-parameter
