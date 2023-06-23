# backend-core
This is the backend core module of the Chatbang.

> 注意：Python版本需为>=3.8.1

重命名根目录里的`env.ini.example`为`env.ini`，并更新对应的values

## 安装依赖

`pip3 install -r requirements.txt`

## 运行应用

`python app.py`

> 默认端口为`10020`，启动程序后可访问`http://localhost:10020/api/health`，如返回的`code`为`200`则说明运行成功。
