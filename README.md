# Paper_summary_Manager
__Paper summary Manager stores summaries in a database using SQLite__



### Table of Contents

- [Introduction](#intro)
- [Interface](#interface)
- [Icons attribution](#icons-attribution)

### Introduction
Simple program to make a summary database. This is specific to my needs(read literature review) and not a general application.
It is quite clear from the layout. Further, this application is best used only on aingle computer. 
The _Paper.db_ file is the database and it is created by default when you run the app for the first time. If you wish to use across multiple-systems, ideally you would link _Paper.db_ to the cloud and have updated across sytems. The App is run by double clicking the App.pyw file after installing python in your system. It needs the support folder to run!



### Interface
**Shortcuts**
- *ctrl + E* Edit entry 
- *ctrl + A* Add entry
- *ctrl + D* Delete entry
- *ctrl + R* Refresh 

The interface is quite simple... 
once you open the app, you'll be greated with this screen. If you already have some papers int eh database, using refresh or filter will show them in the table. 

<img src="https://github.com/vinaykrishna64/Paper_summary_Manager/blob/main/readme_pics/P1.png" width="600" height="400" />

You can add an entry using the green plus icon or the shortcut *ctrl + A*. Each entry has 4 fields *lab* , *field* , *cfd* & *review* to help with filtering the papers. You can select no or multiple fields. .If you choose to not tick any checkboxes, it would mean the paper won't come under any of the four filters.

<img src="https://github.com/vinaykrishna64/Paper_summary_Manager/blob/main/readme_pics/P2.png" width="600" height="400" />

You click on the entries listed in table to show the entered summary and tags. 

<img src="https://github.com/vinaykrishna64/Paper_summary_Manager/blob/main/readme_pics/P3.png" width="600" height="400" />

You can delete an entry using the bin icon or the shortcut *ctrl + D* aftering selecting an entry in the table. You'll prompted with a dialog to confirm the deletion as there is not backup or undo for this.

<img src="https://github.com/vinaykrishna64/Paper_summary_Manager/blob/main/readme_pics/P4.png" width="600" height="400" />
<img src="https://github.com/vinaykrishna64/Paper_summary_Manager/blob/main/readme_pics/P5.png" width="600" height="400" />

You can edit an entry using the document icon or the shortcut *ctrl + E* aftering selecting an entry in the table. You'll be given a form similar to Add entry which filled with previously entered data where you can make changes. You'll prompted with a dialog to confirm the edit as there is not backup or undo for this.

<img src="https://github.com/vinaykrishna64/Paper_summary_Manager/blob/main/readme_pics/P6.png" width="600" height="400" />
<img src="https://github.com/vinaykrishna64/Paper_summary_Manager/blob/main/readme_pics/P7.png" width="600" height="400" />
<img src="https://github.com/vinaykrishna64/Paper_summary_Manager/blob/main/readme_pics/P8.png" width="600" height="400" />

### Icons attribution


 They can be found here [Fugue Icons](https://p.yusukekamiyamane.com/)

(C) 2013 Yusuke Kamiyamane. All rights reserved.

These icons are licensed under a Creative Commons
Attribution 3.0 License.
<http://creativecommons.org/licenses/by/3.0/>

[Back To The Top](#Paper_summary_Manager)