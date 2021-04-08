from django.shortcuts import render
from django.http import HttpResponse
import logging
import json
import base64
import time

# Create your views here.

logger = logging.getLogger(__name__)


# 文件上传：form-data/Multipart方式
def index(request):
    sendfile = request.FILES.items()
    haveFiles = False
    for key,value in sendfile:
        fileData = request.FILES.getlist(key)
        if len(fileData):
            haveFiles = True
            for fl in fileData:
                name = fl.name
                with open('/home/hych007/project/serverproject/'+name, 'wb') as fp:
                    fp.write(bytes(fl.read()))

    if not haveFiles:
        result = {"errcode": 511, "errmsg": "form-data中未读取到图片信息"}
        return HttpResponse(json.dumps(result), content_type="application/json")

    cameraCode = request.POST.get("cameraCode", "")
    if not cameraCode:
        result = {"errcode": 501, "errmsg": "cameraCode摄像头编号不能为空"}
        return HttpResponse(json.dumps(result), content_type="application/json")

    doorCode = request.POST.get("i3310A", "")
    if not doorCode:
        result = {"errcode": 505, "errmsg": "i3310A门禁编码不能为空"}
        return HttpResponse(json.dumps(result), content_type="application/json")

    userCode = request.POST.get("i3310D", "")
    if not userCode:
        result = {"errcode": 507, "errmsg": "i3310D用户唯一标识码不能为空"}
        return HttpResponse(json.dumps(result), content_type="application/json")

    photoCodes = request.POST.get("photoCodes", "")
    if not len(photoCodes):
        result = {"errcode": 502, "errmsg": "photoCode照片编号不能为空"}
        return HttpResponse(json.dumps(result), content_type="application/json")

    dataTimes = request.POST.get("dataTimes", "")
    if not len(dataTimes):
        result = {"errcode": 503, "errmsg": "dataTime拍照时间不能为空"}
        return HttpResponse(json.dumps(result), content_type="application/json")

    result = {"errcode": 200, "errmsg": "上传成功"}
    return HttpResponse(json.dumps(result), content_type="application/json")

# 文件上传：Body中传Json方式
def body(request):
    try:
        jsData = json.loads(str(request.body, encoding='utf-8'))
    except Exception as e:
        result = {"errcode": -1, "errmsg": "数据不能为空"}
        return HttpResponse(json.dumps(result), content_type="application/json")

    if not isinstance(jsData, list):
        result = {"errcode": 500, "errmsg": "上传的json数据错误"}
        return HttpResponse(json.dumps(result), content_type="application/json")

    for data in jsData:
        imgData = data.get("base64String", "")
        if len(imgData) <= 23:
            result = {"errcode": 509, "errmsg": "照片转Base64String 编码后的字符串不能为空"}
            return HttpResponse(json.dumps(result), content_type="application/json")

        imgData = imgData[23:]
        temp = base64.b64decode(imgData)
        picName = time.strftime("%Y%m%d%H%M%S", time.localtime())
        #图片文件的读写要用二进制模式
        with open("/home/hych007/project/serverproject/"+picName+".jpeg", 'wb') as f:
            f.write(temp)

        cameraCode = data.get("cameraCode", "")
        if not cameraCode:
            result = {"errcode": 501, "errmsg": "cameraCode摄像头编号不能为空"}
            return HttpResponse(json.dumps(result), content_type="application/json")

        doorCode = data.get("i3310A", "")
        if not doorCode:
            result = {"errcode": 505, "errmsg": "i3310A门禁编码不能为空"}
            return HttpResponse(json.dumps(result), content_type="application/json")

        userCode = data.get("i3310D", "")
        if not userCode:
            result = {"errcode": 507, "errmsg": "i3310D用户唯一标识码不能为空"}
            return HttpResponse(json.dumps(result), content_type="application/json")

        photoCode = data.get("photoCode", "")
        if not photoCode:
            result = {"errcode": 502, "errmsg": "photoCode照片编号不能为空"}
            return HttpResponse(json.dumps(result), content_type="application/json")

        dataTime = data.get("dataTime", "")
        if not dataTime:
            result = {"errcode": 503, "errmsg": "dataTime拍照时间不能为空"}
            return HttpResponse(json.dumps(result), content_type="application/json")

    result = {"errcode": 200, "errmsg": "上传成功"}
    return HttpResponse(json.dumps(result), content_type="application/json")

# 提供图片下载功能
def picture(request):
    file = open("/home/hych007/project/testface.jpg", "rb")
    response = HttpResponse(content=file.read(), content_type="image/jpg")
    return response