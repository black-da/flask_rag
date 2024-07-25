import os
import chromadb
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter


def get_all_files_in_directory(directory_path):
    file_names = []
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            file_names.append(file)
    return file_names


def load_split_data(directory: str) -> list[Document]:
    file_names = get_all_files_in_directory(directory)
    file_paths = [os.path.join(directory, file_name) for file_name in file_names]
    docs = []
    for file_path in file_paths:
        doc_list = TextLoader(file_path=file_path, encoding='utf-8').load()
        for document in doc_list:
            document.metadata['file_name'] = os.path.basename(file_path)
        docs.extend(doc_list)
    text_splitter = CharacterTextSplitter(separator='\n',
                                          chunk_size=256,
                                          chunk_overlap=32,
                                          length_function=len)
    docs = text_splitter.split_documents(docs)
    return docs


def create_db(directory, embeddings_model, collection_name, persist_directory="./chroma_db"):
    """

    :param directory: 要进行文本嵌入的文件目录
    :param embeddings_model: 实例化后的嵌入模型
    :param collection_name: 知识库名称
    :param persist_directory: 数据库存储位置，默认./chroma_db
    :return: 向量数据库对象
    """
    docs = load_split_data(directory)
    Chroma.from_documents(docs, embeddings_model, collection_name=collection_name,
                          persist_directory=persist_directory)


def delete_db(persist_directory, embeddings_model, collection_name):
    db = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings_model,
        persist_directory=persist_directory,
    )
    db.delete_collection()


def modify_db(new_name, persist_directory, collection_name):
    persistent_client = chromadb.PersistentClient(path=persist_directory)
    collection = persistent_client.get_or_create_collection(collection_name)
    collection.modify(name=new_name)


def get_db(persist_directory, embeddings_model, collection_name):
    db = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings_model,
        persist_directory=persist_directory,
    )
    return db


def add_files_to_db(file_paths, persist_directory, embeddings_model, collection_name):
    db = get_db(persist_directory, embeddings_model, collection_name)
    docs = []
    for file_path in file_paths:
        doc_list = TextLoader(file_path=file_path, encoding='utf-8').load()
        for document in doc_list:
            document.metadata['file_name'] = os.path.basename(file_path)
        docs.extend(doc_list)
    text_splitter = CharacterTextSplitter(separator='\n',
                                          chunk_size=256,
                                          chunk_overlap=32,
                                          length_function=len)
    docs = text_splitter.split_documents(docs)
    db.add_documents(docs)


def delete_files_from_db(file_names, persist_directory, embeddings_model, collection_name):
    db = get_db(persist_directory, embeddings_model, collection_name)
    for file_name in file_names:
        ids = db.get(where={'file_name': file_name}).get('ids')
        db.delete(ids=ids)


if __name__ == '__main__':
    print(load_split_data(r'D:\code\PythonProjects\flask_study\flask_rag\knowledge_base\java'))
