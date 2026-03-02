import base64
import os
import subprocess
import time
from flask import Flask,  request, json
from yiyan_api import single2txt

app = Flask(__name__,static_folder='') #达到前端从根目录访问的目的
app.secret_key = 'YDWGBCQZ'

@app.route('/')
def hello_world():
    return "hello"


@app.route('/call_api', methods=['POST'])
def call_api():
    username = json.loads(request.values.get('username'))
    img_base64 = json.loads(request.values.get('img_base64'))
    text_type = json.loads(request.values.get('text_type'))
    emotion = json.loads(request.values.get('emotion'))

    now = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
    img_file_dirpath = "user_private_dir/" + username + "/" + now
    result_file_dirpath = "result/" + username



    index = 1
    text = ""
    process_list = []
    for img in img_base64:
        decoded_bytes = base64.b64decode(img)  # base64解码
        if not os.path.exists(img_file_dirpath):
            os.makedirs(img_file_dirpath)
        img_file_path = img_file_dirpath + "/" + str(index) + ".jpg"
        with open(img_file_path,'w') as f:
            f.write(decoded_bytes)
        if not os.path.exists(result_file_dirpath):
            os.makedirs(result_file_dirpath)
        result_file_path = result_file_dirpath + str(index) + ".txt"
        p = subprocess.Popen(['python', 'clipcap_api.py',img_file_path,result_file_path,],creationflags=subprocess.CREATE_NEW_CONSOLE)
        process_list.append(p)
        index += 1

    finish_count = 0
    flag = False
    while 1:
        # 检查子进程是否结束
        for process in process_list:
            if process.poll() is not None:
                finish_count += 1
                if finish_count==len(process_list):
                    flag = True
                    break
        if flag:
            break
        finish_count = 0

    for i in range(1,index):
        with open(result_file_dirpath+"/"+str(i)+".txt",'r') as f:
            text += f.read()

    result = single2txt(text,text_type,emotion)
    result_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return json.dumps({'result_time':result_time,'result':result},ensure_ascii=False) #防止中文乱码
