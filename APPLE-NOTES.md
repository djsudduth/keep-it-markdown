## Apple Notes Conversion

### Overview
KIM can now export markdown files in a compatible format for Apple Notes import (OS versions 26.x). Apple Notes has issues
importing markdown files with media links unless the markdown and media are wrapped in a folder. A new switch has been added (`-an`) to export in this special format. Once exported from Keep using the `-an` option you must then use the "Import Markdown..." menu option in the Apple Notes UI to import them successfully. 

### Steps for Migrating to Apple Notes
  (be sure to run a test on a small set of notes first!)
- Run KIM (example `python kim.py -an -b #arthistory` or `python kim.py -an -cd "> 2026-01-01"`). Just be sure to use the `-an` option - see EXAMPLES.md
- Open Apple Notes in MacOS and select the "Import Markdown..." menu
- Find the folder where KIM exported your markdown files
- Select either the folders or files or both in the same directory where KIM exported - you do not need to drop into each markdown folder - just select the folders and/or files
- Run the import
- All markdown folder imports that have media will end up as notes in the current Apple Notes folder you have open at the time in the UI 
- All markdown simple files will end up in the Mac "Imported Notes" folder
- Once transferred, run this special Apple Shortcut (https://www.icloud.com/shortcuts/0be7572bb70c4f808a9e1c73a08e4dda) that will convert your Keep labels to Apple Notes tags (NOTE: the Shortcut may take a long time to run if you've imported a lot of Keep notes)

All media types should transfer (images, audios, and drawings). Reminders, formatted text and note colors do not transfer (reminder notes will transfer - just not the actual Tasks to Apple Reminders)