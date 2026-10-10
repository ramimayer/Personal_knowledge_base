# 

from langchain_community.document_loaders import TextLoader, DirectoryLoader

# import personal_knowledge_base.langchain_utils
# import os
from pathlib import Path


# for chunking
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)
import personal_knowledge_base.pdf_utils
import personal_knowledge_base.word_utils

#----------------------------------------------------------------------------------------
def split_all_files_to_chunks(txt_folder: str, chunks_folder: str) -> list:
    # load all the ".txt" files in the folder
    print("\n\nsplit_all_files_to_chunks():  txt_folder = " +  txt_folder + "\n\n")
    loader = DirectoryLoader(
        txt_folder,
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    print("bfr loader.load()")
    raw_documents = loader.load()
    print("aftr loader.load()")

    # split the raw_documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    documents = text_splitter.split_documents(raw_documents)
    print("num_chunks = " + str(len(documents)) + "\n\n")

    # save the chunks in a folder called "foldername_chunks"
    Path(chunks_folder).mkdir(parents=True, exist_ok=True)
    n = 0
    for d in documents:
        chunk_file_path = chunks_folder + "/chunk_" + str(n) + ".txt"
        n = n + 1
        with open(chunk_file_path, "w", encoding="utf-8") as f:
            f.write(d.page_content)

    return documents

#----------------------------------------------------------------------------------------
# write a function that loads all the PDF documents in a directory, and writes their content as a text-file
def convert_to_txt(folder: str, save_folder: str):
    print("convert_to_txt(): folder = " + folder + ",  save_folder = " + save_folder)

    READ_FOLDER = folder
    SAVE_FOLDER = save_folder
    Path(save_folder).mkdir(parents=True, exist_ok=True)

    folder_to_txt(READ_FOLDER, SAVE_FOLDER)

#----------------------------------------------------------------------------------------
def folder_to_txt(folder:str, output_folder:str):
    print("folder_to_txt(): folder = " + folder)
    pathlist = Path(folder).glob('**/*.*')
    for file_path in pathlist:
        # because path is object not string
        file_name_full_path = str(file_path)


        path_parts = file_name_full_path.split("\\")
        file_name = path_parts[len(path_parts) - 1] 
        name_parts = file_name.split(".")
        file_suffix = name_parts[len(name_parts) - 1]
        
        if (file_suffix == "pdf"):
            print("\nPDF:  file_name_full_path = " + file_name_full_path + ", file_name = " + file_name + ", file_suffix = " + file_suffix)
            personal_knowledge_base.pdf_utils.pdf_to_txt(file_name_full_path, file_name, output_folder)
        elif (file_suffix == "docx"):
            print("DOCX:  file_name_full_path = " + file_name_full_path + ", file_name = " + file_name + ", file_suffix = " + file_suffix)
            personal_knowledge_base.word_utils.docx_to_txt(file_name_full_path, file_name, output_folder)
        elif (file_suffix == "doc"):
            print("DOC:  file_name_full_path = " + file_name_full_path + ", file_name = " + file_name + ", file_suffix = " + file_suffix)
            personal_knowledge_base.word_utils.doc_to_txt(file_name_full_path, file_name, output_folder)
            pass
        elif (file_suffix == "txt"):
            # Path(output_folder).copy(file_name_full_path, output_folder + "/" + file_name + ".txt")
            output_file = Path(output_folder + "/" + file_name)
            print("output_file = " + str(output_file))
            Path(file_name_full_path).copy(output_file)

            print("TXT:  file_name_full_path = " + file_name_full_path + ", file_name = " + file_name + ", file_suffix = " + file_suffix)
            pass
        else:
            print("NOT PDF:  file_name_full_path = " + file_name_full_path + ", file_name = " + file_name + ", file_suffix = " + file_suffix)
            pass

  