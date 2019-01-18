#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from PIL import Image
from io import BytesIO
import json,os
from urllib import request,parse
from http import cookiejar
from Userinformation import Uesrinfo


class Userlogin():

    def __init__(self):


        self.cookiefile = "c:/test/cookie.txt"                  #注意这个文件位置
        
        self.allheaders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Connection': 'keep-alive',
            'Host': 'kyfw.12306.cn',
        }

    def ccookies(self,url):
        #cookiefile = "c:/test/cookie.txt"
        if os.path.isfile(self.cookiefile):
            cookie = cookiejar.MozillaCookieJar(self.cookiefile)
            cookie.load(self.cookiefile,ignore_discard=True,ignore_expires=True)
            handler = request.HTTPCookieProcessor(cookie)       # 通过CookieHandler创建opener
            opener = request.build_opener(handler)              # 此处的open方法打开网页
            response = opener.open(url)
            #if self.mimi == True:
            cookie.save(self.cookiefile, ignore_expires=True, ignore_discard=True)
            return response
        else:
            cookie = cookiejar.MozillaCookieJar(self.cookiefile)     # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
            handler = request.HTTPCookieProcessor(cookie)       # 通过CookieHandler创建opener
            opener = request.build_opener(handler)              # 此处的open方法打开网页
            response = opener.open(url)
            cookie.save(self.cookiefile,ignore_expires=True,ignore_discard=True)

            return response

    def requestyzm(self):
        captchaurl = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&666'
        capresponse= request.Request(captchaurl)
        capresult = self.ccookies(capresponse)
        fn = Image.open(BytesIO(capresult.read()))
        fn.save('c:/test/code.jpg')
        code = {
            '1': '40,40',
            '2': '110,40',
            '3': '180,40',
            '4': '260,40',
            '5': '40,120',
            '6': '110,120',
            '7': '180,120',
            '8': '260,120'
            }
        captchacode = input('请输入验证码序号：')                  # 用户手动输入验证码序号
        temp = captchacode.split(',')                               # 将输入的序号以','号分隔，组成一个输入的数字的列表
        tempcode = ''                                               # 构建一个空字符串
        for i in temp:                                              # 对验证码序号列表进行遍历
            tempcode += code[i] + ','                               # 将每个验证码序号对应的位置信息添加到字符串中，并加上','号
        finalcode = tempcode.rstrip(',')                            # 将最后一个','号去掉，构成一个位置信息的字符串
        captchadata = {
            'answer': finalcode,
            'login_site': 'E',
            'rand': 'sjrand'
        }
        return captchadata

    def login(self):
        captchaurl1 = 'https://kyfw.12306.cn/passport/captcha/captcha-check?'
        userdata= self.requestyzm()
        userdataparse = parse.urlencode(userdata)
        yzmresponse = request.Request(url=captchaurl1,data=userdataparse.encode('utf-8'),headers=self.allheaders)
        yzmrequest = self.ccookies(yzmresponse)

        passmess = json.loads(yzmrequest.read())
        if passmess['result_code'] == '4':
            print(passmess['result_message'])
            loginurl = 'https://kyfw.12306.cn/passport/web/login'
            logindata = {
                'username': 'youraccount',
                'password': 'passwd',
                'appid': 'otn'
            }
            loginparse = parse.urlencode(logindata)
            loginpage = request.Request(loginurl, data=loginparse.encode('utf-8'), headers=self.allheaders)
            loginhttp = self.ccookies(loginpage)
            loginmess = json.loads(loginhttp.read())
            print(loginmess['result_message'])
            loginstat = True
            return loginstat

        elif passmess['result_code'] == '5':
            print('验证失败，请重新输入。',passmess['result_message'],passmess['result_code'])
            os.remove('c:/test/cookie.txt')
        elif passmess['result_code'] == '8':
            print('cookie超时，重新登陆！',passmess['result_message'],passmess['result_code'])
            os.remove('c:/test/cookie.txt')
        else:
            print('未知错误，请联系管理员！',passmess['result_message'],passmess['result_code'])
            os.remove('c:/test/cookie.txt')
if __name__=='__main__':
    begin = Userlogin()
    stat = begin.login()

