import os
# import personal_knowledge_base.config
from personal_knowledge_base.config import global_config
# from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode
from pydantic import SecretStr

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from functools import cache

#----------------------------------------------------------------------------------------
# params: documents -  a list of documents, chunks from the texts, ready for QdrantVectorStore
#         docs_folder - the folder containing the original-documents
# return: the path to the QdrantVectorStore database
def produce_vectorestore(documents: list, docs_folder: str) -> str:
    sparse_embeddings = FastEmbedSparse(model_name=global_config.SPARSE_EMBEDDING_MODEL)
    API_KEY = global_config.openrouter_api_key

    embeddings = OpenAIEmbeddings(api_key=API_KEY, base_url=global_config.URL, model=global_config.EMBEDDING_MODEL)
    qdrant_db_path = docs_folder + "_qdrant_db"
    vectorstore = QdrantVectorStore.from_documents(
        documents=documents,
        embedding=embeddings,
        sparse_embedding=sparse_embeddings,
        collection_name=global_config.PKB_COLLECTION_NAME,
        path=qdrant_db_path,
        retrieval_mode=RetrievalMode.HYBRID,
    )

    return qdrant_db_path

#----------------------------------------------------------------------------------------
@cache
def _create_retriever():
    sparse_embeddings = FastEmbedSparse(model_name=global_config.SPARSE_EMBEDDING_MODEL)

    # API_KEY = s.openrouter_api_key
    API_KEY = global_config.openrouter_api_key
    embeddings = OpenAIEmbeddings(api_key=API_KEY, base_url=global_config.URL, model=global_config.EMBEDDING_MODEL)

    print("\ncreate_retriever(): QDRANT_DB_PATH = " + global_config.PKB_QDRANT_DB_PATH + "\n")
    if not os.path.exists(global_config.PKB_QDRANT_DB_PATH):
        return API_KEY, None

    # step 2:   Vektor-Store erstellen
    vectorstore = QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        sparse_embedding=sparse_embeddings,
        collection_name=global_config._PKB_COLLECTION_NAME,
        # path=s.QDRANT_DB_PATH,
        path=global_config.PKB_QDRANT_DB_PATH,
        retrieval_mode=RetrievalMode.HYBRID,
    )


    # step 3:  Retriever erstellen
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    return API_KEY, retriever


#----------------------------------------------------------------------------------------
def _format_docs(docs, prefix="=====\n"):
    return prefix + f"\n\n{prefix}".join(doc.page_content for doc in docs)

#----------------------------------------------------------------------------------------
def _build_prompt():
    system_prompt = (
        "Du bist ein hilfreicher Assistent. Nutze den folgenden Kontext, "
        "um die Frage zu beantworten. "
        "Wenn der Kontext keine relevanten Informationen enthält, sage: "
        "'Diese Information ist nicht in meinen Dokumenten enthalten.' "
        "Halte die Antwort kurz und prägnant. Nicht mehr als 1 Satz.\n\n"
        "Kontext:\n\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    return prompt

#----------------------------------------------------------------------------------------
# param: query - the question to be answered
# return: the answer to the question, based on the documents in the QdrantVector
def answer(query: str):
    print("create_rag_chain(): query = " + query)

    API_KEY, retriever = _create_retriever()
    if (retriever == None):
        return "ERROR: no retriever, probably qdrant_db file doesn't exist!", False      

    # step 4:  Dokumente formatieren
    docs_found = retriever.invoke(query)

    # step 5:  Retrieval-Chain bauen
    retrieval_chain = retriever | _format_docs
    context_text = retrieval_chain.invoke(query)
    print("context_text: " + context_text)
    print("step 5")

    # step 6:  Prompt bauen
    print("step 6")
    prompt = _build_prompt()

    # step 7:  LLM-Chain bauen
    MINISTRAL = "qwen/qwen3-30b-a3b-instruct-2507"
    llm = ChatOpenRouter(
        api_key=API_KEY,
        model=MINISTRAL,
        temperature=0,
    )

    rag_chain = (
        {"context": retrieval_chain, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    print("step 7")

    # step 8:  RAG-Chain ausführen
    answer = rag_chain.invoke(query)
    print("Answer: " + answer)
    return answer, True


