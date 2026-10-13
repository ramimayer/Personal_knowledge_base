import pytest
import os
from pathlib import Path
from dotenv import load_dotenv
import shutil
import personal_knowledge_base.config 
from fastapi.testclient import TestClient
from personal_knowledge_base.web_service import rag
client = TestClient(rag)

#  ----  lobal test variables -  CHANGE thenm to suite your computer !!   -------------
VALID_FOLDER_TEXTS = "CodingAcademy"
NON_VALID_FOLDER = "Bad_Folder"
EMPTY_STR = ""

VALID_EMAIL =       "VALID_EMAIL"
NON_VALID_EMAIL =   "NON_VALID_EMAIL"

VALID_SAVE_FOLDER_ATTACHMENTS = "docs_orig_format"
VALID_SAVE_FOLDER_TEXTS = "txt_msgs"


#============================================================================================
@pytest.fixture(autouse=True)
def delete_created_folders():
    pkb_data_folder = personal_knowledge_base.config.read_config("PKB_DATA_FOLDER")
    if not pkb_data_folder:
        print("delete_created_folders():  bad PKB_DATA_FOLDER")
        return

    docs_path = pkb_data_folder + "/" + VALID_SAVE_FOLDER_TEXTS
    if (os.path.exists(docs_path)):
        shutil.rmtree(docs_path)



#============================================================================================
# @pytest.mark.test_save_texts
@pytest.mark.parametrize("test_email, folder, save_folder, expected", [ 
    (VALID_EMAIL,       VALID_FOLDER_TEXTS,       VALID_SAVE_FOLDER_TEXTS,      True),
    # (VALID_EMAIL,       VALID_FOLDER_TEXTS,       EMPTY_STR,                    True),
    # (NON_VALID_EMAIL,   VALID_FOLDER_TEXTS,       EMPTY_STR,                    False),
    # (NON_VALID_EMAIL,   NON_VALID_FOLDER,       EMPTY_STR,                      False),
    # (NON_VALID_EMAIL,   EMPTY_STR,              EMPTY_STR,                      False),
    # (VALID_EMAIL,       EMPTY_STR,              VALID_SAVE_FOLDER_TEXTS,      False),
    # (VALID_EMAIL,       NON_VALID_FOLDER,       VALID_SAVE_FOLDER_TEXTS,      False),
    # (EMPTY_STR,         EMPTY_STR,              VALID_SAVE_FOLDER_TEXTS,      False),
    # (EMPTY_STR,         VALID_FOLDER_TEXTS,       VALID_SAVE_FOLDER_TEXTS,      False),
    # (EMPTY_STR,         NON_VALID_FOLDER,       VALID_SAVE_FOLDER_TEXTS,      False),
])
def test_save_texts(test_email, folder, save_folder, expected):
    try:
        email = NON_VALID_EMAIL
        if (test_email == VALID_EMAIL):
            email = pkb_data_folder = personal_knowledge_base.config.read_config("IMAP_USER_NAME")
        # email = pkb_data_folder = personal_knowledge_base.config.read_config("IMAP_USER_NAME")
        response = client.get(f"http://localhost:8000/save_texts?username={email}&email_folder={folder}&save_folder={save_folder}")
        in_range = lambda x, min, max : (x >= min   and   x <max)
        assert(in_range(response.status_code, 200, 250) == expected)
        
    except:
        assert(False == expected)
