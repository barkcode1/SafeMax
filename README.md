# SafeMax
A simple yet effective file encryptor using a password.
I learned a surprising amount of knowledge from just this small project alone.

## Features
 - It uses AES GCM encryption to encrypt a file's bytes.
 - [Overwrite Mode](#overwrite-mode) (My favorite part)
 - Easy to use and open source

## Installation (.exe)
Installing as a .exe format might take a bit more time but it is still easy to do and makes the program more accessible and user friendly.

1. Make sure you have pip and python 3 installed.
2. Download safemax.py and requirements.txt
3. In command prompt go to the same directory as requirements.txt and run
```bash
pip install requirements.txt
```
4. Now in the same directory as safemax.py run
```bash
pyinstaller --onefile safemax.py
```
5. This should create multiple folders in the same directory as safemax.py. Locate the dist folder and inside should be the working safemax.exe file.

## Installation (.py)
Installing as a .py is really simple, but running the program is a bit more inconvenient.

1. Follow steps 1-3 as in the previous installation
2. Use a python interpereter (online, IDLE, etc.) to run safemax.py

## Usage
To encrypt/decrypt a file, begin by entering the path of the file you want to encrypt/decrypt

e.g. "C:\Users\Name\FileLocation\passwords.txt"

The process from here is pretty straightforward.

### Commands:
1. help\
This is self-explanatory. Gives a list of commands and how the program works
2. salt\
Change the salt currently used by your program. Useful if you want to decrypt someone else's file.\
The salt originally created by your program is always stored at SafeMax/salt_backup.txt (the exact location can be seen with the help command).
3. overwrite_enable / overwrite_disable\
Disabled by default, it toggles overwrite on or off. Overwrite essentially deletes the file you are encrypting so that no trace is left. View more [here](#overwrite-mode)



## For the people who actually want to use this
If you are planning to use this program to encrypt your actual, sensitive files, then:

1. I dont reccomend it. This is a hobby project and there are more professional options out there.
2. MAKE SURE to save your salt located in %LOCALAPPDATA%/SafeMax/salt.txt on windows or ~/.safemax/salt.txt as a hidden folder in linux/mac.

The salt is crucial to be kept because it is tied to the password used to encrypt your file, so keep it somewhere safe!!!


## Overwrite Mode
With overwrite mode enabled, encrypting any file with overwrite it with random bytes and then delete it completely. If you don't have any backups left of the file (onedrive, file backups, etc.), it will be virtually impossible to recover (meaning your important data won't be accessible anymore without the password).

While researching, it appears that this works extremely well on HDD (Hard Disk Drive), but will not work on an SSD (Solid State Drive). The technicalities go pretty deep, so the only real way to wipe it fully from an SSD would to be with a hard reset erase-all-data type of thing. 

In any case, even with an SSD, overwrite mode ensures that your data is wiped in a secure fasion that it would basically require a team of forensics and professionals with specialized tools to have a chance at recovery.
