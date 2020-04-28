# Django+FrozenUI移动端拍照翻译系统

 首先注意修改的地方：
 
 - `tran`文件夹下`ocr_function.py`中的 __app_id__ 和 __app_key__ ，使用腾讯AI开发平台文字识别的token
 
 - `tran`文件夹下`tr_function.py`中的 __secretid__ 和 __secredkey__ ，使用腾讯云机器翻译的token
 
 - `innovation_test`文件夹下的`settings.py`中的 __SECRET_KEY__ ,改为自己Django项目的secretkey
 
 - 本项目没上线，所有测试都在本地端进行。可以将手机与PC连至同一个WLAN下，并添加PC IP地址至`innovation_test`文件夹下的`settings.py`中的`ALLOWED_HOST`白名单中
 
### 使用工具

- 腾讯AI开放平台 
- 腾讯云平台的TMT接口
- Django
- 腾讯FrozenUI
- 各种module

###  使用流程

配置好修改的参数后，启动Django `python manage.py runserver 0:8000`
手机浏览器输入PC端IP地址即可进入

效果如下：



1、进入
![7D29F1C4FA45DFA5B5530CA98B1D5D02.JPG](https://i.loli.net/2020/04/28/sFcvyM2A7w4nkbO.png)


2、拍照
![B5BAACFF5D82128DEB63F60EA9D63ED4.JPG](https://i.loli.net/2020/04/28/YNy4mogq85D9bch.png)

3、上传得到翻译结果
![9B6D47BA9E9334A38568332CB643EBE7.JPG](https://i.loli.net/2020/04/28/Lir3OTEc9mKfwUA.png)

4、选择文字进行翻译
![AA510D4BF3292B748E2E3148C1ADD397.JPG](https://i.loli.net/2020/04/28/duypwtHQrqRn1X3.png)

5、同上
![A609EECC5283B610E4F17295EE34D4B5.JPG](https://i.loli.net/2020/04/28/iHYdv4LUJkWgqGA.png)
