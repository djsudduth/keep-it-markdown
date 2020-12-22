import sys
import gkeepapi
import getpass


TECH_ERR = " Technical Error Message: "

class KeepLoginException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

def keep_init():
    keepapi = gkeepapi.Keep()
    return keepapi


def keep_login(keepapi, userid, pw):
    keepapi.login(userid, pw)
    keep_token = keepapi.getMasterToken()
    return keep_token



def ui_login(keepapi, show_token):

    try:
        userid = input('\r\nEnter your Google account username: ')
    
        pw = getpass.getpass(prompt='Enter your Google Password: ', stream=None) 

        ktoken = keep_login(keepapi, userid, pw)
        if ktoken:
            if show_token:
                print (ktoken)
            print ("Test worked!! You've succesfully logged into Google Keep! Please try running Keep-it-Markdown or KIM!")
        else:
            raise Exception
            #print ("Invalid Google userid or pw! Please try again.")

        return (ktoken)

    except Exception as e:
        raise KeepLoginException("Login attempt failed\r\n" + TECH_ERR + repr(e))




def main(argv):

    try:

        show_token = False
        if len(argv) > 1:
           if argv[1] == "-t":
               show_token = True

        kapi = keep_init()

        ui_login(kapi, show_token)

    except Exception as e:
        print (e)
        print ("Please start your browswer and copy-paste this URL in the address bar: https://accounts.google.com/DisplayUnlockCaptcha - then, try logging in again.")

   


if __name__ == '__main__':
    main(sys.argv)
