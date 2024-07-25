import os
import shutil
from flask.views import MethodView
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from App.llm_case import qianwen_llm
from .utils import get_all_files_in_directory, create_db, delete_db, modify_db, add_files_to_db, delete_files_from_db, \
    get_db
from .config import KNOWLEDGE_BASE_DIR, PERSIST_DIRECTORY
from flask import Blueprint, request

bp = Blueprint('rag', __name__)


def init_blueprint(app):
    bp.add_url_rule('/knowledge_base_files/', view_func=KnowledgeBaseFileView.as_view("file_view"))
    app.register_blueprint(blueprint=bp)


@bp.route('/knowledge_bases/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def knowledge_bases():
    result = {
        'code': 200,
        'result': 'success',
        'message': ''
    }
    if request.method == 'POST':
        """
            功能：新增知识库
            需要传的参数：
            knowledge_base_name：知识库名称
            files：文件参数名取为files
        """
        knowledge_base_name = request.form.get('knowledge_base_name')
        knowledge_base_path = os.path.join(KNOWLEDGE_BASE_DIR, knowledge_base_name)
        os.mkdir(knowledge_base_path)
        uploaded_files = request.files.getlist("files")
        for file in uploaded_files:
            file.save(os.path.join(knowledge_base_path, file.filename))
        # 进行文本嵌入
        create_db(directory=knowledge_base_path, embeddings_model=HuggingFaceEmbeddings(),
                  collection_name=knowledge_base_name)
        return result
    if request.method == 'DELETE':
        """
            功能：删除知识库
            需要传的参数：
            knowledge_base_name：知识库名称
        """
        knowledge_base_name = request.form.get('knowledge_base_name')
        knowledge_base_path = os.path.join(KNOWLEDGE_BASE_DIR, knowledge_base_name)
        # 删除数据库中该知识库的部分
        delete_db(persist_directory=PERSIST_DIRECTORY, embeddings_model=HuggingFaceEmbeddings(),
                  collection_name=knowledge_base_name)
        shutil.rmtree(knowledge_base_path)
        result['message'] = f'delete {knowledge_base_name} successfully'
        return result
    if request.method == 'PUT':
        """
            功能：修改知识库名称
            需要传的参数：
            old_knowledge_base_name
            new_knowledge_base_name
        """
        old_knowledge_base_name = request.form.get('old_knowledge_base_name')
        new_knowledge_base_name = request.form.get('new_knowledge_base_name')
        old_knowledge_base_path = os.path.join(KNOWLEDGE_BASE_DIR, old_knowledge_base_name)
        new_knowledge_base_path = os.path.join(KNOWLEDGE_BASE_DIR, new_knowledge_base_name)
        modify_db(new_name=new_knowledge_base_name, persist_directory=PERSIST_DIRECTORY,
                  collection_name=old_knowledge_base_name)
        os.rename(old_knowledge_base_path, new_knowledge_base_path)
        result['message'] = f'rename {old_knowledge_base_name} to {new_knowledge_base_name} successfully'
        return result
    if request.method == 'GET':
        """
            功能：查看知识库或查看指定
            需要传的参数：
            search_type: 0表示查看有哪些知识库，1表示查看指定知识库下有哪些文件
            knowledge_base_name
        """
        search_type = request.args.get('search_type')  # 获取查看类型
        if search_type == '0':
            dir_names = os.listdir(KNOWLEDGE_BASE_DIR)
            result['knowledge_base_names'] = dir_names
        if search_type == '1':
            knowledge_base_name = request.args.get('knowledge_base_name')
            knowledge_base_path = os.path.join(KNOWLEDGE_BASE_DIR, knowledge_base_name)
            file_names = get_all_files_in_directory(knowledge_base_path)
            result['file_names'] = file_names
            result['knowledge_base_name'] = knowledge_base_name
        return result


class KnowledgeBaseFileView(MethodView):
    result = {
        'code': 200,
        'result': 'success',
        'message': ''
    }

    def post(self):
        """
        功能：给指定的知识库上传文件
        参数：
            知识库名称
            文件files，支持多文件上传
        :return: result
        """
        knowledge_base_name = request.form.get('knowledge_base_name')
        if knowledge_base_name not in os.listdir(KNOWLEDGE_BASE_DIR):
            self.result['message'] = "知识库不存在"
            self.result['code'] = 400
            return self.result
        knowledge_base_path = os.path.join(KNOWLEDGE_BASE_DIR, knowledge_base_name)
        uploaded_files = request.files.getlist("files")
        for file in uploaded_files:
            file.save(os.path.join(knowledge_base_path, file.filename))
        file_paths = [os.path.join(knowledge_base_path, file.filename) for file in uploaded_files]
        add_files_to_db(file_paths, PERSIST_DIRECTORY, HuggingFaceEmbeddings(), knowledge_base_name)
        return self.result

    def delete(self):
        """
        功能：给指定的知识库删除文件
        参数：
            知识库名称
            文件file_names，支持多文件删除
        :return: result
        """
        knowledge_base_name = request.form.get('knowledge_base_name')
        knowledge_base_path = os.path.join(KNOWLEDGE_BASE_DIR, knowledge_base_name)
        file_names = request.form.getlist("file_names")
        file_paths = [os.path.join(knowledge_base_path, file_name) for file_name in file_names]
        delete_files_from_db(file_names, PERSIST_DIRECTORY, HuggingFaceEmbeddings(), knowledge_base_name)
        for file in file_paths:
            os.remove(file)
        return self.result

    def put(self):
        """
        功能：修改知识库中文件的内容
        参数：
            知识库名称
            old_file_name
            new_file
        :return: result
        """
        knowledge_base_name = request.form.get('knowledge_base_name')
        knowledge_base_path = os.path.join(KNOWLEDGE_BASE_DIR, knowledge_base_name)
        old_file_name = request.form.get('old_file_name')
        old_file_path = os.path.join(knowledge_base_path, old_file_name)
        new_file = request.files.get('new_file')
        new_file_path = os.path.join(knowledge_base_path, new_file.filename)
        os.remove(old_file_path)
        new_file.save(new_file_path)
        delete_files_from_db([old_file_name], PERSIST_DIRECTORY, HuggingFaceEmbeddings(), knowledge_base_name)
        add_files_to_db([new_file_path], PERSIST_DIRECTORY, HuggingFaceEmbeddings(), knowledge_base_name)
        return self.result

    def get(self):
        """
        功能：查看知识库中文件的内容
        参数：
            知识库名称
            file_name
        :return: result,result[file_content]携带文件内容
        """
        knowledge_base_name = request.args.get('knowledge_base_name')
        file_name = request.args.get('file_name')
        file_path = os.path.join(KNOWLEDGE_BASE_DIR, knowledge_base_name, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
        self.result['file_content'] = file_content
        return self.result


@bp.route('/chat/', methods=['POST'])
def chat():
    """
    :param:
        knowledge_base_name:选择的知识库名称
        k: 命中后topk作为提示词
        question: 提问
    :return: result['answer']
    """
    knowledge_base_name = request.form.get('knowledge_base_name')
    k = request.form.get('k')
    db = get_db(PERSIST_DIRECTORY, HuggingFaceEmbeddings(), knowledge_base_name)
    retriever = db.as_retriever(search_kwargs={'k': int(k)})
    # template = """你是一个问答任务的助手。
    # 只能根据以下检索到的上下文片段来回答这个问题，不要带有其他自己的答案。
    # 如果你不知道答案，就直接说不知道。
    # 尽量保持答案简洁。
    # Question: {question}
    # Context: {context}
    # Answer:
    # """
    template = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
                案。最多使用三句话。尽量使答案简明扼要。总是在回答的最后说“谢谢你的提问！”。
                {context}
                问题: {question}
                有用的回答:
"""
    prompt = PromptTemplate.from_template(template)
    llm = qianwen_llm()
    setup_and_retrieval = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    )
    rag_chain = (
            setup_and_retrieval
            | prompt
            | llm
            | StrOutputParser()
    )
    question = request.form.get('question')
    res = rag_chain.invoke(question)
    relevant_documents = retriever.get_relevant_documents(question)[0].page_content
    result = {
        'code': 200,
        'result': 'success',
        'message': '',
        'relevant_data': relevant_documents,
        'answer': res
    }
    return result
