import encryption
import fileutil
import passutil
from keystore import Keystore
from progress import ProgressBar

maindir = "..\\Secure Folder"


def lock():
    print(" ".join(["Using this directory:", fileutil.getfullpath(maindir)]))
    print("Finding all files...")
    filelist, count = [], 0
    for file in fileutil.getNewFiles(maindir):
        filelist.append(file)
        count += 1
    print("Found all {} files".format(count))
    print("Now Encrypting Files")
    ks = Keystore("SecureFolder.pks")
    ks.newkeystore()
    probar = ProgressBar(count)
    for file in filelist:
        try:
            filepath, sign = encryption.encrypt_files(file, maindir)
            ks.newkey(file, filepath, sign)
        except Exception as e:
            print(e)
            return False
        probar.update()
    probar.finish()
    del(probar)
    ks.saveclose()
    print("Storing Encryption Keys")
    password = passutil.getpassword()
    try:
        passutil.encrypt_keyfile(password, "SecureFolder.pks")
    except Exception as e:
        print(e)
        return False
    print("Finished")
    return True


def unlock():
    ex = True
    while ex:
        password = str(passutil.getpassword())
        try:
            passutil.decrypt_keyfile(password, "SecureFolder.pks")
        except Exception as e:
            print(e)
            continue
        ex = False
    print(" ".join(["Using this directory:", fileutil.getfullpath(maindir)]))
    print("Finding all encrypted files...")
    ks = Keystore("SecureFolder.pks", mode="r")
    ks.load()
    count = len(ks.getkeys())
    print("Found {} encrypted files defined in Keystore".format(count))
    print("Now Decrypting Files")
    probar = ProgressBar(count)
    for keybag in ks.getkeys():
        try:
            encryption.decrypt_files(maindir, keybag)
        except Exception as e:
            print(e)
            return False
        probar.update()
    probar.finish()
    del(probar)
    print("Finished")
    fileutil.srmFile("SecureFolder.pks")
    return True


def main():
    while True:
        print("Python Encryption Program")
        print("Please Select Choice")
        print("1. Lock Directory")
        print("2. Unlock Directory")
        print("3. Exit")
        choice = int(input(">>> "))
        if choice == 1:
            lock()
        elif choice == 2:
            unlock()
        elif choice == 3:
            return None
        else:
            print("Invaild Option")


main()
