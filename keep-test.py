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
    gkeepapi.node.DEBUG = True
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
        print (
            "If you still have issues logging in then you may need " \
            + "to try 1 of 5 possible solutions:\n \
            1) recreate the Google app password to make sure it is valid and try again\n \
            2) find an PC with an older version of an OS (Windows 10 or Debian 11) with Python v3.8 or 3.9\n \
            3) install pyenv to allow for multiple versions of Python - try with Python 3.9.x\n \
            4) create a virtual machine with VirtualBox or other virtualization software and install an older OS\n \
            5) install Docker and run the Docker image in Advanced setup"
            )

   


if __name__ == '__main__':
    main(sys.argv)
