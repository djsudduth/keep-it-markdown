# keep-it-markdown
Keep-it-markdown or KIM converts Google Keep notes to markdown using the unofficial Python Keep API.

The overall goal is to utilize Google Keep as an easy way to capture raw notes on all devices or additionally using the browswer plugin. Then, notes can be queried for export to markdown files directly into notetaking apps such as Obsidian or imported into Notion. 

## Installation
KIM is a command line script that requires Python 3.7 or greater and utilizes the unofficial gkeepapi. **NOTE: Warning! Be aware that this implies that Google could break the API at any time!!**

### Step 1: 
Install Python or Anaconda Python (there are plenty of tutorials online for installation instructions) on you PC or Mac. 

### Step 2: 
Download this project's zip file into any new directory of you choice. Select the 'Code' button on this page and 'Download ZIP'. Unzip the files within your chosen directory


### Step 3:
Start your command prompt, shell or terminal, find your download directory and run 
```bash
> pip install -r requirements.txt
```
This will install the additional libraries needed to run KIM.


### Step 4: 
Keep does not yet have an official API from Google. So, you must first test your Google account login with the Keep library and manually approve access with a browswer. From within your command prompt or shell and run 
```bash
> python keep-test.py
```
This will attempt a simple login using your Google ID and password. *NOTE: first time attempting to login will fail*. If you believe you typed in your Google account name and password correctly, copy and paste this URL into your browswer address bar and approve the request: 
https://accounts.google.com/DisplayUnlockCaptcha

Run the script again
```bash
> python keep-test.py
```
You should see a successful login with the statement -> "You've succesfully logged into Google Keep! Please try running Keep-it-Markdown or KIM!"

## Usage

Congrats! You can now run KIM. Simply start by running 
```bash
> python kim.py
```
This will execute your first query to export a note or set of notes as individual markdown files.

**NOTE: first time you execute, exported md files will be created in your KIM directory. This can be changed later**. 

For the first test, search for a keyword that returns only a few notes at most (you can do the search in Keep first to see how many notes will be returned by your search term).

Note: don't get confused by dashes in labels when looking at other notes. Dashes are added for label export to md files.
