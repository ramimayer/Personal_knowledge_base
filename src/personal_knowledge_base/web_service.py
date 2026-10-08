import os

from dotenv import load_dotenv
from fastapi import FastAPI, Path
import personal_knowledge_base.mail_utils
import personal_knowledge_base.docs_utils
from pydantic import BaseModel
from typing import Annotated
from fastapi import Depends, Query
from pydantic import Field
from personal_knowledge_base.docs_utils import folder_to_txt
import personal_knowledge_base.rag 

class ServerData(BaseModel):
    username: str
    email_folder: str
    save_folder: str

rag = FastAPI()

# usage:   http://localhost:8000/save_attachments?username=rami.mayer@yahoo.com&email_folder=Simulator_2015_eng&save_folder=att
@rag.get("/save_attachments")
def save_attachments(username: str = Query(..., description="email of the user"), 
                     email_folder: str = Query(..., description="mail-folder to process"),
                     save_folder: str = Query(..., description="mail-folder to process")
                     ):
    print("web_service: save_attachments()    " + "username: " + username + ", email_folder: " + email_folder)

    # sanity input-check
    illegal_filename_symbols = ["/", "\\", "\"", "?", ":", "?", ":", ":"]
    for s in illegal_filename_symbols:
        if (s in save_folder):
            return {"message": "Illegal folder-name!   " + save_folder}

    load_dotenv()
    PKB_DATA_FOLDER = os.getenv("PKB_DATA_FOLDER")
    if not PKB_DATA_FOLDER:
        raise RuntimeError("PKB_DATA_FOLDER is not set")
    ATTACHMENTS_SAVE_FOLDER = PKB_DATA_FOLDER + "/" + save_folder
    if not os.path.exists(PKB_DATA_FOLDER):
        raise RuntimeError("The data-folder  DOESN'T exist! " + PKB_DATA_FOLDER)

    # call mail_utils function to do the job, and return the appropriate message       
    success = personal_knowledge_base.mail_utils.save_attachments(username, email_folder, ATTACHMENTS_SAVE_FOLDER)
    if not success:
         raise RuntimeError("save_attachments():  Failiure to write the files !")
         return {"message": "Failiure to connect to mail-folder!"}

    return {"message": "Saving attachments!"}

#  usage:  "http://localhost:8000/save_texts?username=rami.mayer@yahoo.com&email_folder=CodingAcademy&save_folder=msgs"
@rag.get("/save_texts")
def save_texts(server_data: ServerData = Depends()):
    print("web_service: save_texts()")
    print("server_data = {" + server_data.username + ",  " + server_data.email_folder + ",  " + server_data.save_folder)

    load_dotenv()
    PKB_DATA_FOLDER = os.getenv("PKB_DATA_FOLDER")
    if not PKB_DATA_FOLDER:
        raise RuntimeError("PKB_DATA_FOLDER is not set")
    MESSAGES_SAVE_FOLDER = PKB_DATA_FOLDER + "/" + server_data.save_folder
    if not os.path.exists(PKB_DATA_FOLDER):
        raise RuntimeError("The folder where messages should save DOESN'T exist! " + PKB_DATA_FOLDER)
    
    personal_knowledge_base.mail_utils.save_texts(server_data.username, server_data.email_folder, MESSAGES_SAVE_FOLDER)
    return {"message": "Saving texts!"}


# usage:   http://localhost:8000/query_rag/what%20is%20instrument%20flying
@rag.get("/query_rag/{query}")
def query_rag(query: Annotated[str, Path(min_length=1)]):
    print("web_service: query_rag()" + "query = " + query)
    answer = personal_knowledge_base.rag.answer(query)
    return {"answer": answer}


# usage:   http://localhost:8000/create_vectorestore/foldername
@rag.get("/create_vectorestore/{docs_folder}")
def create_vectorestore(docs_folder: Annotated[str, Path(min_length=1)]):
    print("web_service: create_vectorestore()" + "docs_folder = " + docs_folder)
    load_dotenv()
    PKB_DATA_FOLDER = os.getenv("PKB_DATA_FOLDER")
    if not PKB_DATA_FOLDER:
        raise RuntimeError("PKB_DATA_FOLDER is not set")

    docs_folder = PKB_DATA_FOLDER + "/" + docs_folder
    txt_folder = docs_folder + "_txt"
    chunks_folder = docs_folder + "_chunks"

    personal_knowledge_base.docs_utils.convert_to_txt(docs_folder, txt_folder)
    documents = personal_knowledge_base.docs_utils.split_all_files_to_chunks(txt_folder, chunks_folder)
    qdrant_db_path = personal_knowledge_base.rag.produce_vectorestore(documents, docs_folder)

    return {"message": "vectorestore created !!    " + "qdrant_db_path = " + qdrant_db_path}

