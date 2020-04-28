import re
import time
import base64
from . import tr_function
from . import ocr_function
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

pattern = re.compile(r',|\.|\?|"|“|”|;|(|)')  # 正常分词
pattern_line = re.compile(r'-')  # 保证某个词换行时添加的-能够被正确去除

globa_en = ""
globa_cn = ""


def clear_text(text):
    text = re.sub(pattern, '', text)
    text = re.sub('\n+', ' ', text)
    text = re.sub(pattern_line, ' ', text)
    return text


def get_img_type(text):
    group = re.split(',', text)
    type_ = re.split('/', group[0])
    main_code = group[1]
    img_type = re.split(';', type_[1])[0]
    return img_type, main_code


def shot(request):
    return render(request, 'shot2.html', locals())


def zip_img(path, r):
    img_type, code = get_img_type(r)
    path = path + '.' + img_type
    imgdata = base64.b64decode(code)
    fh = open(path, "wb")
    fh.write(imgdata)
    fh.close()
    ocr_function.thumbnail(path, path)
    return path


@csrf_exempt
def function_get(request):
    path = str(time.time())
    if request.method == 'POST':
        r = request.POST.get('avatar')
        path = zip_img(path, r)
        text_en, text_cn = ocr_function.img_to_text(path)
        text_en = clear_text(text_en)
        global globa_cn, globa_en
        globa_en = text_en
        globa_cn = text_cn
    return JsonResponse({"msg": "ok!"})


@csrf_exempt
def result(request):
    global globa_en
    data = re.split(' ', globa_en)
    return render(request, 'shot3.html', locals())


@csrf_exempt
def tran_function(request):
    if request.method == 'POST':
        r = request.POST.get('avatar')
        meaning = tr_function.get_tran(r)
    return JsonResponse({"msg": meaning})


def chinese(request):
    global globa_cn
    text = globa_cn
    return render(request, "shot4.html", locals())
