# from personal_knowledge_base.web_service import rag
import pytest
import os
# from pathlib import Path
# from dotenv import load_dotenv
import shutil
import personal_knowledge_base.config 

from fastapi.testclient import TestClient
from personal_knowledge_base.web_service import rag
client = TestClient(rag)

#  shell-command:  pytest .\test_web_service.py -W ignore::DeprecationWarning --cov=../src --cov-report term-missing

# config parameters for tests - set YOUR OWN before testing !!
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
    (VALID_EMAIL,       VALID_FOLDER_ATTACHMENTS,       VALID_SAVE_FOLDER_ATTACHMENTS,      True),
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


# #============================================================================================
# # @pytest.mark.test_save_texts
# @pytest.mark.parametrize("email, folder, save_folder, expected", [ 
#     (VALID_EMAIL,       VALID_FOLDER_TEXTS,       VALID_SAVE_FOLDER_TEXTS,      True),
#     # (VALID_EMAIL,       VALID_FOLDER_TEXTS,       EMPTY_STR,                    True),
#     # (NON_VALID_EMAIL,   VALID_FOLDER_TEXTS,       EMPTY_STR,                    False),
#     # (NON_VALID_EMAIL,   NON_VALID_FOLDER,       EMPTY_STR,                      False),
#     # (NON_VALID_EMAIL,   EMPTY_STR,              EMPTY_STR,                      False),
#     # (VALID_EMAIL,       EMPTY_STR,              VALID_SAVE_FOLDER_TEXTS,      False),
#     # (VALID_EMAIL,       NON_VALID_FOLDER,       VALID_SAVE_FOLDER_TEXTS,      False),
#     # (EMPTY_STR,         EMPTY_STR,              VALID_SAVE_FOLDER_TEXTS,      False),
#     # (EMPTY_STR,         VALID_FOLDER_TEXTS,       VALID_SAVE_FOLDER_TEXTS,      False),
#     # (EMPTY_STR,         NON_VALID_FOLDER,       VALID_SAVE_FOLDER_TEXTS,      False),
# ])
# def test_save_texts(email, folder, save_folder, expected):
#     try:
#         response = client.get(f"http://localhost:8000/save_texts?username={email}&email_folder={folder}&save_folder={save_folder}")
#         in_range = lambda x, min, max : (x >= min   and   x <max)
#         assert(in_range(response.status_code, 200, 250) == expected)
        
#     except:
#         assert(False == expected)


# #============================================================================================
# # @pytest.mark.test_create_vectorestore
# @pytest.mark.parametrize("docs_folder, expected", [ 
#     # ("test_attachments_new", True),
# ])
# def test_create_vectorestore(docs_folder, expected):
#     response = client.get(f"http://localhost:8000/create_vectorestore/{docs_folder}")
#     in_range = lambda x, min, max : (x >= min   and   x <max)
#     assert(in_range(response.status_code, 200, 250) == expected)


#============================================================================================
# @pytest.mark.test_query_rag
# def all_expected_words_in_answer(expected: list, answer: str) -> bool:
#     words_in_answer = answer.lower().split()
#     one_expected_not_in_answer = False;
#     for e in expected[:-1]:
#         e = e.lower()
#         found_in_answer = False;
#         for w in words_in_answer:
#             word_partly_in_answer = (w in e) or (e in w)          
#             if (word_partly_in_answer == True):
#                 found_in_answer = True

#         if (found_in_answer == False):
#             one_expected_not_in_answer = True
#             break

#     return not one_expected_not_in_answer

# @pytest.mark.parametrize("query, expected", [ 
#     # ("what is the oil-pressure range of a c-500?", ["zwischen", "35", "70", True]),
#     # ("what is the oil-pressure range of a cessna 172?", NOT_IN_MY_DOCS_MSG),
#     # ("what is the oil-pressure range of a mooney?", NOT_IN_MY_DOCS_MSG),
#     # ("who is the PM of New Zealand?", NOT_IN_MY_DOCS_MSG),
#     # ("In Emergency restart, what is Maximum start ITT?", ["Start-ITT", "maximale ", "700", True]),
#     # ("In Emergency restart, what is Maximum start ITT?", ["Start-ITT", "maximale ", "705", False]),
#     # ("who is responsible for flight-planning?", ["captain", "verantwortlich", "ist", True]),
#     # ("can a child fly the plane?", NOT_IN_MY_DOCS_MSG),
# ])
# def test_query_rag(query, expected):
#     response = client.get(f"http://localhost:8000/query_rag/{query}")
    

#     print("test_query_rag(): status_code = " + str(response.status_code))

#     in_range = lambda x, min, max : (x >= min   and   x <max)
#     assert(in_range(response.status_code, 200, 250) == True)

#     j = response.json()
#     answer = str(j["answer"])
#     ret_code = j["rc"] 
#     print("test_query_rag(): ret_code = " + str(ret_code))
#     assert(ret_code != False)

#     # check for a string that we know doesn't exist in the answere
#     find_bad = answer.find("blablabla_its_not_a_reasonable_string")
#     assert(find_bad == -1)

#     found_in_answer = all_expected_words_in_answer(expected, answer)
#     print("test_query_rag(): found_in_answer = " + str(found_in_answer))
#     assert(found_in_answer == (expected[-1]))
