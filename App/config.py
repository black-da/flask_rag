import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, 'knowledge_base')
PERSIST_DIRECTORY = os.path.join(BASE_DIR, "chroma_db")


if __name__ == '__main__':
    print(PERSIST_DIRECTORY)