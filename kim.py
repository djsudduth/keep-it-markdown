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


 
default_settings = {
    'google_userid': USERID_EMPTY,
    'output_path': OUTPUTPATH
    }

media_downloaded = False


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


def url_to_md(text, url_prefix):
    idx = 0
    idxstart = 0
    while idx >= 0:
        idx = text.find(url_prefix, idx)
        idxend = text.find("\n", idx)
        if idxend < 0:
          idxend = text.find(" ", idx)
        if idxend < 0:
            idxend = len(text)
        if idx >= 0:
            url = text[idx: idxend]
            textleft = text[0: idx]
            textright = text[idx: len(text)]
            textright = textright.replace(url, url.replace(url, "[" + url + "](" + url + ")"), 1)
            text = textleft + textright
            idxstart = idx
            idxend = idxend + len(url) + 4
            idx = idxend

    return text
    

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
        extension = ".m4a"
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


def keep_save_md_file(keepapi, note_title, note_text, note_labels, note_blobs, note_date, note_created, note_updated, note_id, overwrite):

    try:
      outpath = load_config().get("output_path")
  
      if outpath == OUTPUTPATH:
        if not os.path.exists(OUTPUTPATH):
          os.mkdir(OUTPUTPATH)
      mediapath = outpath + "/" + MEDIADEFAULTPATH
      if not os.path.exists(mediapath):
          os.mkdir(mediapath)

      file_exists = True
      while file_exists:
        md_file = Path(outpath, note_title + ".md")
        if md_file.exists() and overwrite == False:
          note_title = note_title + note_date
          md_file = Path(outpath, note_title + ".md")
        else:
          file_exists = False

      for idx, blob in enumerate(note_blobs):
        image_url = keepapi.getMediaLink(blob)
        #print (image_url)
        image_name = note_title + str(idx)
        blob_file = keep_download_blob(image_url, image_name, mediapath)
        note_text = blob_file + "\n" + note_text 
 

      print (note_title)
      #print (gnote.archived)
      print (note_labels)
      print (note_date + "\r\n")
  
      f=open(md_file,"w+", errors="ignore")
      f.write(url_to_md(url_to_md(note_text, "http://"), "https://") + "\n")
      f.write("\n" + note_labels + "\n\n")
      f.write("Created: " + note_created + "      Updated: " + note_updated + "\n\n")
      f.write("["+ KEEP_NOTE_URL + note_id + "](" + KEEP_NOTE_URL + note_id + ")\n\n")
      f.close
    except Exception as e:
      raise Exception("Problem with markdown file creation: " + str(md_file) + "\r\n" + TECH_ERR + repr(e))



def keep_query_convert(keepapi, keepquery, overwrite, archive_only):

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
        gnote.title = note_date

      note_title = re.sub('[^A-z0-9-]', ' ', gnote.title)[0:99]
 
      note_text = gnote.text.replace('”','"').replace('“','"').replace("‘","'").replace("’","'").replace('•', "-").replace(u"\u2610", '[ ]').replace(u"\u2611", '[x]').replace(u'\xa0', u' ').replace(u'\u2013', '--').replace(u'\u2014', '--').replace(u'\u2026', '...').replace(u'\u00b1', '+/-')

      note_label_list = gnote.labels 
      labels = note_label_list.all()
      note_labels = ""
      for label in labels:
        note_labels = note_labels + " #" + str(label).replace(' ','-').replace('&','and')
      note_labels = re.sub('[^A-z0-9-_# ]', '-', note_labels)
      
      if archive_only:
        if gnote.archived and gnote.trashed == False:
          keep_save_md_file(keepapi, note_title, note_text, note_labels, gnote.blobs, note_date, str(gnote.timestamps.created), str(gnote.timestamps.updated), str(gnote.id), overwrite)
      else: 
        if gnote.archived == False and gnote.trashed == False:
          keep_save_md_file(keepapi, note_title, note_text, note_labels, gnote.blobs, note_date, str(gnote.timestamps.created), str(gnote.timestamps.updated), str(gnote.id), overwrite)




#--------------------- UI / CLI ------------------------------

def ui_login(keepapi, defaults, keyring_reset):

    try:
      
      userid = defaults.get("google_userid").strip().lower()
    
      if userid == USERID_EMPTY:
        userid = click.prompt('Enter your Google account username', type=str)
      else:
        print("Your Google account name in the " + CONFIG_FILE + " file is: " + userid + " -- Welcome!")
  
      if keyring_reset:
        print ("Clearing keyring")
        keep_clear_keyring(keepapi, userid)
    
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


def ui_query(keepapi, search_term, overwrite, archive_only):

    if search_term != None:
        keep_query_convert(keepapi, search_term, overwrite, archive_only)
        exit()
    else:
      kquery = "kquery"
      while kquery:
        kquery = click.prompt("\r\nEnter a keyword search, label search or '--all' to convert Keep notes to md or '--x' to exit", type=str)
        if kquery != "--x":
          keep_query_convert(keepapi, kquery, overwrite, archive_only)
        else:
          exit()
  
def ui_welcome_config():
    print ("\r\nWelcome to Keep it Markdown or KIM!\r\n")
    return load_config()


@click.command()
@click.option('-r', is_flag=True, help="Will reset and not use the local keep access token in your system's keyring")
@click.option('-o', is_flag=True, help="Overwrite any existing markdown files with the same name")
@click.option('-a', is_flag=True, help="Search and export only archived notes")
@click.option('-b', '--search-term', help="Run in batch mode with a specific Keep search term")
def main(r, o, a, search_term):

  try:

    kapi = keep_init()

    ui_login(kapi, ui_welcome_config(), r)
 
    ui_query(kapi, search_term, o, a)
      
      
  except Exception as e:
    print (e)
 

if __name__ == '__main__':
    main()
