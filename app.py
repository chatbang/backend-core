from flask import Flask
from config import config
from flask_cors import CORS

# 配置日志信息
config.setup_log()
# 创建flask对象
app = Flask(__name__)
# SocketIO(app, cors_allowed_origins='*') 配置跨域请求
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)


# 上传文件
@app.route('/uploadFile')
def upload_file():
    # put application's code here
    return {"code": "200", "message": "file upload success"}


# 返回与chatDPT交互信息
@app.route('/chatBang')
def chat_bang():
    # put application's code here
    question = ""
    answer = ""
    return {"code": "200",  "message": "success", "data": {"question": question, "answer": answer}}


if __name__ == '__main__':
    app.run(port=10020, debug=True, host='0.0.0.0')
    app.logger.info('port')
