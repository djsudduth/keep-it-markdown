[![GitHub license](https://img.shields.io/github/license/djsudduth/keep-it-markdown)](https://github.com/djsudduth/keep-it-markdown/blob/main/LICENSE)

# keep-it-markdown
Keep-it-markdown or KIM converts Google Keep notes to markdown using the unofficial Python Keep API without having to use Google Takeout to export notes first. KIM can now also **import** markdown notes back to Keep. The script will execute on Windows, MacOS or Linux.

The overall goal is to utilize Google Keep as an easy way to capture raw notes on all devices or additionally using the browser plugin. Then, notes can be queried for export to markdown files directly into notetaking apps such as Obsidian, Logseq and/or Notion, or used directly with Typora. 

## Installation
Install assumes you have some familiarity with running scripts through a terminal or command line. KIM is a command line script that **requires Python 3.8 or greater** and utilizes the unofficial gkeepapi. (**If you have Python versions 3.10+ and have login issues you may need to review Advanced Docker Setup below**)

**NOTE: Be aware that 'unofficial' implies that Google could change the API at any time that might stop the script from working!**

You only need to run installation steps 1 through 4 one time.

#### Step 1: 
Install Python (there are plenty of tutorials online for installation instructions) on you PC or Mac. Start your command prompt, shell or terminal and verify your python version by running:
```bash
> python --version
```
If you had Python 2 installed already you may need to type 'python3' instead of just 'python' for the rest of these steps to use version 3.8+.

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
This script was written before the official Google Keep API was available. The Google Keep API is currently only available to workspace users and not individuals. So, you must manually create an application password for authentication purposes. 

1) Navigate to your [Google Account Page](https://myaccount.google.com)
2) Click on the Security option on the left
3) Under the **Signing in to Google** header select **App passwords**
4) Choose **Select App** and select **Other**, the name can be anything you want but I suggest something identifiable such as "**KeepItMarkdown**"
5) Click on Generate and Copy the password that's generated
6) Run the following command and logon with your Google email and the newly generated application password. 
```bash
> python kim.py
```
If you entered your Google email and application password correctly, you should see a successful login with the statement -> "You've succesfully logged into Google Keep!"

**If this step keeps failing see 'Key Callouts' #9 below, or, if you are using Python 3.10 or greater and have issues with the login - see Advanced Docker Setup below or read this note: https://github.com/djsudduth/keep-it-markdown/issues/72**

## Usage
Congrats! You can now run KIM. Simply start by running:  
```bash
> python kim.py
```
After logging in you should see:
```bash
> Enter a keyword search, label search or '--all' to convert Keep notes to md or '--x' to exit:
```

Entering a query term and pressing Enter will execute your first export of a note or set of notes as individual markdown files from your active note list.

**NOTE: first time you execute, exported md files will be created in a default KIM sub-directory called 'mdfiles' within your install directory. Images are exported into 'media' within the default directory. This can be changed later**. 

For the first test, use a keyword query that returns and converts only a few notes at most (you can do the search in Keep first to see how many notes will be returned by your query/convert term).

You can convert to md by using a single word, a phrase or by a label. **All queries to convert ignore notes in archive and trash unless you use the option flags below**. KIM will stay active to do more conversions until you just press --x or Ctrl-C.

### Using Settings
At first launch KIM will create a **settings.cfg** file in the directory where you chose to install KIM. You can modify these settings with a text editor:

**google_userid** = your-google-account-id (allows you to bypass typing in your id)  
**output_path** = path to where the output md files are created (if empty it is your install directory). Windows users use forward slashes, e.g. -> c:/md-files/export.
**media_path** = location of the exported media files (images, audio) relative to your output_path. If the output_path is /mdexport and media_path is media/data, the media full path will be /mdexport/media/data. Media paths cannot start with /, mount or drive letter.

(For import settings, see the -i switch below)

### Help and Options
All KIM options can be discovered using
```bash
> python kim.py --help
```
#### Labels
Searching for notes by labels just requires the # character in front of the search term like '#MyLabel'. On some operating systems like Linux you may need to enclose the term in quotes.

#### Titles
Exported note titles use Keep titles in conversion as best it can. In many cases Keep notes do not have titles and by default KIM will use the create date-time as the title. If you wish to use the beginning body content for blank Keep titles use
```bash
> python kim.py -c
```
if the note has no title or text in the body then the date will be used as default.

#### Overwriting or Skipping
KIM by default does not overwrite markdown files when exporting, principally because Keep notes can have the same titles. KIM will try to rename duplicate notes. However, notes can be overwritten with
```bash
> python kim.py -o
```
all exported md files will be overwritten. However, if 2 or more Keep notes have the same title, the create date will be appended on the note to be unique.

If you want to skip or ignore notes that have already been exported then
```bash
> python kim.py -s
```
will skip exporting Keep notes to markdown that already exist in the destination directory. If 2 or more Keep notes have the same title and a markdown file already exists with that name, a new export will be created for any exports that do not exist. (Note that overwrite and skip cannot be used at the same time)

#### Logseq Style (Experimental!)
Some markdown systems prefer to have bullets prepended on each paragraph within a note. KIM will attempt to prepend a dash to any Keep note that has 2 linefeeds as well as the first line. You can enable this feature with
```bash
> python kim.py -l
```

#### Joplin Front Matter 
Joplin tags do not use the hashtag format. They are provided as front matter comments within the notes. With this switch KIM will prepend notes with the Joplin front matter comments to preserve tags and dates. You can enable this feature with
```bash
> python kim.py -j
```

#### Move Notes to Archive After Export  
**CAUTION! This is the only switch that alters your notes - even if it just an attribute change. Be sure to backup your Keep notes to Google Takeout before using this option!!**  
If you have a large number of notes it can be confusing which ones have already been exported. With this switch any exported notes will be moved to the Keep archive. You can enable this feature with
```bash
> python kim.py -m
```

#### Authentication Token Storage
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

#### Import Notes - EXPERIMENTAL
KIM now supports importing markdown note files back into Keep using 
```bash
> python kim.py -i
```
There are a number of restrictions for importing. First, KIM will only import files within a single directory (no subdirectories) and they must have an .md extension. KIM does not support importing any media (images/audio) at this point. Additionally, KIM will not scan files for tags/labels or create new ones. The file create date and update date will be appended to the note (**Windows users note** - if you copy markdown files to a new directory, the create date will reflect the current date rather than the file's original create date - unless you use Robocopy). Only existing labels can be used and those must be setup in the **settings.cfg** file.

To add the path and desired labels for import in **settings.cfg**, add or update these two additional settings:  
**input_path** = path to where the input md files are located. Windows users use forward slashes, e.g. -> c:/md-files/import  
**input_labels** = a list of one or more comma delimited labels without the # leading character - e.g. -> computers, programming (this will tag all of the imported notes with both labels 'computers' and 'programming' within that import directory as long as you have those labels predefined within Keep already)

NOTE: the import switch -i is incompatible with all other switches for export. Be sure to test simple import examples before using this feature!!! 

#### Combinations
Example: to export all achived notes, using content for blank note titles, with overwriting, preserving Keep label format and logseq style paragraphs in batch:
```bash
> python kim.py -a -c -o -p -l -b --all
```
Note: skip -s and overwrite -o cannot be used at the same time

### Key callouts
1. KIM does its best to convert unusual unicode characters where it can to keep the markdown clean but may have some issues with certain captured notes. If KIM crashes during conversion, try to isolate the problem note in Keep to see why it is causing issues.
2. All label spaces and special characters are hyphenated in conversion for proper tags. For example, if your Keep label is '#key topics', KIM will convert this to '#key-topics' or if it is '#mind*learning' KIM will convert to '#mind-learning' in the markdown file. Underscores are kept intact. Use the -p flag to override this and preserve Keep labels as they are.
3. Note titles are truncated to 100 characters max.
4. Notes without Keep titles are given titles using the date-time of when the note was created unless the -c flag is used. Notes with the same title will have the date-time appended on the original title when converted to not allow overwriting of each other unless the overwrite flag is set. 
5. Running KIM repeatably without the skip or overwrite options or clearing the output path without using a new path will continue to append date-time to the title of each exported note when it detects a note with the same title until it fails if the title is too long. 
6. All notes' exported text are appended by their create date, update date and URL link back to the original Keep note.  
7. Both standard PNG and JPEG image files are supported. However, not all image types or non-standard formats may export properly. Drawings in Keep should download as PNG files.
8. Keep uses AAC format for audio recordings. When notes are downloaded the audio is saved as M4A files. It is not known if this format will work on all markdown applications.
9. There seems to be login issues due to some of the authentication and security library changes with Google and Python. Take a look at this note -> https://github.com/djsudduth/keep-it-markdown/issues/72 or use the Advanced Docker Setup in the next section

## Advanced Docker Setup
If you are having difficulty logging in to Google you can use Docker with the preconfigured OS and Python version to access KIM and save your exported notes (see alternative step 7 if you want to save the Keep token on your PC).

**Steps:**
1) Install Docker on any PC (find the online instructions for your particular operating system)
2) Startup Docker (or it will autostart on reboot depending on how you installed it)
3) Go to the command line and run ``docker build -t kim .`` in the directory where you installed KIM (it will take about 5 min to create the image)
4) Run the Docker image with ``docker run --mount type=bind,source=(your PC's KIM directory)/mdfiles,target=/keep-it-markdown-0.5.4/mdfiles -it kim`` (you will be automatically logged into the Docker image and your PC's directory will be mapped to the Docker image directory)
5) Change the directory to Kim ``cd keep-it-markdown-0.5.4``
6) Create a temporary app password on Google
---
7) For one time or sporatic use, run KIM per the instructions above (note that in Docker python3 is aliased to python) - your exported notes will be exported to your PC. NOTE, however, that running Docker this way will not save any passwords or exported notes when you exit and you may need to recreate Google app passwords each time you use KIM with Docker this way.(Exit the Docker image with ``exit``)
---
7) Alternatively, run ``python keep-test.py -t`` in the Docker image to log in and display the Keep token (keep token will **appear be very long** - almost 2 lines)
8) Copy the token by highlighting the entire string and hitting enter
9) Paste and save the token somewhere safe
10) Exit the Docker image with ``exit``
11) Now run KIM in your current OS with the -t switch once to save it in the keystore (``python kim.py -t <long token here>`` - you may need a new Google app password to do this)
12) You can now run KIM on any PC (once you save the token) with Python v-3.8 or higher

## Obsidian Use
Since KIM converts Google Keep notes to markdown, you can use some of the Obsidian text markdown features in your Keep notes as you're capturing information. For example, you can begin to cross-link notes in Keep by using the Wikilink double-brackets within a note like this [[Title of another Keep note]]. Then, when you convert your notes to the Obsidian vault they will be automatically linked. This will also work for block references and other markdown notation. Most markdown types in Keep notes should convert successfully even if Keep cannot render them. **Do not try to add markdown for links/URLs in Keep**. KIM will try to map link any of Keep's URLs to markdown format for you.

KIM's goal is to be markdown compliant. Obsidian uses Wikilinks by default. Obsidian can use strict markdown by setting the Options / Files & Links / Use [[Wikilinks]] to off. Currently, only strict markdown is enforced in KIM conversion to be as compatible as possible.

## Logseq Use
Notes will import into Logseq similar to the Obsidian Use description, however, you need to set your mdfiles path to the `pages` folder in Logseq. For images to render properly be sure to set your media path to `../assets`. Also, to format notes correctly, an experimental feature has been added. A new switch has been configured (-l) to add paragraph bullets within each exported note so Logseq will render them better. Deep testing was not done on this option.

## Notion Use
KIM markdown note exports seem to import into Notion successfully. However, Notion STILL fails to import linked image attachments (which seems to be a general Notion md import problem at this time). Notion also ties underlying ids to any cross-linked notes so that there is no automated cross-linking when importing (future feature). Also, tags are not supported in Notion so Keep labels will just be text hashtags within the note which are searchable.

## Joplin Use
KIM markdown note exports also import very well into Joplin. Using the -j flag will add Keep labels as Joplin front matter to add them as tags. Most markdown types in Keep notes should convert successfully even if Keep cannot render them. However, wikilinks are not supported in Joplin's manual markdown import and front matter tags are not supported on import.

## Typora Use
KIM tries to adhere to strict markdown to be as compatible as possible.   No issues have been discovered using Typora on KIM markdown exports.

## Feature Todos
- [x] Add Keep audio and drawing files  
- [x] Add overwrite flag to replace notes
- [x] Clean-up code from MVP
- [ ] Export from Google Takeout Keep backups
- [ ] Build a simple installer  
- [ ] Create setup scripts for Windows, macOS and Linux  
- [ ] Tie Keep notes to Notion links for cross-linking of md imports  
- [ ] Email notes to Keep   
- [ ] Roam imports  
- [x] Docker version  


## Thank You
Thanks for trying this markdown converter! I hope you find it useful!
There's always room for improvement. Feel free to add issues to the issues list.


## 0.5.1 Recent Changes
Fixed image overwrite if note has no title or text and using -c switch  
Fixed error of markdown note imports if there are special characters within  
Added create and update dates of markdown files to imported notes  

## 0.5.2 Recent Changes
Switched audio file extensions from AAC back to M4A  
Added Joplin exports -j flag to use front matter header  
Removed first dash on list notes exported to Logseq with -l switch  

## 0.5.3 Recent Changes
Docker image creation and use  
Removed captcha note in keep-test.py  

## 0.5.4 Recent Changes
Docker image altered to use Ubuntu:22.04 to fix Google auth issues with gkeepapi  
Added new flag -m to move exported images to Archive folder  
Removed python deprecated imghdr library with pillow module  