# gittar

Many file formats including those with extensions `docx`, `xlsx`, `pptx`, etc. used by Microsoft Office (Word, Excel, PowerPoint etc.) are actually zip files containing mainly plain texts (specifically XML for the examples).  

After unzipped, these files and their different versions can be managed by [`git`](https://github.com/git/git), a useful version control system.  

Here I write `gittar`, a simple command implementing the idea above. The gadget is equivalent to a combination of `git` and `tar`, hence the name, although the unzipping does not rely on `tar` in fact. 

## Installation

The script of `gittar` is written in Python 3. Dependencies including `codecs`, `os`, `shutil`, `sys`, `xml`, and `zipfile` (all Python packages) should be ready before using the command.

In Windows OS, the directory containing `gittar.py` and `gittar.bat` should be added to the `PATH` environmental variable to allow the tool to launch anywhere in the system when necessary.

## Usage

All `gittar` commands resemble those for `git`, except `gittar add` and `gittar diff` currently require an argument corresponding to an existing file.

```
gittar init
gittar add somefile.xlsx
gittar commit -m "some commit message"
```

After modifying the content of `somefile.xlsx`, the user may execute `gittar diff somefile.xlsx` to check the difference between the current status and the last committed version (maybe illegible although).

The command `gittar reset` has not been implemented yet.

## History

- v0.0.1, prototype
