import sys

import paddle
from clipcap import GPTTokenizer, CLIPProcessor, CLIPModel, ClipCaptionModel, img2text
import numpy as np
from PIL import Image


prefix_length = 10
#加载预训练模型gpt2的tokenizer，将输入文本分词成一个个token(最小语义单元)。
lm_tokenizer = GPTTokenizer.from_pretrained('gpt2-medium-en')
#加载预训练的 CLIP 模型和处理器
clip_preprocess = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
#初始化ClipCap模型
model = ClipCaptionModel(10, clip_length=10, prefix_size=512,num_layers=8)
#将预训练好的模型参数加载到当前模型中
model.set_state_dict(paddle.load("-epoch_last.pdparams"))

def clipcap_main(img_temp):
    try:
        img = np.array(img_temp)
        pil_image = img[:,:,::-1]
    except:
        return "图片处理发生错误，请检查图片内容"
    # 调用图片转文本接口
    text = img2text(pil_image,
                    prefix_length=prefix_length,
                    lm_tokenizer=lm_tokenizer,
                    clip_preprocess=clip_preprocess,
                    clip_model=clip_model,
                    model=model)

    return text


if __name__ == "__main__":
    img_temp = Image.open(sys.argv[1])
    text = clipcap_main(img_temp)
    with open(sys.argv[2], "w") as f:
        f.write(text)
    print(text)