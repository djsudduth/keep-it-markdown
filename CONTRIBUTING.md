## NOTE: Kim is in full refactoring for version 0.5.0!!
What's happening? The kim structure is being modified for more generic output of notes.  
You will be able to define Keep input and output classes for markdown, joplin, json, etc. 
For example, the routine save_md_file() is generic for any markdown output for any input type
as long as the Note data object is populated.  
The goal is to modularize more of the input and output code so that new markdown apps can be 
accomodated.  
Please be aware the changes are fairly significant.

#### Pull Request Branch
All contributions should submit pull requests to the **develop** branch of this repo. 

#### Formatting
Please try to observe formatting by using the yapf utility. The formatting rules have been provided in the
.editorconfig and .style.yapf files included in this rep.

To install yapf run:
```bash
> pip install yapf
```

To execute formatting run:
```bash
> yapf kim.py 
```
within the same directory as the formatting rules files noted above.

#### Forking
Contributions are welcome! Just fork this repo, make your changes and submit a pull request!