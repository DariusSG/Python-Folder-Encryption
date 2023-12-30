import fileutil
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from keystore import Signature

BUFFER_SIZE = 1024


def genkey():
    return get_random_bytes(32)


# === Encrypt ===
def encrypt_files(file, maindirpath):
    key = genkey()
    file_path = maindirpath + "\\" + file
    in_file = open(file_path, "rb")
    out_file = open(file_path + '.encrypted', 'wb+')

    try:
        # Create the cipher object and encrypt the data
        cipher = AES.new(key, AES.MODE_GCM)
        data = in_file.read(BUFFER_SIZE)
        while len(data) != 0:
            encrypted_data = cipher.encrypt(data)
            out_file.write(encrypted_data)
            data = in_file.read(BUFFER_SIZE)
        hash = cipher.digest()

    except Exception as e:
        in_file.close()
        out_file.close()
        fileutil.srmFile(file_path + '.encrypted')
        raise Exception("{}".format(e)) from e

# Close the input and output files
    sign = Signature().newsignature(cipher.nonce, key, hash)
    in_file.close()
    out_file.close()
    fileutil.srmFile(file_path)
    return file_path, sign


# === Decrypt ===
def decrypt_files(maindirpath, keybag):
    file_path = keybag['path']
    in_file = open(file_path + '.encrypted', "rb")
    out_file = open(file_path, 'wb+')

    try:
        sign = Signature()
        sign.loadsignature(keybag['signature'])
        in_nonce = sign.intnonce
        in_hash = sign.intmactag
        in_key = sign.intkey
        cipher = AES.new(in_key, AES.MODE_GCM, nonce=in_nonce)
        data = in_file.read(BUFFER_SIZE)
        while len(data) != 0:
            decrypted_data = cipher.decrypt(data)
            out_file.write(decrypted_data)
            data = in_file.read(BUFFER_SIZE)
        cipher.verify(in_hash)

    except ValueError as e:
        in_file.close()
        out_file.close()
        fileutil.srmFile(file_path)
        raise Exception("ValueError[{}]".format(e)) from e

    except KeyError as e:
        in_file.close()
        out_file.close()
        fileutil.srmFile(file_path)
        raise Exception("KeyError[{}]".format(e)) from e

    except Exception as e:
        in_file.close()
        out_file.close()
        fileutil.srmFile(file_path)
        raise Exception("{}".format(e)) from e

    # Close the input and output files
    in_file.close()
    out_file.close()
    fileutil.srmFile(file_path + '.encrypted')
    return True
