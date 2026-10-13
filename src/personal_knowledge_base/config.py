# from fastapi import  Path
import os

class PkbConfig:
    EMPTY_STRING = ""
    _PKB_DATA_FOLDER = "bla bla"
    _PKB_QDRANT_DB_PATH = EMPTY_STRING

    @property
    def PKB_DATA_FOLDER(self):
        return read_config("PKB_DATA_FOLDER")

    def __init__(self):
        read_config("PKB_DATA_FOLDER")

def read_config(variable: str) -> str:
    config_file = "./src/personal_knowledge_base/config.txt"
    print("read_config():   config_file = " + config_file + ",   variable = " + variable)
    f = open(config_file, "r")
    for line in f:
        s = line.split()
        print("aftr split, s[0] = " + s[0] + ", s[1] = " + s[1])
        if (s[0] == variable):
            print("assigning..  _PKB_DATA_FOLDER = " + s[1])
            return s[1]
            # print("assigning..  _PKB_DATA_FOLDER = " + _PKB_DATA_FOLDER)
        
        print("line = " + line)
    f.close()

    print("read_config():  bfr returning")

    return ""

    # if not os.path.exists(_PKB_DATA_FOLDER):
    #     error_msg = "the given PKB_DATA_FOLDER (" + _PKB_DATA_FOLDER + ")  doesn't exist"
    #     raise RuntimeError(error_msg)

    # if not os.path.exists(_PKB_QDRANT_DB_PATH):
    #     error_msg = "the given PKB_QDRANT_DB_PATH (" + _PKB_QDRANT_DB_PATH + ")  doesn't exist"
    #     raise RuntimeError(error_msg)

