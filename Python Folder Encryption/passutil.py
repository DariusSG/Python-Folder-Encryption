import getpass
import re

import fileutil
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes


def checkstrength(password):
    if (len(password) < 12):
        print("Password too short!")
        return False
    elif not re.search("[a-z]", password):
        print("Password must contain at least one lowercase latter!")
        return False
    elif not re.search("[A-Z]", password):
        print("Password must contain at least one uppercase latter!")
        return False
    elif not re.search("[0-9]", password):
        print("Password must contain at least one number between 0 and 9")
        return False
    elif not re.search("[@_!#$%^&*()<>?}{~:]", password):
        print("Password must contain at least one Special Character")
        print('@_!#$%^&*()<>?}{~:')
        return False
    else:
        return True


def getpasswordprompt(check):
    if check:
        return getpass.getpass("Re-Enter the Password: ")
    else:
        return getpass.getpass("Enter the Password: ")


def getpassword(check=False):
    while True:
        password = getpasswordprompt(False)
        if check:
            return password
        while not checkstrength(password):
            password = getpasswordprompt(True)
        checkpass = getpasswordprompt(True)
        while checkpass == password:
            return password
        print("Password does not match")


def passwordhash(password, resalt, salt=get_random_bytes(32)):
    key = scrypt(password, salt, 32, N=1048576, r=8, p=1)
    if resalt:
        return key, salt
    else:
        return key


def encrypt_keyfile(password, keyfile):
    in_file = open(keyfile, "rb")
    out_file = open(keyfile + '.encrypted', 'wb+')
    resalt = True

    try:
        # Create the cipher object and encrypt the data
        key, salt = passwordhash(password, resalt)
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext = cipher.encrypt(in_file.read())
        out_file.write(cipher.nonce)
        out_file.write(salt)
        out_file.write(cipher.digest())
        out_file.write(ciphertext)

    except Exception as e:
        in_file.close()
        out_file.close()
        fileutil.srmFile(keyfile + '.encrypted')
        raise Exception("{}".format(e)) from e

# Close the input and output files
    in_file.close()
    fileutil.srmFile(keyfile)
    out_file.close()
    return True


def decrypt_keyfile(password, keyfile):
    in_file = open(keyfile + '.encrypted', "rb")
    out_file = open(keyfile, 'wb+')
    resalt = False

    try:
        in_nonce = in_file.read(16)
        in_salt = in_file.read(32)
        in_hash = in_file.read(16)
        key = passwordhash(password, resalt, salt=in_salt)
        cipher = AES.new(key, AES.MODE_GCM, nonce=in_nonce)
        plaintext = cipher.decrypt(in_file.read())
        cipher.verify(in_hash)
        out_file.write(plaintext)

    except ValueError as e:
        in_file.close()
        out_file.close()
        fileutil.srmFile(keyfile)
        raise Exception("ValueError[{}]".format(e)) from e

    except Exception as e:
        in_file.close()
        out_file.close()
        fileutil.srmFile(keyfile)
        raise Exception("{}".format(e)) from e

    # Close the input and output files
    in_file.close()
    fileutil.srmFile(keyfile + '.encrypted')
    out_file.close()
    return True
