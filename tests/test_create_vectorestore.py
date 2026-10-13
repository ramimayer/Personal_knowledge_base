
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
DOCS_FOLDER = "test_attachments_new"

#============================================================================================
@pytest.fixture(autouse=True)
def delete_created_folders():
    pkb_data_folder = personal_knowledge_base.config.read_config("PKB_DATA_FOLDER")
    if not pkb_data_folder:
        print("delete_created_folders():  bad PKB_DATA_FOLDER")
        return

    # docs_path = pkb_data_folder + "/" + VALID_SAVE_FOLDER_TEXTS
    # if (os.path.exists(docs_path)):
    #     shutil.rmtree(docs_path)

#============================================================================================
# @pytest.mark.test_create_vectorestore
@pytest.mark.parametrize("docs_folder, expected", [ 
    (DOCS_FOLDER, True),
])
def test_create_vectorestore(docs_folder, expected):
    try:
        response = client.get(f"http://localhost:8000/create_vectorestore/{docs_folder}")
        in_range = lambda x, min, max : (x >= min   and   x <max)
        assert(in_range(response.status_code, 200, 250) == expected)
            
    except:
        assert(False == expected)
