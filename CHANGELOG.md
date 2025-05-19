# Changelog

## 0.6.7 Release (05/15/2025)
- Added ability to import both markdown and text files from the import folder
- Added `-lb`option to provide comma delimited labels/tags in the cli for import  
- Added creation and validation of both the import and import-completed folders on launch
- Added `-q` option for quiet/silent mode when importing or exporting notes
- Added `-d` option to remove duplicate tags at the end of notes if already embedded in the note text
- Fixed audio file extension error for Android mp3 audio types vs Apple m4a audio
- Cleaned up cli structure

## 0.6.6 Release (N/A - reverted)

## 0.6.5 Release (10/30/2024)
- Added support for the *Markdown for Google Keep* plugin - ignore of any pre-existing markdown web links in notes and Keep note-to-note linking relative urls  
- Added `-w` option to convert pre-existing Keep note-to-note markdown links to wikilinks during export  
- Filter exported notes by create (`-cd`) or edit date (`-ed`) ( < or > date only)  
- Fixed exported notes update date bug to be the actual edited date vs. internal Google update date  
- Added warning on importing too many markdown notes may lock user out of Keep  
- Added EXAMPLES.md for command line examples using option switches  
- Added ability to export namespaces with '/' character in filenames for Logseq and Joplin  
- Removed old python formatting yapf settings  

## 0.6.3|0.6.4 Release (9/16/2024)
- Fixed the Dockerfile versions    

## 0.6.2 Release (9/15/2024)
- Fixed the keep.resume warning message for newer gkeepapi version >= 0.16.0  
- Fixed the Python 3.12+ regular expression error  
- Added more detail error message if KIM fails to execute  

## 0.6.1 Release (5/26/2024)
- New instructions and Dockerfile for updated versions of gkeepapi and gpsoauth to get keep token  
- Wikilinking now supported for Joplin notes  

## 0.6.0 Release (1/28/2024)
- Now requires Python v-3.10+ to run KIM  
- New Docker image to get the Keep token  
- Old keep-test.py module removed for new Google authentication (get_token.py added)  
- New simple INSTALL.md steps

## 0.5.4 Release (1/14/2024)
- Docker image altered to use Ubuntu:22.04 to fix Google auth issues with gkeepapi  
- Added new flag -m to move exported images to Archive folder  
- Removed python deprecated imghdr library with pillow module  

## 0.5.3 Release (11/5/2023)
- Docker image creation and use  
- Removed captcha note in keep-test.py  

## 0.5.2 Release (7/12/2023)
- Switched audio file extensions from AAC back to M4A  
- Added Joplin exports -j flag to use front matter header  
- Removed first dash on list notes exported to Logseq with -l switch  

## 0.5.1 Release (6/28/2023)
- Fixed image overwrite if note has no title or text and using -c switch  
- Fixed error of markdown note imports if there are special characters within  
- Added create and update dates of markdown files to imported notes  

## 0.5.0 Release (2/4/2023)
This update is a major refactor of the previous versions. Updates include:  
- Faster export  
- Added Logseq switch to add bullets to exported Keep notes  
- Added simple import option to upload markdown files back to Keep  
- Removed microseconds from note create and update dates  
- Fixed null image bug  
