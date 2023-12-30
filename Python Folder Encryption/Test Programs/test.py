import encryption
from Crypto.Cipher import AES

key = encryption.genkey()
file = "50mb"
resalt = True
print("Key:", key.hex())

in_file = open(file, "rb")
out_file = open(file + '.encrypted', 'wb+')
key_file = open(file + '.keyfile', 'wb+')
print("Encrypting")
try:
    # Create the cipher object and encrypt the data
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext = cipher.encrypt(in_file.read())
    hash = cipher.digest()
    key_file.write(cipher.nonce)
    key_file.write(hash)
    key_file.write(key)
    out_file.write(ciphertext)
    print("Nonce:", len(cipher.nonce), "Key:",
          len(key), "Hash:", len(hash))

except ValueError:
    print("ERROR:ValueError")

except KeyError:
    print("ERROR:KeyError")

except Exception as e:
    print("ERROR:{}".format(e))

# Close the input and output files
in_file.close()
out_file.close()
key_file.close()

in_file = open(file + '.encrypted', 'rb')
out_file = open(file + ".copy", 'wb+')
key_file = open(file + '.keyfile', 'rb')
resalt = True
print("Decrypting")
try:
    in_nonce = key_file.read(16)
    in_hash = key_file.read(16)
    in_key = key_file.read(32)
    cipher = AES.new(in_key, AES.MODE_GCM, nonce=in_nonce)
    plaintext = cipher.decrypt(in_file.read())
    hash = cipher.verify(in_hash)
    out_file.write(plaintext)
    print("Nonce:", len(cipher.nonce), "Key:",
          len(in_key))


except ValueError:
    print("ERROR:ValueError")

except KeyError:
    print("ERROR:KeyError")

except Exception as e:
    print("ERROR:{}".format(e))

in_file.close()
out_file.close()
key_file.close()
