from keystore import Keystore


def addstuff(kys: Keystore):
    kys.newkey("Test", "Test", "aaa")


ks = Keystore("keystore.ks")
ks.newkeystore()
addstuff(ks)
ks.saveclose()
