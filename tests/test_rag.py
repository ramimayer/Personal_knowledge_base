import pytest
from fastapi.testclient import TestClient
from personal_knowledge_base.web_service import rag
client = TestClient(rag)

#  ----  lobal test variables -  CHANGE thenm to suite your computer !!   -------------
NOT_IN_MY_DOCS_MSG = ["nicht ", "meinen ", "Dokumenten ", "enthalten", True]

#============================================================================================
# @pytest.mark.test_query_rag
def all_expected_words_in_answer(expected: list, answer: str) -> bool:
    words_in_answer = answer.lower().split()
    one_expected_not_in_answer = False;
    for e in expected[:-1]:
        e = e.lower()
        found_in_answer = False;
        for w in words_in_answer:
            word_partly_in_answer = (w in e) or (e in w)          
            if (word_partly_in_answer == True):
                found_in_answer = True

        if (found_in_answer == False):
            one_expected_not_in_answer = True
            break

    return not one_expected_not_in_answer

@pytest.mark.parametrize("query, expected", [ 
    ("what is the oil-pressure range of a c-500?", ["zwischen", "35", "70", True]),
    ("what is the oil-pressure range of a cessna 172?", NOT_IN_MY_DOCS_MSG),
    # ("what is the oil-pressure range of a mooney?", NOT_IN_MY_DOCS_MSG),
    # ("who is the PM of New Zealand?", NOT_IN_MY_DOCS_MSG),
    # ("In Emergency restart, what is Maximum start ITT?", ["Start-ITT", "maximale ", "700", True]),
    # ("In Emergency restart, what is Maximum start ITT?", ["Start-ITT", "maximale ", "705", False]),
    # ("who is responsible for flight-planning?", ["captain", "verantwortlich", "ist", True]),
    # ("can a child fly the plane?", NOT_IN_MY_DOCS_MSG),
])
def test_query_rag(query, expected):
    response = client.get(f"http://localhost:8000/query_rag/{query}")
    

    print("test_query_rag(): status_code = " + str(response.status_code))

    in_range = lambda x, min, max : (x >= min   and   x <max)
    assert(in_range(response.status_code, 200, 250) == True)

    j = response.json()
    answer = str(j["answer"])
    ret_code = j["rc"] 
    print("test_query_rag(): ret_code = " + str(ret_code))
    assert(ret_code != False)

    # check for a string that we know doesn't exist in the answere
    find_bad = answer.find("blablabla_its_not_a_reasonable_string")
    assert(find_bad == -1)

    found_in_answer = all_expected_words_in_answer(expected, answer)
    print("test_query_rag(): found_in_answer = " + str(found_in_answer))
    assert(found_in_answer == (expected[-1]))
