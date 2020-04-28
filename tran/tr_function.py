import sys
import hmac
from base64 import b64encode
from time import time
import requests
from random import randint

SecretId = '？？？？？'
SecretKey = '？？？？？'
encoding = 'utf-8'
meth = 'GET'
alg = 'sha1'


"""
    本py文件是英文->中文的翻译，调用的是腾讯云的接口，比腾讯AI平台的接口更方便简单，两个平台调用方式不同
"""


def timestamp():
    # 获取时间戳
    return int(time())


def signature(key, text):
    # 对访问请求签名
    # 腾讯云支持 sha1 和 sha256
    s = hmac.new(key.encode(encoding), text.encode(encoding), alg)
    return b64encode(s.digest()).decode('utf-8')


def sort_join(params):
    # 拼接请求参数 param1=value1&param2=value2
    _params = sorted(params.items())
    return '&'.join(['='.join([i[0], str(i[1])]) for i in _params])


params = {
    'Action': 'TextTranslate',
    'ProjectId': 0,
    'Source': 'en',
    'SourceText': None,
    'Target': 'zh',
    'Region': 'ap-guangzhou',
    'Timestamp': None,
    'Nonce': None,
    'SecretId': SecretId,
    # 'SignatureMethod': 'HmacSHA1',
    'Version': '2018-03-21'
}


def get_tran(text):
    """
    调用接口，获取英文->中文的翻译
    :param text:
    :return:
    """
    params.update({
        'SourceText': text,
        'Timestamp': timestamp(),
        'Nonce': randint(1, sys.maxsize),  # Nonce: 1 ~ sys.maxsize 的随机数
    })
    _params = sort_join(params)
    sig = signature(SecretKey, meth + 'tmt.tencentcloudapi.com/?' + _params)
    req = requests.get('https://tmt.tencentcloudapi.com/', params={'Signature': sig, **params})
    resp = req.json()['Response']
    if resp.get('TargetText', None):
        return resp['TargetText']

