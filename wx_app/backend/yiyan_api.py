import requests
import json


def get_access_token():
    API_KEY = "7jfL7xi0iZqlWH4CGu0y50tc"
    SECRET_KEY = "yO4cjd88vLHV5xuqkxb3xNE2BidbnMqx"
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


def yiyan_chat(prompt):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "disable_search": False,
        "enable_citation": False
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    json_dict = json.loads(response.text)
    return json_dict["result"]


def single2txt(text,text_type, emotion):
    if emotion=='无': emotion=""
    prompt = f"我想要发一个微信朋友圈，拍摄的几张照片的内容是{text}，请帮我生成一段{emotion}{text_type}"
    result = yiyan_chat(prompt)
    print(result)
    return result






# with gr.Blocks() as demo:
#     gr.Markdown(
#     """
#     # 基于深度学习的看图配文朋友圈
#
#     上传一张图片，帮你生成朋友圈配文、写诗、吐槽，什么都行~
#     """)
#     # 输入
#     Img_input = gr.Image()
#
#     text_type = gr.Radio(["朋友圈配文", "七言绝句", "五言绝句", "诗歌", "小作文", "吐槽"], label="文本类型",value="朋友圈配文")
#     emotion = gr.Radio(["无", "开心的", "忧郁的", "孤独的", "疲惫的", "伤心的", "亢奋的"], label="情感",value="无")
#     # 输出
#     Text_output = gr.Text()
#     btn = gr.Button()
#     btn.click(fn=single2txt, inputs=[Img_input, text_type, emotion], outputs=[Text_output])
#
# demo.launch()
