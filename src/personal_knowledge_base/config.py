# from fastapi import  Path
import os
from pydantic import SecretStr
from dotenv import load_dotenv


class PkbConfig:
    EMPTY_STRING = ""
    _PKB_DATA_FOLDER = "bla bla"
    _PKB_QDRANT_DB_PATH = EMPTY_STRING
    _PKB_COLLECTION_NAME = EMPTY_STRING
    _IMAP_USER_NAME = EMPTY_STRING
    _IMAP_SSL_HOST = EMPTY_STRING
    _IMAP_SSL_PORT = EMPTY_STRING
    EMBEDDING_MODEL = "openai/text-embedding-3-small"
    SPARSE_EMBEDDING_MODEL = "Qdrant/bm25"
    URL = "https://openrouter.ai/api/v1"

    @property
    def PKB_DATA_FOLDER(self):
        return self._PKB_DATA_FOLDER

    @property
    def PKB_QDRANT_DB_PATH(self):
        return self._PKB_QDRANT_DB_PATH

    @property
    def PKB_COLLECTION_NAME(self):
        return self._PKB_COLLECTION_NAME

    @property
    def IMAP_USER_NAME(self):
        return self._IMAP_USER_NAME

    @property
    def IMAP_SSL_HOST(self):
        return self._IMAP_SSL_HOST

    @property
    def IMAP_SSL_PORT(self):
        return self._IMAP_SSL_PORT

    @property
    def openrouter_api_key(self):
        API_KEY = SecretStr(os.getenv("OPENROUTER_API_KEY", ""))
        if not API_KEY.get_secret_value():
            raise RuntimeError("OPENROUTER_API_KEY is not set")
        return API_KEY

    def __init__(self):
        load_dotenv()
        self.read_config()

    def read_config(self):
        self._PKB_DATA_FOLDER = read_config("PKB_DATA_FOLDER")
        self._PKB_QDRANT_DB_PATH = read_config("PKB_QDRANT_DB_PATH")
        self._PKB_COLLECTION_NAME = read_config("PKB_COLLECTION_NAME")
        self._IMAP_USER_NAME = read_config("IMAP_USER_NAME")
        self._IMAP_SSL_HOST = read_config("IMAP_SSL_HOST")
        self._IMAP_SSL_PORT = read_config("IMAP_SSL_PORT")



                
# ========================================================================
def read_config(variable: str) -> str:
    config_file = "./src/personal_knowledge_base/config.txt"
    f = open(config_file, "r")
    for line in f:
        if line in ['\n', '\r\n']:
            continue
        s = line.split()
        print("aftr split, s[0] = " + s[0] + ", s[1] = " + s[1])
        if (s[0] == variable):
            print("assigning..  _PKB_DATA_FOLDER = " + s[1])
            return s[1]


global_config = PkbConfig()      


