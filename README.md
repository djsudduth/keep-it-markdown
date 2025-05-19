[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/donsuddutha)  
[![GitHub license](https://img.shields.io/github/license/djsudduth/keep-it-markdown)](https://github.com/djsudduth/keep-it-markdown/blob/main/LICENSE)   
# keep-it-markdown
Keep-it-markdown or KIM converts Google Keep notes to markdown using the unofficial Python Keep API without having to use Google Takeout to export notes first. KIM can now also **import** markdown notes back to Keep. The script will execute on Windows, MacOS or Linux.

The overall goal is to utilize Google Keep as an easy way to capture raw notes on all devices or additionally using the browser plugin. Then, notes can be queried for export to markdown files directly into notetaking apps such as Obsidian, Logseq and/or Notion, or used directly with Typora. 

## Installation
**Advanced Users:** see the **INSTALL.md** to skip over these installation details for simple step-by-steps  

Install assumes you have some familiarity with running scripts through a terminal or command line. KIM is a command line script that **requires Python 3.10 or greater** and utilizes the unofficial gkeepapi. (**If you have Python versions 3.10+ and have login issues you may need to review Advanced Docker Setup below**)

**NOTE: Be aware that 'unofficial' implies that Google could change the API at any time that might stop the script from working!**

You only need to run installation steps 1 through 6 one time.

#### Step 1: 
Install Python (there are plenty of tutorials online for installation instructions) on you PC or Mac. If you have an older version of Python (3.8 or 3.9) installed and you want to leave it, you can install pyenv to run multiple versions. Start your command prompt, shell or terminal and verify your python version by running:
```bash
> python --version
```
If you had Python 2 installed already you may need to type 'python3' instead of just 'python' for the rest of these steps to use version 3.10+.

#### Step 2: 
Download this project's zip file into any new directory of you choice. Select the most current release noted at the top right of this page and download 'Source code' using this link:  
https://github.com/djsudduth/keep-it-markdown/releases

Unzip the files within your chosen directory.

#### Step 3:
Make sure you are in your KIM directory and install all needed dependencies with:  
```bash
> pip install -r requirements.txt
```
(you may need to use 'pip3' instead of 'pip' if you have both python versions 2 and 3 installed) This will install the additional libraries needed to run KIM. You only need to do this once. If you have Anaconda as your Python base you may need to find tutorials on how to get pip and install dependencies. Advanced users may want to setup a virtual environment for this.

#### Step 4:
KIM requires a Google Keep authentication token in order to run. The token can only be retrieved once you have a Google page OAuth cookie. Install the Chrome extension called 'Cookie Tab Viewer'. Change the directory to where you installed KIM.  

Here's the tricky part - you need to get your OAuth token from a Google cookie. To get the OAuth token - follow the **"Second way"** instructions here (but get the cookie value using the Chrome extension once you've pressed "I agree" on the Google page in the Second way method):
https://github.com/rukins/gpsoauth-java?tab=readme-ov-file  

Copy the cookie called `oauth_token` using the Chrome Cookie Tab Viewer from the cookies in your local browser. Then, run the script
```bash
> python get_token.py
```
You will be prompted for your Google email account name, OAuth token, and Android ID

The AndroidID can just be a random value like: `abcdef123`  

So, when you get the prompt when running the script:  
**Email:** your google ID  
**OAuth Token:** oauth2_4/......rest of token  
**Android ID:** abcdef123  

The Keep token should be displayed - it should look like:  
"aas_et/FKcp.............lots of characters.....................BjQ="  

Copy that token and save it in a safe place! If it didn't work your OAuth token may have expired (takes about 5 min to expire). Run this step again until you get the token.  

#### Step 5: 
You now need to save your Keep token within the KIM secure keyring
```bash
> python kim.py -t <your long token value here>
```
If you entered your Google email and token correctly, you should see a successful login with the statement -> "You've succesfully logged into Google Keep!"

**If this step keeps failing see 'Key Callouts' #9 below, and have issues with the login - see Advanced Docker Setup below**

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
Also see **EXAMPLES.md** for many option combinations  

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

#### Preserve Labels 
Many markdown applications cannot work with special characters in labels/tags (such as brackets, parentheses, asterisks, etc). By default, KIM will strip out all special characters and replace them with dashes(-). If you need to preserve labels in their original form, use the -p option:
```bash
> python kim.py -p
```

#### Logseq Style 
Some markdown systems prefer to have bullets prepended on each paragraph within a note. KIM will attempt to prepend a dash to any Keep note that has 2 linefeeds as well as the first line. You can enable this feature with
```bash
> python kim.py -l
```

#### Joplin Front Matter 
Joplin tags do not use the hashtag format. They are provided as front matter comments within the notes. With this switch KIM will prepend notes with the Joplin front matter comments to preserve tags and dates. You can enable this feature with
```bash
> python kim.py -j
```

#### Filter by Create or Edit Date 
KIM now supports filtering your export by either the created date (`-cd`) or edited date (`-ed`). This can be combined with the other options to export notes only after or before specific dates. Only the greater-than `>` or less-than `<` filters are available. You must provide the `<`|`>` preceeding the date. The date must be in the form `YYYY-MM-DD`. For example, you can filter on any notes created before Dec 9, 2022 with:
```bash
> python kim.py -cd "< 2022-12-09"
```
Or, you can filter on any notes edited after Oct 31, 2023 with:
```bash
> python kim.py -ed "> 2023-10-31"
```
(Note that Linux users my have to use single quotes)

#### Move Notes to Archive After Export  
**CAUTION! This is the only switch that alters your notes - even if it just an attribute change. Be sure to backup your Keep notes to Google Takeout before using this option!!**  
If you have a large number of notes it can be confusing which ones have already been exported. With this switch any exported notes will be moved to the Keep archive. You can enable this feature with
```bash
> python kim.py -m
```

#### Batch Mode
KIM can run through your own script by using the -b flag. For example, running:
```bash
> python kim.py -b 'my search term'
or
> python kim.py -b --all
```
will execute KIM without input prompts as long as you have your Google ID in the setting.cfg file and you have stored your Keep access token by running KIM once manually on your device. Be sure the -b flag is the last of all option flags when combining them.

#### Silent Mode
KIM can suppress any screen prompts or status messages using the -q flag. Silent or quiet mode will pipe all output to at file called `kim.log` in the install diretory. This is useful for batch mode execution. You must have `settings.cfg` setup with your google id so the user prompt will not display.  This works both for exporting and importing:
```bash
> python kim.py -q -b '#mylabel'
```

#### Remove Duplicate Labels/Hashtags
KIM by default appends labels as hashtags at the end of notes. However, Keep can create labels either from the menu or by using hashtags embedded within the note text. KIM can remove any duplicate tags at the end of exported notes using the -d flag. This will allow in-line tags in notes so that apps like Obsidian and Logseq won't have duplicates appended:
```bash
> python kim.py -d
```
**NOTE: If you've used inline hashtagging within notes that have unusual characters, this option will not modify the hashtag within the note. Use the -p option to preserve labels and hashtags in their original form without modification**

#### Archive Notes
KIM has an option to export only Keep archive notes. All other note types are ignored with this option
```bash
> python kim.py -a
```
Archive export can be combined with the -o and -b options. 

#### Convert to Wikilinks
KIM has an option to modify pre-existing Keep note-to-note links that are in markdown format such as `[Other Keep Note](https://keep.google.com/#NOTE/dks7r23ksdf...UI9kshweriuhv)` to just `[[Other Keep Note]]`
```bash
> python kim.py -w
```
This is very useful if you're using the *Markdown for Google Keep* plugin and want Wikilinks for note-to-note link in Obsidian or Joplin. 

#### Import Notes - (WARNING - GOOGLE RATE LIMITS)
KIM supports importing markdown note files back into Keep using 
```bash
> python kim.py -i
```
**WARNING! Google may lock you out of your account if you attempt to import more than a couple hundred files - use caution!**

There are a number of restrictions for importing. First, KIM will only import files from a single directory (no subdirectories) and they must have either a .txt or .md extension (both can be mixed in the import folder). KIM does not support importing any media (images/audio) at this point. Additionally, KIM will not scan files for tags/labels or create new ones. The file create date and update date will be appended to the note (**Windows users note** - if you copy markdown files to a new directory, the create date will reflect the current date rather than the file's original create date - unless you use Robocopy). Only existing labels can be used.

To add the path and desired labels for import in **settings.cfg**, add or update these two additional settings:  
**input_path** = path to where the input md files are located. Windows users use forward slashes, e.g. -> c:/md-files/import  
**input_labels** = a list of one or more comma delimited labels without the # leading character - e.g. -> computers, programming (this will tag all of the imported notes with both labels 'computers' and 'programming' within that import directory as long as you have those labels predefined within Keep already)

You can override the settings `input_labels` in the command line with the (-lb) parameter - example:
```bash
> python kim.py -i -lb "computers,programming"
```

NOTE: the import switches -i and -lb are incompatible with all other switches for export. Be sure to test simple import examples before using this feature!!! 

#### Authentication Token Storage
When you run KIM for the first time and log in via your password, it will store your authenticated Google Keep token in your computer's safe storage (macOS - Keychain, Windows Credential Locker and Linux Secret Service or KWallet). You will not need to re-enter your password next time you run KIM.

If you need to change or reset your access token or don't feel comfortable saving the token in safe storage, just run KIM with the -r flag (NOTE: this has changed from version 0.2.0):
```bash
> python kim.py -r
```

#### Combinations
Example: to export all non-archived notes, using content for blank note titles, with overwriting, preserving Keep label format, Logseq style paragraphs, removing trailing labels if hashtags are embedded in note, with create dates > Oct 3, 2023 in batch:
```bash
> python kim.py -c -o -p -l -d -cd "> 2023-10-03" -b --all
```
Note: skip -s and overwrite -o cannot be used at the same time

### Key callouts
1. KIM does its best to convert unusual unicode characters where it can to keep the markdown clean but may have some issues with certain captured notes. If KIM crashes during conversion, try to isolate the problem note in Keep to see why it is causing issues.
2. All label spaces and special characters are hyphenated in conversion for proper tags. For example, if your Keep label is '#key topics', KIM will convert this to '#key-topics' or if it is '#mind*learning' KIM will convert to '#mind-learning' in the markdown file. Underscores are kept intact. Use the `-p` flag to override this and preserve Keep labels as they are.
3. Note titles are truncated to 100 characters max.
4. Notes without Keep titles are given titles using the date-time of when the note was created unless the `-c` flag is used. Notes with the same title will have the date-time appended on the original title when converted to not allow overwriting of each other unless the overwrite flag is set. 
5. Running KIM repeatably without the skip or overwrite options or clearing the output path without using a new path will continue to append date-time to the title of each exported note when it detects a note with the same title until it fails if the title is too long. 
6. All notes' exported text are appended by their create date, update date and URL link back to the original Keep note.  
7. Both standard PNG and JPEG image files are supported. However, not all image types or non-standard formats may export properly. Drawings in Keep should download as PNG files.
8. Keep uses AAC format for audio recordings. When notes are downloaded the audio is saved as M4A files. It is not known if this format will work on all markdown applications.
9. It is possible there can be login issues due to some of the authentication and security library changes with Google and Python. If there are issues, use the Advanced Docker Setup in the next section.

## Advanced Docker Setup
If you are having difficulty logging in to Google you can use Docker with the preconfigured OS and Python version to access KIM and save your exported notes (see alternative step 12 if you want to save the Keep token on your PC).

**Steps:**
1) Install Docker on any PC (find the online instructions for your particular operating system)
2) Startup Docker (or it will autostart on reboot depending on how you installed it)
3) Go to the command line and run ``docker build -t kim .`` in the directory where you installed KIM (it will take about 5 min to create the image)
4) Run the Docker image with ``docker run --mount type=bind,source=(your PC's KIM directory)/mdfiles,target=/keep-it-markdown-0.6.7/mdfiles -it kim`` (you will be automatically logged into the Docker image and your PC's directory will be mapped to the Docker image directory)
5) Change the directory to Kim ``cd keep-it-markdown-0.6.7``  
6) Follow **Second Way** instructions here to get a copy of the oauth_token cookie value - https://github.com/rukins/gpsoauth-java?tab=readme-ov-file
7) Run the script in the KIM directory - `python get_token.py`
8) Enter your Google email account name, oauth_token, and Android ID when prompted (Android ID can be anything, OAuth token expires in about 5 min)
9) Copy and save the Keep Token value output from `get_token.py` on your PC
---
10) For one time or sporatic use, run KIM in Docker with ``python kim.py -t <long token here>`` using the saved Token above (note that in Docker python3 is aliased to python) - your exported notes will be exported to your PC. NOTE, however, that running Docker this way will not save any passwords or exported notes when you exit and you will need use the saved Token each time you use KIM with Docker this way.(Exit the Docker image with ``exit``)
---
11) Alternatively, exit the Docker image with ``exit``
12) Download and install KIM in your current OS
13) Install KIM dependencies your PC using `pip install -r requirements.txt`
14) Run KIM with the `-t` switch once to save the Token in your PC keystore (``python kim.py -t <long token here>``)
15) You can now run KIM on your PC (once you save the token) with Python v-3.10 or higher without having to run these steps again. The Token will be saved in your local PC's keystore

## Obsidian Use
Since KIM converts Google Keep notes to markdown, you can use some of the Obsidian text markdown features in your Keep notes as you're capturing information. For example, you can begin to cross-link notes in Keep by using the Wikilink double-brackets within a note like this `[[Title of another Keep note]]`. You can also cross-link notes in Keep like `[Other Note](https://keep.google.com/#NOTE/....)` and use the `-w` option to convert note-to-note links like this to wikilinks. Then, when you convert your notes to the Obsidian vault they will be automatically linked. This will also work for block references and other markdown notation. Most markdown types in Keep notes should convert successfully even if Keep cannot render them. KIM will try to map link any of Keep's URLs to markdown format for you or ignore markdown hyperlinks if they are already in the note.

## Logseq Use
Notes will import into Logseq similar to the Obsidian Use description, however, you need to set your mdfiles path to the `pages` folder in Logseq. For images to render properly be sure to set your media path to `../assets`. Also, to format notes correctly, a switch has been configured (`-l`) to add paragraph bullets within each exported note so Logseq will render them better. Also, namespaces are supported by using the `/` character in Keep titles (example a Keep note title of "Journal/2024-May" will export to "Journal___2024-May.md" - when opened in Logseq the namespace will be "Journal/2024-May").

## Notion Use
KIM markdown note exports seem to import into Notion successfully. However, Notion STILL fails to import linked image attachments (which seems to be a general Notion md import problem at this time). Notion also ties underlying ids to any cross-linked notes so that there is no automated cross-linking when importing (future feature). Also, tags are not supported in Notion so Keep labels will just be text hashtags within the note which are searchable.

## Joplin Use
KIM markdown note exports also import very well into Joplin. Using the `-j` flag will add Keep labels as **Joplin front matter** to add them automatically as tags. Most markdown types in Keep notes should convert successfully even if Keep cannot render them. For example, you can begin to cross-link notes in Keep by using the Wikilink double-brackets within a note like this `[[Title of another Keep note]]`. If you have full markdown note-to-note links in Keep like `[Other Note](https://keep.google.com/#NOTE/....)`, add the `-w` flag to convert those to Wikilinks. Wikilinking between Keep notes will automatically convert to standard Joplin markdown note links connecting notes together.

## Typora Use
KIM tries to adhere to strict markdown to be as compatible as possible.   No issues have been discovered using Typora on KIM markdown exports.


## Thank You
Thanks for trying this markdown converter! I hope you find it useful!
There's always room for improvement. Feel free to add questions or issues to the issues list.


