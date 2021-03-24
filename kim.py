import sys
import os
import getopt
import gkeepapi
import keyring
import getpass
import requests
import imghdr
import shutil
import re
import time
import configparser
import click
from pathlib import Path


KEEP_CACHE = 'kdata.json'
KEEP_KEYRING_ID = 'google-keep-token'
KEEP_NOTE_URL = "https://keep.google.com/#NOTE/"
CONFIG_FILE = "settings.cfg"
DEFAULT_SECTION = "SETTINGS"
USERID_EMPTY = 'add your google account name here'
OUTPUTPATH = 'mdfiles'
MEDIADEFAULTPATH = "media/"

TECH_ERR = " Technical Error Message: "

CONFIG_FILE_MESSAGE = "Your " + CONFIG_FILE + " file contains to the following [" + DEFAULT_SECTION + "] values. Be sure to edit it with your information."
MALFORMED_CONFIG_FILE = "The " + CONFIG_FILE + " default settings file exists but has a malformed header - header should be [DEFAULT]"
UNKNOWNN_CONFIG_FILE = "There is an unknown configuration file issue - " + CONFIG_FILE + " or file system may be locked or corrupted. Try deleting the file and recreating it."
MISSING_CONFIG_FILE = "The configuration file - " + CONFIG_FILE + " is missing. Please check the documention on recreating it"
BADFILE_CONFIG_FILE = "Unable to create " + CONFIG_FILE + ". The file system issue such as locked or corrupted"

ILLEGAL_FILE_CHARS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '&', '\n', '\r', '\t']
ILLEGAL_TAG_CHARS = ['~', '`', '!', '@', '$', '%', '^', '(', ')', '+', '=', '{', '}', '[', ']', '<', '>', ';', ':', ',', '.', '"', '/', '\\', '|', '?', '*', '&', '\n', '\r']
 
default_settings = {
    'google_userid': USERID_EMPTY,
    'output_path': OUTPUTPATH
    }

media_downloaded = False

name_list = []
keep_name_list = []


class ConfigurationException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg



def load_config():
    config = configparser.ConfigParser()
  
    try:
        cfile = config.read(CONFIG_FILE)
    except configparser.MissingSectionHeaderError:
        raise ConfigurationException(MALFORMED_CONFIG_FILE)
    except Exception:
        raise ConfigurationException(UNKNOWNN_CONFIG_FILE)
    
    configdict = {}
    if not cfile:
        config[DEFAULT_SECTION] = default_settings
        try:
            with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)
        except Exception as e:
            raise (e)
    options = config.options(DEFAULT_SECTION)
    for option in options:
        configdict[option] = config.get(DEFAULT_SECTION, option)
    return configdict 



# Note that the use of temporary %%% is because notes can have the same URL repeated and replace would fail
def url_to_md(text):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[~#$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    for url in urls:
      text = text.replace(url, "[" + url[:1] + "%%%" +url[2:] + "]("+url[:1] + "%%%" +url[2:]+")", 1)
    return(text.replace("h%%%tp", "http"))


    

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

    dest_path = blob_path + "/" + blob_name
    data_file = blob_name + ".dat"

    r = requests.get(blob_url)
    if r.status_code == 200:

      with open(data_file,'wb') as f:
        f.write(r.content)

      if imghdr.what(data_file) == 'png':
        media_name = blob_name + ".png"
        blob_final_path = dest_path + ".png"
      elif imghdr.what(data_file) == 'jpeg':
        media_name = blob_name + ".jpg"
        blob_final_path = dest_path + ".jpg"
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
    return("![" + MEDIADEFAULTPATH + media_name + "](" + MEDIADEFAULTPATH + media_name + ")")


def keep_note_name(note_title, note_date):
    if note_title in keep_name_list:
      note_title = note_title + note_date
      note_title = keep_note_name(note_title, note_date)
    return(note_title)


def keep_md_exists(md_file, outpath, note_title, note_date):
    #md_file = Path(outpath, note_title + ".md")
    keep_name_list.remove(note_title)
    while md_file.exists():
      note_title = keep_note_name(note_title, note_date)
      keep_name_list.append(note_title)
      md_file = Path(outpath, note_title + ".md")
    return(note_title)


def keep_save_md_file(keepapi, gnote, note_labels, note_date, overwrite, skip_existing):

    try:
      outpath = load_config().get("output_path")
  
      if outpath == OUTPUTPATH:
        if not os.path.exists(OUTPUTPATH):
          os.mkdir(OUTPUTPATH)
      mediapath = outpath + "/" + MEDIADEFAULTPATH
      if not os.path.exists(mediapath):
          os.mkdir(mediapath)

      gnote.title = keep_note_name(gnote.title, note_date)
      keep_name_list.append(gnote.title)

      md_file = Path(outpath, gnote.title + ".md")
      if not overwrite:
          if md_file.exists():
            if skip_existing:
              return(0)
            else:
              gnote.title = keep_md_exists(md_file, outpath, gnote.title, note_date)
              md_file = Path(outpath, gnote.title + ".md")
      
      note_text=gnote.text

      for idx, blob in enumerate(gnote.blobs):
        image_url = keepapi.getMediaLink(blob)
        #print (image_url)
        image_name = gnote.title + str(idx)
        blob_file = keep_download_blob(image_url, image_name, mediapath)
        note_text = blob_file + "\n" + note_text
 
      print("{} - {}".format(note_date,gnote.title))
  
      f=open(md_file,"w+", encoding='utf-8', errors="ignore")
      #f.write(url_to_md(url_to_md(note_text, "http://"), "https://") + "\n")
      f.write(url_to_md(note_text) + "\n")
      f.write("\n" + note_labels + "\n\n")
      f.write("Created: " + str(gnote.timestamps.created) + "      Updated: " + str(gnote.timestamps.updated) + "\n\n")
      f.write("["+ KEEP_NOTE_URL + str(gnote.id) + "](" + KEEP_NOTE_URL + str(gnote.id) + ")\n\n")
      f.close
      return(1)
    except Exception as e:
      raise Exception("Problem with markdown file creation: " + str(md_file) + "\r\n" + TECH_ERR + repr(e))



def keep_query_convert(keepapi, keepquery, overwrite, archive_only, preserve_labels, skip_existing, text_for_title):

    count = 0

    if keepquery == "--all":
      gnotes = keepapi.all()
    else:
      if keepquery[0] == "#":
        gnotes = keepapi.find(labels=[keepapi.findLabel(keepquery[1:])], archived=archive_only, trashed=False)
      else:
        gnotes = keepapi.find(query=keepquery, archived=archive_only, trashed=False)

    for gnote in gnotes:
      note_date = re.sub('[^A-z0-9-]', ' ', str(gnote.timestamps.created).replace(":","").replace(".", "-"))
      
      if gnote.title == '':
        if text_for_title:
          gnote.title = re.sub('[' + re.escape(''.join(ILLEGAL_FILE_CHARS)) + ']', '', gnote.text[0:50]) #.replace(' ',''))
        else:
          gnote.title = note_date


      gnote.title = re.sub('[' + re.escape(''.join(ILLEGAL_FILE_CHARS)) + ']', ' ', gnote.title[0:99]) #re.sub('[^A-z0-9-]', ' ', gnote.title)[0:99]
      #note_text = gnote.text #gnote.text.replace('”','"').replace('“','"').replace("‘","'").replace("’","'").replace('•', "-").replace(u"\u2610", '[ ]').replace(u"\u2611", '[x]').replace(u'\xa0', u' ').replace(u'\u2013', '--').replace(u'\u2014', '--').replace(u'\u2026', '...').replace(u'\u00b1', '+/-')
 
      note_label_list = gnote.labels 
      labels = note_label_list.all()
      note_labels = ""
      if preserve_labels:
        for label in labels:
          note_labels = note_labels + " #" + str(label)
      else:
        for label in labels:
          note_labels = note_labels + " #" + str(label).replace(' ','-').replace('&','and')
        note_labels = re.sub('[' + re.escape(''.join(ILLEGAL_TAG_CHARS)) + ']', '-', note_labels) #re.sub('[^A-z0-9-_# ]', '-', note_labels)
       
    
      if archive_only:
        if gnote.archived and gnote.trashed == False:
          ccnt = keep_save_md_file(keepapi, gnote, note_labels, note_date, overwrite, skip_existing)
      else: 
        if gnote.archived == False and gnote.trashed == False:
          ccnt = keep_save_md_file(keepapi, gnote, note_labels, note_date, overwrite, skip_existing)

      count = count + ccnt

    name_list.clear()
    if overwrite or skip_existing:
      keep_name_list.clear()

    return (count)


#--------------------- UI / CLI ------------------------------

def ui_login(keepapi, defaults, keyring_reset, master_token):

    try:
      
      userid = defaults.get("google_userid").strip().lower()
    
      if userid == USERID_EMPTY:
        userid = click.prompt('Enter your Google account username', type=str)
      else:
        print("Your Google account name in the " + CONFIG_FILE + " file is: " + userid + " -- Welcome!")
  
      if keyring_reset:
        print ("Clearing keyring")
        keep_clear_keyring(keepapi, userid)

      if master_token:
        ktoken = master_token
        keep_save_token(ktoken, userid)
      else:
        ktoken = keep_token(keepapi, userid)
      if ktoken == None:
        pw = getpass.getpass(prompt='Enter your Google Password: ', stream=None) 
        print ("\r\n\r\nOne moment...")

        ktoken = keep_login(keepapi, userid, pw, keyring_reset)
        if ktoken:
          if keyring_reset:
            print ("You've succesfully logged into Google Keep!")
          else:
            print ("You've succesfully logged into Google Keep! Your Keep access token has been securely stored in this computer's keyring.")
        else:
          print ("Invalid Google userid or pw! Please try again.")

      else:
        print ("You've succesfully logged into Google Keep using local keyring access token!")

      keep_resume(keepapi, ktoken, userid)
      return (ktoken)

    except:
      print ("\r\nUsername or password is incorrect") 
      exit()


def ui_query(keepapi, search_term, overwrite, archive_only, preserve_labels, skip_existing, text_for_title):

    if search_term != None:
        count = keep_query_convert(keepapi, search_term, overwrite, archive_only, preserve_labels, skip_existing, text_for_title)
        print ("\nTotal converted notes: " + str(count))
        exit()
    else:
      kquery = "kquery"
      while kquery:
        kquery = click.prompt("\r\nEnter a keyword search, label search or '--all' to convert Keep notes to md or '--x' to exit", type=str)
        if kquery != "--x":
          count = keep_query_convert(keepapi, kquery, overwrite, archive_only, preserve_labels, skip_existing, text_for_title)
          print ("\nTotal converted notes: " + str(count))
        else:
          exit()
  
def ui_welcome_config():
    print ("\r\nWelcome to Keep it Markdown or KIM!\r\n")
    return load_config()



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

    if o and s:
        print ("Overwrite and Skip flags are not compatible together -- please use one or the other...")
        exit()

    kapi = keep_init()

    ui_login(kapi, ui_welcome_config(), r, master_token)
 
    ui_query(kapi, search_term, o, a, p, s, c)
      
      
  except Exception as e:
    print (e)
 




if __name__ == '__main__':

    main()
