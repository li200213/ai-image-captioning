import os
import time
import subprocess
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS # 导入跨域处理库

from model.all_history import add_history, show_history
from yiyan_api import single2txt
from model.check_login import is_existed, or_exist_user
from model.add_user import add_user

app = Flask(__name__, static_folder='') 
app.secret_key = 'YDWGBCQZ'

# 允许所有跨域请求 (Vue 前端必须)
CORS(app)


# ================== 1. 登录接口 ==================
@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        if is_existed(username, password):
            return jsonify({
                'code': 200, 
                'message': '登录成功',
                'data': {'username': username}
            })
        else:
            if or_exist_user(username):
                return jsonify({'code': 401, 'message': '密码错误'})
            else:
                return jsonify({'code': 404, 'message': '用户不存在'})
    except Exception as e:
        print(f"Login Error: {e}")
        return jsonify({'code': 500, 'message': '服务器内部错误'})


# ================== 2. 注册接口 ==================
@app.route('/api/register', methods=['POST'])
def api_register():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        if or_exist_user(username):
            return jsonify({'code': 409, 'message': '用户名已存在'})
        
        add_user(username, password)
        return jsonify({'code': 200, 'message': '注册成功'})

    except Exception as e:
        print(f"Register Error: {e}")
        return jsonify({'code': 500, 'message': '注册失败'})


# ================== 3. 上传图片并生成配文接口 ==================
@app.route('/api/upload', methods=['POST'])
def api_upload_and_generate():
    try:
        username = request.form.get('username')
        text_type = request.form.get('style')  
        emotion_type = request.form.get('emotion') 
        files = request.files.getlist('imgFile_list') 
 
        now_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        img_dir = os.path.join("user_private_dir", username, now_time)
        result_dir = os.path.join("result", username, now_time)

        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        img_src_list = [] # 存储相对路径，用于存数据库
        process_list = [] # 存储子进程处理并行多张图片
        txt_contents = [] # 存储所有生成的文本

        # 2. 遍历保存图片并启动 AI 进程
        for index, file in enumerate(files, start=1):
            filename = f"{index}.jpg"
            save_path = os.path.join(img_dir, filename)
            
            # 保存图片
            file.save(save_path)
            img_src_list.append(save_path) # user_private_dir/xx/xx.jpg

            # 结果 txt 路径
            result_txt_path = os.path.join(result_dir, f"{index}.txt")

            # 调用 clipcap_api.py 
            # 使用 sys.executable 确保使用当前环境的 python 解释器
            cmd = [sys.executable, 'clipcap_api.py', save_path, result_txt_path]
            
            # creationflags 让程序静悄悄地干活，不要弹窗
            creation_flags = 0
            if os.name == 'nt':
                creation_flags = subprocess.CREATE_NO_WINDOW 

            p = subprocess.Popen(cmd, creationflags=creation_flags)
            process_list.append((p, result_txt_path))

        # 3. 等待所有子进程结束
        for p, txt_path in process_list:
            p.wait() # 阻塞等待，直到该进程结束
            
            # 读取生成的 txt 内容
            if os.path.exists(txt_path):
                with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
                    txt_contents += f.read() + " "
            else:
                txt_contents += " " # 防止某个失败导致为空


        caption = single2txt(txt_contents, text_type, emotion_type)
        img_paths_str = ";".join(img_src_list)
        add_history(username, now_time, img_paths_str, text_type, emotion_type, caption)

        # 6. 返回结果给前端
        return jsonify({
            'code': 200,
            'message': '生成成功',
            'data': {
                'time': now_time,       
                'style': text_type,   
                'emotion': emotion_type, 
                'imgUrls': img_src_list,
                'caption': caption
            }
        })

    except Exception as e:
        print(f"Upload Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'code': 500, 'message': f'生成失败: {str(e)}'})


# ================== 4. 获取历史记录接口 ==================
@app.route('/api/history', methods=['GET'])
def api_get_history():
    try:
        username = request.args.get('username')

        history_list = show_history(username)
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': history_list
        })
    except Exception as e:
        print(f"History Error: {e}")
        return jsonify({'code': 500, 'message': '获取历史记录失败'})


if __name__ == "__main__":
    # host='0.0.0.0' 允许局域网访问
    app.run(debug=True, host='0.0.0.0', port=5000)