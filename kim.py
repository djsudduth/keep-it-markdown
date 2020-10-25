import sys
import getopt
import gkeepapi
import keyring
import getpass
import re

KEEP_CACHE = 'kdata.json'
KEEP_KEYRING_ID = 'google-keep-token'

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


def keep_login(keepapi, userid, pw):
    try:
      keepapi.login(userid, pw)
    except:
      return None
    else:
      keep_token = keepapi.getMasterToken()
      keyring.set_password(KEEP_KEYRING_ID, userid, keep_token)
      return keep_token


def keep_resume(keepapi, keeptoken, userid):
    keepapi.resume(userid, keeptoken)



def keep_query_convert(keepapi, keepquery):

    if keepquery == "--all":
      gnotes = keepapi.all()
    else:
      if keepquery[0] == "#":
        gnotes = keepapi.find(labels=[keepapi.findLabel(keepquery[1:])])
      else:
        gnotes = keepapi.find(query=keepquery, archived=False, trashed=False)

    for gnote in gnotes:
      note_date = re.sub('[^A-z0-9-]', ' ', str(gnote.timestamps.created).replace(":","").replace(".", "-"))
      
      if gnote.title == '':
        gnote.title = note_date

      note_title = re.sub('[^A-z0-9-]', ' ', gnote.title)[0:99]
 
      note_text = gnote.text.replace('”','"').replace('“','"').replace("’","'").replace('•', "-").replace(u"\u2610", '[ ]').replace(u"\u2611", '[x]')

      note_label_list = gnote.labels 
      labels = note_label_list.all()
      note_labels = ""
      for label in labels:
        note_labels = note_labels + " #" + str(label).replace(' ','-')

      print (note_title)
      #print (note_text)
      print (note_labels)
      print (note_date)



   # my_file = Path(note_title + ".md")
   # if my_file.exists():
   #   note_title = note_title + note_date

   # f=open(note_title + ".md","w+", errors="ignore")
   # f.write(n + "\r\n")
   # for label in l:
   #   ll = " #" + str(label).replace(' ','-')
      #print (ll)
   #   f.write(ll)

   # f.close
  


def main(argv):
      
    try:
      argv = sys.argv[1:]
      opts, args = getopt.getopt(argv,"r:")
    except:
      print ("\r\n Incorrect syntax for resetting your password. Please use: 'python kim.py -r pw'") 
      exit()

    kapi = keep_init()

    print ("\r\nWelcome to Keep it Markdown or KIM!\r\n")

    userid = input('Enter your Google account username: ')
    for opt, arg in opts:
      if opt == "-r":
        keep_clear_keyring(kapi, userid)
  
    ktoken = keep_token(kapi, userid)
    if ktoken == None:
      pw = getpass.getpass(prompt='Enter your Google Password: ', stream=None) 
      print ("\r\n")

      ktoken = keep_login(kapi, userid, pw)
      if ktoken:
        print ("You've succesfully logged into Google Keep! Your password has been securely stored in this computer's keyring.")
      else:
        print ("Invalid Google userid or pw! Please try again.")

    else:
      print ("You've succesfully logged into Google Keep using local keyring password!")

    keep_resume(kapi, ktoken, userid)

    kquery = "start"
    while kquery:
      kquery = input("\r\nEnter a keyword search or '--all' for all notes to convert to Markdown or just press Enter to exit: ")
      if kquery:
        keep_query_convert(kapi, kquery)
  


if __name__ == '__main__':
    main(sys.argv)
