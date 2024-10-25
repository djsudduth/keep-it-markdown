## NOTE: Kim is in full refactoring for version 0.5.0!!
What's happening?  
The kim structure is being modified for more generic output of notes.  You will be able to define Keep input and output classes for markdown, joplin, json, etc. For example, the routine save_md_file() is generic for any markdown output for any input type as long as the Note data object is populated.  

The goal is to modularize more of the input and output code so that new markdown apps can be accommodated.  

Please be aware the 0.5.0 changes are fairly significant!

#### Pull Request Branch
All contributions should submit pull requests to the **develop** branch and not **main** of this repo. 

#### Philosophy
Please try to submit pull requests that are more incremental in nature vs. a big bang approach. Small feature and bug fixes are more appropriate for evolving this utility. 

#### Formatting
Please try to observe formatting by using the PEP 8 Style Guide. 

#### Forking
Contributions are welcome! Just fork this repo, make your changes and submit a pull request!