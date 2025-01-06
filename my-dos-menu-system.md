---
date: 2024-04-22
---

# My DOS menu system

On Thursday and Friday,

I wrote a DOS menu system in QBASIC, (compiled with QuickBASIC), for my family to launch DOS games without having to \*gasp\* learn to use the DOS command line.
This menu system is fairly simple, it reads MENU.CSV in the current working directory, for example:

```
Play Music,C:\APPS\MPXPLAY\,MPXPLAY.EXE D:\MEDIA\MUSIC\*.MP3
Microsoft Word 5.5,C:\DOC\,C:\APPS\WORD\WORD.EXE
FreeDOS EDIT,C:\DOC\,C:\FREEDOS\BIN\EDIT.EXE
QBASIC,C:\SRC\,C:\DEVEL\QB11\QBASIC.EXE
```

It has the name, working directory, and command to run.
This is flexible enough that I implemented submenus without any change to the code.

It draw the menu border using line drawing characters, and uses double line characters for the selected item.
Navigation is with the up and down arrow keys, and items are selected using the enter key.

### Screenshots

![](/Menu_Shot_1.png)
#### Submenu (Other)
![](/Menu_Shot_2.png)
#### On my CRT
![](/CRT_DOS_1.png)

### Download
[menu.tar.gz](https://ebruce613.tilde.team/files/menu.tar.gz)
