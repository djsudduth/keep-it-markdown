import sys
import gkeepapi
import keyring
import getpass

KEEP_CACHE = 'kdata.json'
KEEP_KEYRING_ID = 'google-keep-token'

def keep_init():
    keepapi = gkeepapi.Keep()
    return keepapi


def keep_token(keepapi, userid):
   keep_token = keyring.get_password(KEEP_KEYRING_ID, userid)
   return keep_token
   #  keyring.delete_password('google-keep-token', userid)


def keep_login(keepapi, userid):
    try:
      keepapi.login(userid, pw)
    except:
      return None
    else:
      keep_token = keepapi.getMasterToken()
      keyring.set_password(KEEP_KEYRING_ID, userid, keep_token)
      return keep_token


def main(argv):
    print ("Welcome to Keep it Markdown or Kim!")
    userid = input('Enter your Google username: ')
    pw = getpass.getpass(prompt='Enter your Google Password: ', stream=None) 
    print (userid, pw)
 


if __name__ == '__main__':
    main(sys.argv)
