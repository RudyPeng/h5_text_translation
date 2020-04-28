import base64
import hashlib
import time
import random
import string
from urllib.parse import quote
import requests
from PIL import Image

"""
本文件是图片->英文（中文）的翻译函数，调用的是腾讯AI开放平台的接口
"""


def thumbnail(path, savefile='', q=50):
    """
    压缩并保存到文件
    :param path:
    :param savefile:
    :param q:
    :return:
    """
    img = Image.open(path)
    w, h = img.size
    width, height = w * q // 100, h * q // 100
    img.thumbnail((width, height))
    if not savefile:
        savefile = '{}_{}x{}.{}'.format(
            path, width, height, img.format.lower())
    img.save(savefile, img.format)


def curlmd5(src):
    m = hashlib.md5(src.encode('UTF-8'))
    return m.hexdigest().upper()


# 请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效）
def get_params(base64_data):
    t = time.time()
    s_id = str(t)[:8]
    time_stamp = str(int(t))
    # 请求随机字符串，用于保证签名不可预测
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    # 应用标志，这里修改成自己的id和key
    app_id = '？？？'
    app_key = '？？？？？？'
    params = {'app_id': app_id,
              'image': base64_data,
              'time_stamp': time_stamp,
              'nonce_str': nonce_str,
              'scene': 'doc',
              'source': 'en',
              'target': 'zh',
              'session_id': s_id,
              }
    sign_before = ''
    # 要对key排序再拼接
    for key in sorted(params):
        # 键值拼接过程value部分需要URL编码，URL编码算法用大写字母，例如%E8。quote默认大写。
        sign_before += '{}={}&'.format(key, quote(params[key], safe=''))
    # 将应用密钥以app_key为键名，拼接到字符串sign_before末尾
    sign_before += 'app_key={}'.format(app_key)
    # 对字符串sign_before进行MD5运算，得到接口请求签名
    sign = curlmd5(sign_before)
    params['sign'] = sign
    return params


def img_to_text(path):
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_imagetranslate"
    with open(path, 'rb') as fin:
        image_data = fin.read()
    base64_data = base64.b64encode(image_data)
    params = get_params(base64_data)
    r = requests.post(url, data=params)
    if r.status_code == 200:
        data = r.json()['data']['image_records']
        str_en = ""
        str_cn = ""
        for item in data:
            str_en = str_en + item['source_text']
            str_cn = str_cn + item['target_text']
            if item['source_text'][-1] != "-":
                str_en += " "
        return str_en, str_cn
    else:
        return "Error!!!", "出错啦！！！"
