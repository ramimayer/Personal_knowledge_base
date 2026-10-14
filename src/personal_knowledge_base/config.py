# This class reads the configuration-file of this project ONCE, and when another file imports the "global_config"
# instance - it gets access to these configuration-variables

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
    _MAIL_PASSWD = EMPTY_STRING
    _API_KEY = EMPTY_STRING
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
    def MAIL_PASSWD(self):
        return self._MAIL_PASSWD

    @property
    def openrouter_api_key(self):
        return self._API_KEY

    @property
    def mail_passwd(self):
        return self._MAIL_PASSWD

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
        self._MAIL_PASSWD = SecretStr(os.getenv("MAIL_SERVER_PASSWD", ""))
        self._API_KEY = SecretStr(os.getenv("OPENROUTER_API_KEY", ""))

        if not self._API_KEY.get_secret_value():
            raise RuntimeError("OPENROUTER_API_KEY is not set")
        
        if not self.MAIL_PASSWD.get_secret_value():
            raise RuntimeError("MAIL_SERVER_PASSWD is not set")

        if not os.path.exists(self._PKB_DATA_FOLDER):
            raise RuntimeError("The folder where messages should save DOESN'T exist! " + self._PKB_DATA_FOLDER)

        if not os.path.exists(self._PKB_QDRANT_DB_PATH):
            raise RuntimeError("The QDRANT_DB folder DOESN'T exist! " + self._PKB_QDRANT_DB_PATH)


                
# ========================================================================
def read_config(variable: str) -> str:
    config_file = "./src/personal_knowledge_base/config.txt"
    f = open(config_file, "r")
    for line in f:
        if line in ['\n', '\r\n']:
            continue
        s = line.split()
        if (s[0] == variable):
            return s[1]


global_config = PkbConfig()      


