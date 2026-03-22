## Apple Notes Conversion

### Overview
KIM can now export markdown files in a compatible format for Apple Notes import (OS versions 26.x). Apple Notes has issues
importing markdown files with media link unless the markdown and media are wrapped in a folder. A new switch has been added (`-an`) to export in this special format. Once exported from Keep using the `-an` option you must then use the "Import Markdown..." menu option in the Apple Notes UI to import them successfully. 

### Steps for Migrating to Apple Notes
- Run KIM (example `python kim.py -an -b #arthistory` or `python kim.py -an -cd "> 2026-01-01"`) - see EXAMPLES.md
- Open Apple Notes in MacOS and select the "Import Markdown..." menu
- Find the folder where KIM exported your markdown files
- Select either the folders or files or both in the same directory where KIM exported - you do not need to drop into each markdown folder - just select the folders and/or files
- Run the import
- All markdown folder imports that have media will end up in the current Apple Notes folder you have open at the time in the UI 
- All markdown simple files will end up in the Mac "Imported Notes" folder
- Once transferred, run the special Apple Shortcut (link provided) that will convert your Keep labels to Apple Notes tags
