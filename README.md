# keep-it-markdown
Keep-it-markdown or KIM converts Google Keep notes to markdown using the unofficial Python Keep API.

The overall goal is to utilize Google Keep as an easy way to capture raw notes on all devices or additionally using the browswer plugin. Then, notes can be queried for export to markdown files directly into notetaking apps such as Obsidian or imported into Notion. 

## Installation
KIM is a command line script that requires Python 3.7 or greater and utilizes the unofficial gkeepapi. 

**NOTE: Warning! Be aware that 'unofficial' implies that Google could break the API at any time!!**

#### Step 1: 
Install Python (there are plenty of tutorials online for installation instructions) on you PC or Mac. 

#### Step 2: 
Download this project's zip file into any new directory of you choice. Select the 'Code' button on this page and 'Download ZIP'. Unzip the files within your chosen directory

#### Step 3:
Start your command prompt, shell or terminal, find your download directory and run 
```bash
> pip install -r requirements.txt
```
This will install the additional libraries needed to run KIM. You only need to do this once. If you have Anaconda as your Python base you may need to find tutorials on how to get pip and install dependencies. Advanced users will want to setup a virtual environment for this.

#### Step 4: 
Keep does not yet have an official API from Google. So, you must first test your Google account login with the Keep library and manually approve access with a browswer. From within your command prompt or shell and run 
```bash
> python keep-test.py
```
This will attempt a simple login using your Google ID and password. **NOTE: first time attempting to login will fail**. 

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
This will execute your first query to export a note or set of notes as individual markdown files.

**NOTE: first time you execute, exported md files will be created in your KIM directory. This can be changed later**. 

For the first test, search for a keyword that returns only a few notes at most (you can do the search in Keep first to see how many notes will be returned by your search term).

You can search by a single word, a phrase or by a label. All searches ignore notes in archive and trash. KIM will stay active to do more conversions until you just press enter or Ctrl-C.

### Using Settings
At first launch KIM will create a **settings.cfg** file in the directory where you chose to install KIM. You can modify these settings with a text editor:

**google_userid** = your-google-account-id (allows you to bypass typing in your id)  
**output_path** = path to where the output md files are created (if empty it is your install directory). Windows users use forward slashes, e.g. -> c:/md-files/export.

### Password Storage
When you run KIM for the first time it will store your Google password in your computer's safe storage (macOS - Keychain, Windows Credential Locker and Linux Secret Service or KWallet). You will not need to re-enter your password next time you run KIM. If you need to change or reset your password, just run:
```bash
> python kim.py -r pw
```

### Key callouts
1. KIM does its best to convert unusual unicode characters where it can to keep the markdown clean but may have some issues with certain captured notes. If KIM crashes during conversion, try to isolate the problem note in Keep to see why it is causing issues.
2. All label spaces are hyphenated in conversion for proper tags. For example, if your label is '#key topics', KIM will convert this to '#key-topics' in the markdown file.
3. Note titles are truncated to 100 characters max.
4. Notes without Keep titles are given titles using the date-time of when the note was created. Notes with the same title will have the date-time appended on the original title when converted to not allow overwriting of each other.
5. If you have login errors after reboot or long idle periods you may need to re-approve KIM access through Step 4's URL - (https://accounts.google.com/DisplayUnlockCaptcha)
6. All notes are appended by their create date, update date and link back to the original note.

## Obsidian Use
Since KIM converts Google Keep notes to markdown, you can use some of the Obsidian markdown features in your Keep notes as you're capturing information. For example, you can begin to cross-link notes in Keep by using the double-brackets within a note like this [[Title of another Keep note]]. 
Then, when you convert your notes to the Obsidian vault they will be automatically linked. This will also work for block references and other markdown notation. Most markdown types in Keep notes should convert successfully even if Keep cannot render them.

## Notion Use
KIM markdown exports seem to import into Notion successfully. However, Notion ties underlying ids to any cross-linked notes so that there is no automated cross-linking when importing (future feature). Also, tags are not supported in Notion so Keep labels will just be text hashtags in Notion which are searchable.


## Feature Todos
-[ ] Use OAuth login to launch browser window and authenticate automatically  
-[ ] Build a simple installer  
-[ ] Tie Keep notes to Notion links for cross-linking of md imports  
-[ ] Email notes to Keep   
-[ ] Roam imports  

