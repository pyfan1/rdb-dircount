
rdb-dircount
============

Count directories backed up by rdiff-backup
-------------------------------------------

[rdiff-backup](https://rdiff-backup.net/) can list the files involved in a backup, however, the list can be overwhelming. rdb-dircount.py counts the occurrences of each directory so you can see which ones are contributing the most files to a given backup. 

It expects the output of the command "rdiff-backup list files ..." 

For example, the command 

`rdiff-backup list files --changed-since 1D /backup/repos/itory | rdb-dircount.py `

would count all the files and directories backed up the previous day in the repository __/backup/repos/itory__ and display them in order of decreasing count. 

It can display the result sorted either by decreasing count or by file name. The command 

`rdb-dircount.py -h `

displays a help message telling how to select the sort order. 

If you have the file lists saved in files, you can list one or more of those files on the command line, and rdb-dircount.py will take its input from them instead of stdin. 


