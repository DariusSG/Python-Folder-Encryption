import json

FILE_VERSION = 1

FILE_FORMAT = {
    "version": FILE_VERSION,
    "store": []
}

KEY_FORMAT = {
    "name": "",
    "path": "",
    "signature": ""
}


class Keystore:
    def __init__(self, filepath, mode="w+"):
        if type(filepath) != str:
            raise "Exception: Invaild File Path"
        elif filepath == "":
            raise "Exception: Invaild File Path"
        self.mode = mode
        self.file = open(filepath, mode)

    def load(self):
        try:
            self.keyfile = json.load(self.file)
        except ValueError:
            self.file.close()
            raise "Exception: Invaild or Corrupted Keystore file"

    def newkeystore(self):
        self.ks = dict(FILE_FORMAT)

    def newkey(self, name, filepath, signature):
        newkeyfile = dict(KEY_FORMAT)
        newkeyfile["name"] = name
        newkeyfile["path"] = filepath
        newkeyfile["signature"] = signature
        self.ks["store"].append(newkeyfile)

    def getkeys(self):
        return self.keyfile["store"]

    def save(self):
        if self.mode != "w+":
            raise "Exception: File is not in Read-Write Mode"
        try:
            json.dump(self.ks, self.file, indent=4)
        except Exception as e:
            raise "Exception: {}".format(e)

    def close(self):
        self.file.close()

    def saveclose(self):
        self.save()
        self.close()


class Signature:
    def __init__(self):
        self.intkey, self.intnonce, self.mactag = None, None, None

    def newsignature(self, nonce, key, mactag):
        self.intkey, self.intnonce, self.intmactag = key, nonce, mactag
        return "{n}${k}${mt}".format(n=nonce.hex(),
                                     k=key.hex(),
                                     mt=mactag.hex())

    def loadsignature(self, signature):
        bsign = signature.split("$")
        self.intnonce = bytes.fromhex(bsign[0])
        self.intkey = bytes.fromhex(bsign[1])
        self.intmactag = bytes.fromhex(bsign[2])

    def nonce(self):
        return self.intnonce

    def key(self):
        return self.intkey

    def mactag(self):
        return self.intmactag
