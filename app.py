import os
import pinecone
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from config import config
from flask_cors import CORS
from typing import List
from langchain.vectorstores.pinecone import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from langchain.schema import Document
from processor import processor

OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV = os.getenv('PINECONE_ENV')
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')

# 配置日志信息
config.setup_log()
# 创建flask对象
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000  # Max 16MB
# SocketIO(app, cors_allowed_origins='*') 配置跨域请求
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)


@app.route('/api/health')
def health():
    return {'code': 200, 'message': 'success'}


# 测试用上传文件html，TODO 删除此接口
@app.route('/', methods=['GET'])
def upload():
    return '''
    <!doctype html>
    <title>Processing TXT and PDF</title>
    <h1>Upload new File</h1>
    <form method=post action='/api/file-process' enctype=multipart/form-data>
      <input type=file name=file accept='.txt,.pdf'>
      <input type=submit value=Upload>
    </form>
    '''


# 文件处理接口
@app.route('/api/file-process', methods=['POST'])
def file_processor():
    if 'file' not in request.files:
        return {'code': 400, 'message': 'No file part'}
    
    file = request.files['file']
    if file.filename == '':
        return {'code': 400, 'message': 'No selected file'}
    
    if file and processor.allowed_file(file.filename):
        text = ''
        if (file.filename.endswith('.pdf')):
            text = processor.get_pdf_text(file)
        elif (file.filename.endswith('.txt')):
            text = file.read().decode('utf-8')

        # get the text chunks
        text_chunks = processor.get_text_chunks(text)

        # save the text chunks to pinecone
        metadatas = [{'fileName': file.filename, 'page': i} for i in range(len(text_chunks))]
        embeddings = OpenAIEmbeddings(openai_api_key=OPEN_AI_KEY)
        Pinecone.from_texts(
            text_chunks,
            embeddings,
            index_name=PINECONE_INDEX_NAME,
            metadatas=metadatas,
            namespace='default'
        )

        return {'code': 200, 'message': 'file processed successfully'}

@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()
    question = data.get('question', '')
    if question.strip() == '':
        return jsonify({'code': 400, 'message': 'question is empty'}), 400

    db = Pinecone.from_existing_index(
        PINECONE_INDEX_NAME,
        embedding=OpenAIEmbeddings(openai_api_key=OPEN_AI_KEY),
        text_key='text',
        namespace='default'
    )
    retriever = db.as_retriever(search_kwargs={'k': 3})
    docs = retriever.get_relevant_documents(question)
    
    answers = [{'content': doc.page_content, 'metadata': doc.metadata} for doc in docs]
    return {'code': 200, 'message': 'success', 'answers': answers}

# def parse_docs(docs: List[Document], all_meta: bool = False) -> None:
#     for doc in docs:
#         assert doc.page_content
#         assert doc.metadata
#         main_meta = {"Published", "Title", "Authors", "Summary"}
#         assert set(doc.metadata).issuperset(main_meta)
#         if all_meta:
#             assert len(set(doc.metadata)) > len(main_meta)
#         else:
#             assert len(set(doc.metadata)) == len(main_meta)

# 返回与chatDPT交互信息
@app.route('/api/completion', methods=['POST'])
def chatgpt_completion():
    data = request.get_json()
    question = data.get('question', '')
    if question.strip() == '':
        return jsonify({'code': 400, 'message': 'question is empty'}), 400

    chat_history = data.get('chat_history', [])
    
    db = Pinecone.from_existing_index(
        PINECONE_INDEX_NAME,
        embedding=OpenAIEmbeddings(openai_api_key=OPEN_AI_KEY),
        text_key='text',
        namespace='default'
    )
    retriever = db.as_retriever(search_kwargs={'k': 3})
    qa = ConversationalRetrievalChain.from_llm(
        llm=OpenAI(openai_api_key=OPEN_AI_KEY),
        retriever=retriever
    )
    result = qa({"question": question, 'chat_history': chat_history})

    return {'code': 200, 'message': 'success', 'answer': result['answer']}


def pinecone_setup():
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENV,
    )

def main():
    load_dotenv()
    pinecone_setup()
    app.run(port=os.getenv('PORT') or 10020, debug=True, host='0.0.0.0')
    app.logger.info('port')


if __name__ == '__main__':
    main()
