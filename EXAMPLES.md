## Simple Export

### All user queries have the prompt:
`Enter a keyword search, label search or --all' to convert Keep notes to md or '--x' to exit:`

#### User query and export active notes (no notes will be overwritten)
`python kim.py`

#### User query and export only archived notes
`python kim.py -a`

#### User query and export active notes and overwrite existing markdown notes
`python kim.py -o`

#### User query to export active notes that were edited after Jun 15, 2023
`python kim.py -ed "> 2023-06-15"`

#### Export all active notes in batch without user prompts
`python kim.py -b --all`

#### Export only notes with the label #science in batch without user prompts
`python kim.py -b "#science"`

#### Export all active notes with silent mode with output to kim.log in batch with create dates after Jan 1, 2023
`python kim.py -q -cd "> 2023-01-01" -b --all`

#### Export all active notes in batch and skip over notes already exported
`python kim.py -s -b --all`

## Import Files

#### Import all markdown and text files in the import folder (labels in settings) - move files to completed folder when done (labels must pre-exist)
`python kim.py -i`

#### Import all markdown and text files in the import folder with labels input - move files to completed folder when done (labels must pre-exist)
`python kim.py -i -lb movies,tv,media`

## Complex Export
#### Export all active notes in batch formatted to Joplin front matter headers, and move them to archive after export with edit dates after May 14, 2024
`python kim.py -j -m -ed "> 2023-05-14" -b --all`

#### Export all active notes with the label #computer in batch using the first note line as the markdown file title if the title is missing (50 chars max), preserve Logseq namespaces and format Logseq bullets, and overwriting any existing notes
`python kim.py -c -l -o -b "#computer"`

#### Export all active notes in batch preserving Keep labels with spaces and special characters, skipping over existing notes, moving them to archive after export in silent mode (output to kim.log)
`python kim.py -p -s -m -q -b --all`

#### Export all archived notes in batch, overwriting existing notes and modifying Keep note-to-note markdown links to wikilinks
`python kim.py -a -o -w -b --all`

### List of options
```
Options:
  -r  Will reset and not use the local keep access token in your system's keyring  
  -o  Overwrite any existing markdown files with the same name  
  -a  Search and export only archived notes  
  -p  Preserve keep labels with spaces and special characters  
  -s  Skip over any existing notes with the same title  
  -c  Use starting content within note body instead of create date for md filename  
  -l  Prepend paragraphs with Logseq style bullets and preserve namespaces 
  -j  Prepend notes with Joplin front matter tags and dates  
  -m  Move any exported Keep notes to Archive  
  -w  Convert pre-formatted markdown note-to-note links to wikilinks  
  -q  Execute exporting or importing in silent mode - output to kim.log
  -i  Import notes from markdown files WARNING - EXPERIMENTAL!! 
  -lb TEXT  Comma delimited labels for import - for use with only with (-i) flag
  -cd TEXT  Export notes before or after the create date - < or > YYYY-MM-DD  
  -ed TEXT  Export notes before or after the edit date - < or > YYYY-MM-DD  
  -b  --search-term TEXT  Run in batch mode with a specific Keep search term  
  -t  --master-token TEXT  Log in using master keep token
  --help Show this message and exit.
```
