[![GitHub license](https://img.shields.io/github/license/djsudduth/keep-it-markdown)](https://github.com/djsudduth/keep-it-markdown/blob/main/LICENSE)

# keep-it-markdown
Keep-it-markdown or KIM converts Google Keep notes to markdown using the unofficial Python Keep API without having to use Google Takeout to export notes first. The script will execute on Windows, MacOS or Linux.

The overall goal is to utilize Google Keep as an easy way to capture raw notes on all devices or additionally using the browswer plugin. Then, notes can be queried for export to markdown files directly into notetaking apps such as Obsidian and/or Notion, or used directly with Typora. 

## Installation
Install assumes you have some familiarity with running scripts through a terminal or command line. KIM is a command line script that requires Python 3.7 or greater and utilizes the unofficial gkeepapi.

**NOTE: Be aware that 'unofficial' implies that Google could change the API at any time that might stop the script from working!**

You only need to run installation steps 1 through 4 one time.

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
 Keep does not yet have an official API from Google. So, you must first test your Google account login with the Keep library and manually approve access with a browswer. **Be sure you have logged into your primary Google account only in your default browser first before testing the Keep login.**  From within your command prompt or shell and run 
```bash
> python keep-test.py
```
This will attempt a simple login using your Google ID and password. **NOTE: first time attempting to login may fail**. 

If you believe you typed in your Google account name and password correctly and it failed, copy and paste or click on this URL (https://accounts.google.com/DisplayUnlockCaptcha) into your browswer address bar and approve the request by pressing the 'Continue' button.

Run the script again
```bash
> python keep-test.py
```
If you entered your Google account id and password correctly, you should see a successful login with the statement -> "You've succesfully logged into Google Keep! Please try running Keep-it-Markdown or KIM!"
**If this step keeps failing see 'Key Callouts' #10 below.**

## Usage
Congrats! You can now run KIM. Simply start by running 
```bash
> python kim.py
```
After logging in you should see:
```bash
> Enter a keyword search, label search or '--all' to convert Keep notes to md or '--x' to exit:
```

Entering a query term and pressing Enter will execute your first export of a note or set of notes as individual markdown files.

**NOTE: first time you execute, exported md files will be created in a default KIM sub-directory called 'mdfiles' within your install directory. Images are exported into 'media' within the default directory. This can be changed later**. 

For the first test, use a keyword query that returns and converts only a few notes at most (you can do the search in Keep first to see how many notes will be returned by your query/convert term).

You can convert to md by using a single word, a phrase or by a label. All queries to convert ignore notes in archive and trash. KIM will stay active to do more conversions until you just press --x or Ctrl-C.

### Using Settings
At first launch KIM will create a **settings.cfg** file in the directory where you chose to install KIM. You can modify these settings with a text editor:

**google_userid** = your-google-account-id (allows you to bypass typing in your id)  
**output_path** = path to where the output md files are created (if empty it is your install directory). Windows users use forward slashes, e.g. -> c:/md-files/export.

### Help and Options
All KIM options can be discovered using
```bash
> python kim.py --help
```
#### Labels
Searching for notes by labels just requires the # character in front of the search term like '#MyLabel'. On some operating systems like Linux you may need to enclose the term in quotes.

#### Overwriting
KIM by default does not overwrite markdown files when exporting, principally because Keep notes can have the same titles. KIM will try to rename duplicate notes. However, notes can be overwritten with
```bash
> python kim.py -o
```
all exported md files will be overwritten. However, if 2 or more Keep notes have the same name, the create date will be appended on the note to be unique.

#### Password Token Storage
When you run KIM for the first time and log in via your password, it will store your authenticated Google Keep token in your computer's safe storage (macOS - Keychain, Windows Credential Locker and Linux Secret Service or KWallet). You will not need to re-enter your password next time you run KIM.

If you need to change or reset your access token or don't feel comfortable saving the token in safe storage, just run KIM with the -r flag (NOTE: this has changed from version 0.2.0):
```bash
> python kim.py -r
```

#### Batch Mode
KIM can run through your own script by using the -b flag. For example, running:
```bash
> python kim.py -b 'my search term'
or
> python kim.py -b --all
```
will execute KIM without input prompts as long as you have your Google ID in the setting.cfg file and you have stored your Keep access token by running KIM once manually on your device. Be sure the -b flag is the last of all option flags when combining them.

#### Archive Notes
KIM has an option to export only Keep archive notes. All other note types are ignored with this option
```bash
> python kim.py -a
```
Archive export can be combined with the -o and -b options. 

#### Combinations
Example: to export all achived notes with overwriting in batch:
```bash
> python kim.py -a -o -b --all
```

### Key callouts
1. KIM does its best to convert unusual unicode characters where it can to keep the markdown clean but may have some issues with certain captured notes. If KIM crashes during conversion, try to isolate the problem note in Keep to see why it is causing issues.
2. All label spaces and special characters are hyphenated in conversion for proper tags. For example, if your Keep label is '#key topics', KIM will convert this to '#key-topics' or if it is '#mind*learning' KIM will convert to '#mind-learning' in the markdown file. Underscores are kept intact. Use the -p flag to preserve Keep labels as they are.
3. Note titles are truncated to 100 characters max.
4. Notes without Keep titles are given titles using the date-time of when the note was created. Notes with the same title will have the date-time appended on the original title when converted to not allow overwriting of each other. 
5. Running KIM repeatably without the overwrite option or clearing the output path without using a new path will continue to append date-time to the title of each exported note when it detects a note with the same title until it fails if the title is too long. 
6. If you have login errors after reboot or long idle periods you may need to re-approve KIM access through Step 4's URL - (https://accounts.google.com/DisplayUnlockCaptcha)
7. All notes' exported text are appended by their create date, update date and link back to the original Keep note.  
8. Both standard PNG and JPEG image files are supported. However, not all image types or non-standard formats may export properly. Drawings in Keep should download as PNG files.
9. Keep uses AAC files for audio recordings and are downloaded as M4A files. Most notes apps do not support AAC format. If you need markdown audio support you will have to manually convert the M4A files to MP3.
10. There seems to be login issues especially for Windows users due to older python libraries. Be sure to upgrade the gkeepapi to the latest version (**'pip install gkeepapi'**). If that doesn't work, find a Linux or Mac and run **'python keep-test.py -t'** which will display the token with the -t flag. Copy and save this master token in a safe and secure place!!. You can then use that token in KIM with **'python kim.py -t <your-token>'** which will save it in your keystore.

## Obsidian Use
Since KIM converts Google Keep notes to markdown, you can use some of the Obsidian text markdown features in your Keep notes as you're capturing information. For example, you can begin to cross-link notes in Keep by using the Wikilink double-brackets within a note like this [[Title of another Keep note]]. Then, when you convert your notes to the Obsidian vault they will be automatically linked. This will also work for block references and other markdown notation. Most markdown types in Keep notes should convert successfully even if Keep cannot render them. **Do not try to add markdown for links/URLs in Keep**. KIM will try to map link any of Keep's URLs to markdown format for you.

KIM's goal is to be markdown compliant. Obsidian uses Wikilinks by default. Obsidian can use strict markdown by setting the Options / Files & Links / Use [[Wikilinks]] to off. Currently, only strict markdown is enforced in KIM conversion to be as compatible as possible.

## Notion Use
KIM markdown text exports seem to import into Notion successfully. However, Notion fails to import linked image attachments (which seems to be a general Notion md import problem at this time). Notion also ties underlying ids to any cross-linked notes so that there is no automated cross-linking when importing (future feature). Also, tags are not supported in Notion so Keep labels will just be text hashtags which are searchable.

## Typora Use
KIM tries to adhere to strict markdown to be as compatible as possible.   No issues have been discovered using Typora on KIM markdown exports other than AAC audio support.

## Feature Todos
- [x] Add Keep audio and drawing files  
- [ ] Use OAuth login to launch browser window and authenticate automatically  
- [ ] Build a simple installer  
- [ ] Create setup scripts for Windows, macOS and Linux  
- [ ] Tie Keep notes to Notion links for cross-linking of md imports  
- [ ] Email notes to Keep   
- [ ] Roam imports  
- [ ] Docker version  
- [x] Add overwrite flag to replace notes
- [ ] Clean-up code from MVP

## Thank You
Thanks for trying this markdown converter! I hope you find it useful!
There's always room for improvement. Feel free to add issues to the issues list.

## 0.3.0 Changes
- Fixed overwriting the same keep notes if multiple exports or notes with the same title
- Fixed spaces in image link problem 
- Fixed multiple similar URL in the same note conversion issue  
- Fixed export of archived and trashed notes when using all command
- Fixed overwriting duplication on Keep notes with the same title
- Added audio file download to m4a format (not recognized in Obsidian yet)
- Added flag to overwrite exported markdown files
- Added flag to ignore saving Keep authentication token in the keystore
- Added flag to search and export only archived notes
- Added capability to run in batch with a script and search term
- Added help prompt 'kim.py --help'
- Added download of drawings

## 0.3.1 Changes
- Added foreign language support and fixed UTF-8 output
- Added flag to preserve Keep labels that have spaces and special characters
- Some MVP code cleanup


