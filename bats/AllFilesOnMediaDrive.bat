@echo off
Z:
tree /f /a > AllFilesOnMediaDrive.txt
copy /y AllFilesOnMediaDrive.txt "C:\Users\AbesGames\Google Drive\AllFilesOnMediaDrive.txt" 
copy /y AllFilesOnMediaDrive.txt "F:\AllFilesOnMediaDrive.txt" 