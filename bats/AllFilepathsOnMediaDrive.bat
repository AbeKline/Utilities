@echo off
Z:
dir/s/b > AllFilepathssOnMediaDrive.txt
copy /y AllFilepathssOnMediaDrive.txt "C:\Users\AbesGames\Google Drive\AllFilepathssOnMediaDrive.txt" 
copy /y AllFilepathssOnMediaDrive.txt "F:AllFilepathssOnMediaDrive.txt"