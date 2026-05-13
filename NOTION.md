## Notion Conversion

### Overview
KIM can now export markdown files in a compatible format for Notion import. Notion has issues importing markdown
files with media links unless the markdown and media are wrapped into a zip file. A new switch has been added (`-no`) to export in this special format. Once exported from Keep using the `-no` option you must then use the "Settins / Import..." menu option in the Notion UI to import the ZIP file successfully. 

### Steps for Migrating to Notion
  (be sure to run a test on a small set of notes first!)
- Run KIM (example `python kim.py -no -b #arthistory` or `python kim.py -no -cd "> 2026-01-01"`). Just be sure to use the `-no` option - see EXAMPLES.md

### Finish later for 0.7.0 
- Open Apple Notes in MacOS and select the "Import Markdown..." menu
- Find the folder where KIM exported your markdown files
- Select either the folders or files or both in the same directory where KIM exported - you do not need to drop into each markdown folder - just select the folders and/or files
- Run the import
- All markdown folder imports that have media will end up as notes in the current Apple Notes folder you have open at the time in the UI 
- All markdown simple files will end up in the Mac "Imported Notes" folder
- Once transferred, run this special Apple Shortcut (https://www.icloud.com/shortcuts/0be7572bb70c4f808a9e1c73a08e4dda) that will convert your Keep labels to Apple Notes tags (NOTE: the Shortcut may take a long time to run if you've imported a lot of Keep notes)

If you want to export all your notes (run both `python kim.py -an -d -b --all` and `python kim.py -an -d -a -b --all` to export both active and archive (`-a`) notes). The `-d` option removes duplicate labels in notes - e.g., if you have both #mytag in the note and the label 'mytag' as well.

All media types should transfer (images, audios, and drawings). Reminders, formatted text and note colors do not transfer (reminder notes will transfer - just not the actual Tasks to Apple Reminders)