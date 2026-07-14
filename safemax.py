# SafeMax
# I didn't include comments (too lazy too add this time)
# If you really want to understand the program it is somewhat easy to follow along the code
import os
import base64
import hashlib
import sys
import getpass
import random
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def save_file(path, contents):
    f = open(os.path.join(app_dir, path), "w")
    f.write(contents)
    f.close()

def read_file(path):
    f = open(os.path.join(app_dir, path), "r")
    contents = f.read()
    f.close()
    return contents
def handle_path(p):
    if p[0] == '"':
        return p.strip('"')
    return p
if sys.platform == "win32":
    app_dir = os.path.join(os.environ["LOCALAPPDATA"], "SafeMax")
else:
    app_dir = os.path.join(os.path.expanduser("~"), ".safemax")


salt_message = "\n\nDO NOT TAMPER WITH THE SALT ABOVE - IT WILL RESULT IN YOU UNABLE TO ACCESS YOUR CURRENT PASSWORDS\nIt is recommended to keep this salt somewhere safe"

if not os.path.isdir(app_dir):

    os.makedirs(app_dir, exist_ok=True)

    letters = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()")
    salt = ''.join(random.choice(letters) for _ in range(16))
    
    save_file("salt.txt", salt + salt_message)
    save_file("salt_backup.txt", salt + salt_message)

    save_file("overwrite_settings.txt", "F")




salt = read_file("salt.txt").split("\n")[0]
overwrite_setting = read_file("overwrite_settings.txt")[0]



def encrypt(data, password):
    key = hashlib.sha256(password.encode()).digest()

    nonce = os.urandom(12)

    aes = AESGCM(key)
    ciphertext = aes.encrypt(nonce, data, None)

    return base64.b64encode(nonce + ciphertext).decode()


def decrypt(data, password):
    key = hashlib.sha256(password.encode()).digest()

    data = base64.b64decode(data)
    nonce = data[:12]
    ciphertext = data[12:]

    aes = AESGCM(key)
    plaintext = aes.decrypt(nonce, ciphertext, None)

    return plaintext


print("Welcome to SafeMax!")
print("For help on commands, type help into the console")

while True:
    userinput = handle_path(input("\n> "))

    if userinput.lower() == "help":
        print("\nTo use SafeMax, start by entering the path of the file you want to encrypt/decrypt to the console.\n\
        \nChoosing a safe password is VERY important. A character length of at least 12 is strongly recommended.\
        \n\n\n\nSalt: Each user on SafeMax is given a unique salt. \
        \nPasswords created with a salt will only work with the same salt that was originally used when the password was first used.\
        \nYou can change your salt by typing salt into the console. BE SURE YOU KNOW WHAT YOU ARE DOING BEFORE CHANGING A SALT!!\
        \nYour orignal salt will always be backed up at: '" + os.path.join(app_dir, "salt_backup.txt") + "'\
        \n\nOverwrite (off by default): With overwrite enabled, files encrypted will overwrite (delete) the file being encrypted, meaning the only way to retrieve the file will be to decrypt it.\
        \nType overwrite_enable or overwrite_disable to toggle this feature.\
        \nNotice - The overwrite setting will save inbetween sessions!\
        \n\n\nTo exit the software, type quit\n\n\n")
        continue


    elif userinput.lower() == "quit" or userinput.lower() == "q":
        sys.exit()


    elif userinput.lower() == "overwrite_enable":
        overwrite_setting = "T"
        save_file("overwrite_settings.txt", "T")
        print("Overwrite is enabled")
        continue


    elif userinput.lower() == "overwrite_disable":
        overwrite_setting = "F"
        save_file("overwrite_settings.txt", "F")
        print("Overwrite is disabled")
        continue


    elif userinput.lower() == "salt":
        userinput = input("Confirm you want to change your salt (I know what I'm doing!) (y|n):")
        if userinput.lower() != "y":
            continue
        
        salt = input("Enter new salt here:")

        save_file("salt.txt", salt + salt_message)

        print("Salt set to '" + salt + "'")
        print("You can always find your original salt backed up at '" + os.path.join(app_dir, "salt_backup.txt") + "'")
        continue



    elif not os.path.exists(userinput):
        print("Invalid command / Path does not exist! Type help for a list of commands")
        continue




    with open(userinput, "rb") as f:
        content = f.read()


    name = os.path.splitext(os.path.basename(userinput))[0]
    fullpath = userinput
    location = os.path.dirname(userinput)

    userinput = input("Encrypt|Decrypt|Quit (e|d|q):")

    if userinput.lower() == "q" or userinput.lower() == "quit":
        continue
    elif userinput.lower() == "e":
        print("A long and safe password is STRONGLY recommended!")
        pwd = salt + getpass.getpass("Enter password (text will be hidden):")

        confirm_pwd = salt + getpass.getpass("Confirm password (text will be hidden):")

        if not pwd == confirm_pwd:
            print("Passwords do not match!")
            continue

        

        
        filename = name + ".enc"
        filelocation = os.path.join(location, filename)
        if os.path.exists(filelocation):
            print("Error: '" + filelocation + "' already exists")
            continue

        encrypted = encrypt(content, pwd)
        
        with open(filelocation, "w") as encrypted_file:
            encrypted_file.write(encrypted)

        if overwrite_setting == "T":
            size = os.path.getsize(fullpath)
            with open(fullpath, "r+b") as f:
                f.write(os.urandom(size))
                f.flush()
                os.fsync(f.fileno())
            
            os.remove(fullpath)

            print("Successfully deleted '" + fullpath + "'")

        print("Successfully encrypted file as " + filename + "\n")
        continue




    elif userinput.lower() == "d":
        pwd = salt + getpass.getpass("Enter password:")

        userinput = input("Optional: File extension|Defualt-txt ({extension}|d:")
        if userinput.lower() == "d" or userinput == "":
            userinput = ".txt"
        elif userinput[0] != ".":
            userinput = "." + userinput

        userinput2 = input("Enter file name:")
        
        filename = userinput2 + userinput
        filelocation = os.path.join(location, filename)

        if os.path.exists(filelocation):
            print("Error: '" + filelocation + "' already exists")
            continue

        decrypted = decrypt(content, pwd)

        with open(filelocation, "wb") as decrypted_file:
            decrypted_file.write(decrypted)

        print("Successfully decrypted file as " + filelocation + "\n")
        continue


