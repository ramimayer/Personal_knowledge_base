from unittest import TestCase
from personal_knowledge_base.web_service import rag, save_attachments
import requests
import pytest
import os
from pathlib import Path
import shutil

#  shell-command:  pytest .\test_web_service.py -W ignore::DeprecationWarning --cov=../src --cov-report term-missing

# gobal parameters for tests-parametrization
VALID_EMAIL = "rami.mayer@yahoo.com"
NON_VALID_EMAIL = "ram.mayer@yahoo.com"
NON_VALID_FOLDER = "Bad_Folder"
USE_DEFAULT_SAVE_FOLDER = ""
VALID_FOLDER_ATTACHMENTS = "Simulator_2015_eng"
VALID_FOLDER_TEXTS = "CodingAcademy"

VALID_SAVE_FOLDER_ATTACHMENTS = "docs_orig_format"
VALID_SAVE_FOLDER_TEXTS = "txt_msgs"
# VALID_SAVE_FOLDER_ATTACHMENTS = "C:/Users/ramim/Documents/projects/data/new_orig_format"
# VALID_SAVE_FOLDER_TEXTS = "C:/Users/ramim/Documents/projects/data/txt_msgs"


DEFAULT_SAVE_FOLDER = "C:/Users/ramim/Documents/projects/data/docs_orig_format"
EMPTY_STR = ""


@pytest.fixture(autouse=True)
def delete_created_folders():
    # default_path = Path("C:/Users/ramim/Documents/projects/data/docs_orig_format")
    default_path = DEFAULT_SAVE_FOLDER

    if (os.path.exists(default_path)):
        shutil.rmtree(default_path)

    # docs_path = Path("C:/Users/ramim/Documents/projects/data/new_orig_format")
    docs_path = VALID_SAVE_FOLDER_ATTACHMENTS
    if (os.path.exists(docs_path)):
        shutil.rmtree(docs_path)

    docs_path = VALID_SAVE_FOLDER_TEXTS
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
    response = requests.get(f"http://localhost:8000/save_attachments?username={email}&email_folder={folder}&save_folder={save_folder}")
    in_range = lambda x, min, max : (x >= min   and   x <max)
    assert(in_range(response.status_code, 200, 250) == expected)


#============================================================================================
# @pytest.mark.test_save_texts
@pytest.mark.parametrize("email, folder, save_folder, expected", [ 
    # (VALID_EMAIL,       VALID_FOLDER_TEXTS,       VALID_SAVE_FOLDER_TEXTS,      True),
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
def test_save_texts(email, folder, save_folder, expected):
    response = requests.get(f"http://localhost:8000/save_texts?username={email}&email_folder={folder}&save_folder={save_folder}")
    in_range = lambda x, min, max : (x >= min   and   x <max)
    assert(in_range(response.status_code, 200, 250) == expected)


#============================================================================================
# @pytest.mark.test_create_vectorestore
@pytest.mark.parametrize("docs_folder, expected", [ 
    ("test_attachments_new", True),
])
def test_create_vectorestore(docs_folder, expected):
    response = requests.get(f"http://localhost:8000/create_vectorestore/{docs_folder}")
    in_range = lambda x, min, max : (x >= min   and   x <max)
    assert(in_range(response.status_code, 200, 250) == expected)


#============================================================================================
# @pytest.mark.test_query_rag
@pytest.mark.parametrize("query, expected", [ 
    # ("what is the oil-pressure range of a c-500?", ["zwischen", "35", "70", True]),
    # ("what is the oil-pressure range of a c-500?", ["zwischen", "135", "70", False]),
])
def test_query_rag(query, expected):
    response = requests.get(f"http://localhost:8000/query_rag/{query}")
    

    print("test_query_rag(): status_code = " + str(response.status_code))

    in_range = lambda x, min, max : (x >= min   and   x <max)
    assert(in_range(response.status_code, 200, 250) == True)

    j = response.json()
    answer = str(j["answer"])

    # check for a string that we know doesn't exist in the answere
    find_bad = answer.find("blablabla_its_not_a_reasonable_string")
    assert(find_bad == -1)

    all_words_are_in_answer = True;
    for w in expected[:-1]:
        word_is_in_answer = (answer.find(w) > 0)
        if (word_is_in_answer == False):
            all_words_are_in_answer = False

    assert(all_words_are_in_answer == (expected[-1]))
