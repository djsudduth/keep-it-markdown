# keep-it-markdown
Keep-it-markdown or KIM converts Google Keep notes to markdown using the unofficial Python Keep API without having to use Google Takeout to export notes first. The script will execute on Windows, MacOS or Linux.

The overall goal is to utilize Google Keep as an easy way to capture raw notes on all devices or additionally using the browswer plugin. Then, notes can be queried for export to markdown files directly into notetaking apps such as Obsidian, used with Typora or imported into Notion. 

## Installation
Install assumes you have some familiarity with running scripts through a terminal or command line. KIM is a command line script that requires Python 3.7 or greater and utilizes the unofficial gkeepapi. 

**NOTE: Be aware that 'unofficial' implies that Google could change the API at any time that might stop the script from working!**

#### Step 1: 
Install Python (there are plenty of tutorials online for installation instructions) on you PC or Mac. Start your command prompt, shell or terminal and verify your python version by running:
```bash
> python --version
```
If you had Python 2 installed already you may need to type 'python3' instead of just 'python' for the rest of these steps to use version 3.7+.

#### Step 2: 
Download this project's zip file into any new directory of you choice. Select the most current release noted at the top right of this page and download 'Source code' using this link:  
https://github.com/djsudduth/keep-it-markdown/releases

Unzip the files within your chosen directory.  

#### Step 3:
Start your command prompt, shell or terminal, find your download directory and run 
```bash
> pip install -r requirements.txt
```
(you may need to use 'pip3' instead of 'pip' if you have both python versions 2 and 3 installed) This will install the additional libraries needed to run KIM. You only need to do this once. If you have Anaconda as your Python base you may need to find tutorials on how to get pip and install dependencies. Advanced users may want to setup a virtual environment for this.

#### Step 4: 
Keep does not yet have an official API from Google. So, you must first test your Google account login with the Keep library and manually approve access with a browswer. From within your command prompt or shell and run 
```bash
> python keep-test.py
```
This will attempt a simple login using your Google ID and password. **NOTE: first time attempting to login may fail**. 

If you believe you typed in your Google account name and password correctly, copy and paste or click on this URL (https://accounts.google.com/DisplayUnlockCaptcha) into your browswer address bar and approve the request by pressing the 'Continue' button.

Run the script again
```bash
> python keep-test.py
```
If you entered your Google account id and password correctly, you should see a successful login with the statement -> "You've succesfully logged into Google Keep! Please try running Keep-it-Markdown or KIM!"

## Usage
Congrats! You can now run KIM. Simply start by running 
```bash
> python kim.py
```
After logging in you should see:
```bash
> Enter a keyword search, label search or '--all' for all notes to convert to Markdown or just press Enter to exit:
```

Entering a query term and pressing Enter will execute your first export of a note or set of notes as individual markdown files.

**NOTE: first time you execute, exported md files will be created in a default KIM sub-directory called 'mdfiles' within your install directory. This can be changed later**. 

For the first test, use a keyword query that returns and converts only a few notes at most (you can do the search in Keep first to see how many notes will be returned by your query/convert term).

You can convert to md by using a single word, a phrase or by a label. All queries to convert ignore notes in archive and trash. KIM will stay active to do more conversions until you just press enter or Ctrl-C.

### Using Settings
At first launch KIM will create a **settings.cfg** file in the directory where you chose to install KIM. You can modify these settings with a text editor:

**google_userid** = your-google-account-id (allows you to bypass typing in your id)  
**output_path** = path to where the output md files are created (if empty it is your install directory). Windows users use forward slashes, e.g. -> c:/md-files/export.

### Password Storage
When you run KIM for the first time it will store your Google password in your computer's safe storage (macOS - Keychain, Windows Credential Locker and Linux Secret Service or KWallet). You will not need to re-enter your password next time you run KIM.

If you need to change or reset your password, just run:
```bash
> python kim.py -r pw
```

### Key callouts
1. KIM does its best to convert unusual unicode characters where it can to keep the markdown clean but may have some issues with certain captured notes. If KIM crashes during conversion, try to isolate the problem note in Keep to see why it is causing issues.
2. All label spaces and special characters are hyphenated in conversion for proper tags. For example, if your Keep label is '#key topics', KIM will convert this to '#key-topics' or if it is '#mind*learning' KIM will convert to '#mind-learning' in the markdown file.
3. Note titles are truncated to 100 characters max.
4. Notes without Keep titles are given titles using the date-time of when the note was created. Notes with the same title will have the date-time appended on the original title when converted to not allow overwriting of each other.
5. If you have login errors after reboot or long idle periods you may need to re-approve KIM access through Step 4's URL - (https://accounts.google.com/DisplayUnlockCaptcha)
6. All notes are appended by their create date, update date and link back to the original Keep note.  
7. Both standard PNG and JPEG image files are supported. However, not all image types or non-standard formats may export properly. Any unknown types are saved with a .dat extension.

## Obsidian Use
Since KIM converts Google Keep notes to markdown, you can use some of the Obsidian text markdown features in your Keep notes as you're capturing information. For example, you can begin to cross-link notes in Keep by using the double-brackets within a note like this [[Title of another Keep note]]. Then, when you convert your notes to the Obsidian vault they will be automatically linked. This will also work for block references and other markdown notation. Most markdown types in Keep notes should convert successfully even if Keep cannot render them. **Do not try to add markdown for links or URLs in Keep**. KIM will try to map link URLs to markdown format for you.

However, KIM's goal is to be markdown compliant. Oddly, Obsidian does not use standard markdown formatting for images and links. Non-compliance makes reading markdown easier for Obsidian users but breaks in apps like Notion and Typora. Currently, a strict markdown is enforced in conversion except for images to be as compatible as possible.

## Notion Use
KIM markdown text exports seem to import into Notion successfully. However, Notion fails to import linked image attachments (which seems to be a general Notion md import problem at this time). Notion also ties underlying ids to any cross-linked notes so that there is no automated cross-linking when importing (future feature). Also, tags are not supported in Notion so Keep labels will just be text hashtags which are searchable.

## Typora Use
KIM tries to adhere to strict markdown to be as compatible as possible. However, Obsidian does not follow strict rules. To be compatible with both Typora and Obsidian, a non-compliant markdown image syntax is used. 

## Feature Todos
-[ ] Add Keep audio and drawing files  
-[ ] Use OAuth login to launch browser window and authenticate automatically  
-[ ] Build a simple installer  
-[ ] Create setup scripts for Windows, macOS and Linux  
-[ ] Tie Keep notes to Notion links for cross-linking of md imports  
-[ ] Email notes to Keep   
-[ ] Roam imports  
-[ ] Docker version  
-[ ] Add overwrite flag to replace notes

## Thank You
Thanks for trying this markdown converter! I hope you find it useful!
There's always room for improvement. Feel free to add issues to the issues list.

## 0.2.0 
- Added standard jpeg and png media file downloads
- Fixed ignore of archive and trash for label search
- Fixed compliant markdown of Keep note backlinks and images
- Added replace of em dash with 2 dashes
- Fixed conversion to tags of Keep labels with odd characters
