import os
from flask import Flask, request
from dotenv import load_dotenv
from config import config
from flask_cors import CORS
from processor import processor


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
        print(text_chunks)

        # TODO save the text chunks to pinecone

        return {'code': 200, 'message': 'file processed successfully'}


# 返回与chatDPT交互信息
@app.route('/api/completion')
def chatgpt_completion():
    # put application's code here
    question = ''
    answer = ''
    return {'code': 200,  'message': 'success', 'data': {'question': question, 'answer': answer}}


def main():
    load_dotenv()
    app.run(port=os.getenv('PORT') or 10020, debug=True, host='0.0.0.0')
    app.logger.info('port')


if __name__ == '__main__':
    main()
