import pytest
import os
import shutil
import personal_knowledge_base.config 

from fastapi.testclient import TestClient
from personal_knowledge_base.web_service import rag
client = TestClient(rag)

#  shell-command:  pytest .\test_web_service.py -W ignore::DeprecationWarning --cov=../src --cov-report term-missing

#  ----  global test variables -  CHANGE thenm to suite your computer !!   -------------
VALID_EMAIL = "rami.mayer@yahoo.com"
NON_VALID_EMAIL = "ram.mayer@yahoo.com"
NON_VALID_FOLDER = "Bad_Folder"
USE_DEFAULT_SAVE_FOLDER = ""
VALID_FOLDER_ATTACHMENTS = "Simulator_2015_eng"
VALID_FOLDER_TEXTS = "CodingAcademy"

VALID_SAVE_FOLDER_ATTACHMENTS = "docs_orig_format"
VALID_SAVE_FOLDER_TEXTS = "txt_msgs"

DEFAULT_SAVE_FOLDER = "C:/Users/ramim/Documents/projects/data/docs_orig_format"
EMPTY_STR = ""
NOT_IN_MY_DOCS_MSG = ["nicht ", "meinen ", "Dokumenten ", "enthalten", True]
#==========================================================================================


@pytest.fixture(autouse=True)
def delete_created_folders():
    pkb_data_folder = personal_knowledge_base.config.read_config("PKB_DATA_FOLDER")
    if not pkb_data_folder:
        print("delete_created_folders():  bad PKB_DATA_FOLDER")
        return

    default_path = pkb_data_folder + "/" + VALID_SAVE_FOLDER_ATTACHMENTS
    if (os.path.exists(default_path)):
        shutil.rmtree(default_path)

    docs_path = pkb_data_folder + "/" + VALID_SAVE_FOLDER_TEXTS
    if (os.path.exists(docs_path)):
        shutil.rmtree(docs_path)


#============================================================================================
# @pytest.mark.test_save_attachments
@pytest.mark.parametrize("email, folder, save_folder, expected", [ 
    # (VALID_EMAIL,       VALID_FOLDER_ATTACHMENTS,       VALID_SAVE_FOLDER_ATTACHMENTS,      True),
    # (VALID_EMAIL,       VALID_FOLDER_ATTACHMENTS,       EMPTY_STR,                          True),
    # (NON_VALID_EMAIL,   VALID_FOLDER_ATTACHMENTS,       EMPTY_STR,                          False),
    # (NON_VALID_EMAIL,   NON_VALID_FOLDER,               EMPTY_STR,                          False),
    # (NON_VALID_EMAIL,   EMPTY_STR,                      EMPTY_STR,                          False),
    # (VALID_EMAIL,       EMPTY_STR,                      VALID_SAVE_FOLDER_ATTACHMENTS,      False),
    # (VALID_EMAIL,       NON_VALID_FOLDER,               VALID_SAVE_FOLDER_ATTACHMENTS,      False),
    # (EMPTY_STR,         EMPTY_STR,                      VALID_SAVE_FOLDER_ATTACHMENTS,      False),
    # (EMPTY_STR,         VALID_FOLDER_ATTACHMENTS,       VALID_SAVE_FOLDER_ATTACHMENTS,      False),
    # (EMPTY_STR,         NON_VALID_FOLDER,               VALID_SAVE_FOLDER_ATTACHMENTS,      False),
])


def test_save_attachments(email, folder, save_folder, expected):
    response = client.get(f"http://localhost:8000/save_attachments?username={email}&email_folder={folder}&save_folder={save_folder}")
    print("print:  test_save_attachments():  after client.get()")

    j = response.json()
    message = str(j["message"])
    ret_code = j["rc"] 
    if (not ret_code):
        print("test_save_attachments(): message = " + message)

    print("expected = " + str(expected))
    assert(ret_code == expected)
    
    in_range = lambda x, min, max : (x >= min   and   x <max)
    assert(in_range(response.status_code, 200, 250) == True)

