import os
import shutil

from secure_delete import secure_delete


def tar_compress(filename, dirpath):
    return shutil.make_archive(filename, "tar", dirpath)


def tar_decompress(filename, dirpath):
    return shutil.unpack_archive(filename, dirpath, "tar")


def getfullpath(dirpath):
    return os.path.abspath(dirpath)


def removeFile(file):
    os.remove(file)


def move(file, dst):
    shutil.move(file, dst)


def mkdirs(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)


def srmFile(file):
    secure_delete.secure_random_seed_init()
    secure_delete.secure_delete(file)


def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def getNewFiles(inputdir):
    for sourcefile in getListOfFiles(inputdir):
        if not sourcefile.endswith('.encrypted'):
            path = ""
            for i in sourcefile.split("\\")[2:]:
                path += "\\{}".format(i)
            yield path


def getEncryptedFiles(inputdir):
    for sourcefile in getListOfFiles(inputdir):
        if sourcefile.endswith('.encrypted'):
            path = ""
            for i in sourcefile.split("\\")[2:]:
                path += "\\{}".format(i)
            yield path


def joinpath(path, paths):
    return os.path.join(path, paths)


def clean(dirpath):
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)


def removefileext(file_path):
    return os.path.splitext(file_path)[0]
