## Simple Export
#### Query and export active notes
`python kim.py`

#### Query and export archived notes
`python kim.py -a`

#### Export all active notes in batch without prompts
`python kim.py -b --all`

#### Export all active notes in batch with create dates after Jan 1, 2023
`python kim.py -cd "> 2023-01-01" -b --all`


## Complex Export
#### Export all active notes in batch with edit dates after May 14, 2024, format to Joplin style headers, and move them to archive after export
`python kim.py -j -m -ed "> 2023-05-14" -b --all`

#### Export all active notes in batch with using the first note line as the markdown file title, format Logseq bullets, and overwriting any existing notes
`python kim.py -c -l -o -b --all`