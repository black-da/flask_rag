from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from App.config import PERSIST_DIRECTORY


db = Chroma(
    persist_directory=PERSIST_DIRECTORY,
    collection_name="java",
    embedding_function=HuggingFaceEmbeddings()
)
retriever = db.as_retriever()
print('普通检索：', end=' ')
print(retriever.invoke('Java是如何实现跨平台性的？'))

print('根据metadata检索text1：', end=' ')
t1 = db.get(where={'source': r'D:\code\PythonProjects\flask_study\flask_rag\knowledge_base\java\text1.txt'})
print(t1)
# print('text1的长度为这里是字典的长度',  len(t1))  # 这里是字典的长度，所以t1,t2和t的长度才一样
print('text1的长度为',  len(t1.get('ids')))

print('根据metadata检索text2：', end=' ')
t2 = db.get(where={'file_name': 'text2.txt'})
print(t2)
# print('text2的长度为',  len(t2))
print('text2的长度为',  len(t2.get('ids')))

print('根据id检索：', end=' ')
print(db.get(ids=['1']))

print('用get函数打印全部：', end=' ')
t = db.get()
print(t)
print(len(t.get('ids')))
