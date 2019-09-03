# coding=utf-8
from getpass import getpass
import urllib.request, urllib.error, urllib.parse
import http.cookiejar
import re
from urllib.parse import urlencode
import json
import sys
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup


class Renren(object):
    RENREN_HEADER = "http://www.renren.com/"
    SHELL_HEADER = "http://shell.renren.com/"
    SIG = ""
    TOK_PAT = re.compile(b">XN = {get_check:'([^']+)',get_check_x:'([^']+)'")

    def __init__(self):
        self.cookie = http.cookiejar.CookieJar()
        cookieProc = urllib.request.HTTPCookieProcessor(self.cookie)
        opener = urllib.request.build_opener(cookieProc)
        urllib.request.install_opener(opener)
        self.username = ""
        self.password = ""
        self.loggedon = False
        self.hostid = None

    def setAccount(self, user, pw):
        self.username = input('Renren Account: ')
        self.password = getpass(prompt='Password: ')

    def login(self):
        post = {
            'email': self.username,
            'password': self.password,
            "autoLogin": "true",
            "origURL": "http://www.renren.com/home",
            "domain": "renren.com",
            "key_id": "1",
            "captcha_type": "web_login"}
        post = urlencode(post)
        post = post.encode('utf-8')
        req = urllib.request.Request(
            url=self.RENREN_HEADER + "PLogin.do",
            data=post)
        resp = urllib.request.urlopen(req)
        html = resp.read()
        out = re.search(self.TOK_PAT, html)
        if out is None:
            return False
        else:
            self.reqToken = out.group(1)
            self._rtk = out.group(2)
            id_cookie = get_cookie_by_name(self.cookie, 'id')
            self.hostid = id_cookie.value
            self.loggedon = True
            return True

    def publishStatus(self, status):
        target = self.SHELL_HEADER + self.hostid + "/status"
        post = urlencode(
            {"content": status + sys.version,
             "hostid": self.hostid,
             "requestToken": self.reqToken,
             "_rtk": self._rtk,
             "channel": "renren"
            }
        )
        req = urllib.request.Request(
            url=target,
            data=post
        )
        resp = urllib.request.urlopen(req)
        return (json.loads(resp.read()))["code"] == 0

    def auto_post(self, post_url, post_data):
        header_info = {'User-Agent': 'IE', }
        req = urllib.request.Request(
            url=post_url,
            headers=header_info,
            data=post_data.encode('utf-8'),
        )
        result = urllib.request.urlopen(req)

    def post_renren_blog(self, name='None', body='None'):
        post_blog_url = 'http://blog.renren.com/NewEntry.do'
        req = urllib.request.urlopen(post_blog_url).read()
        soup = BeautifulSoup(req)
        post_id = soup.find(id='postFormId').get('value')
        post_data = urllib.parse.urlencode(
            {'title': name, 'body': body, 'categoryId': '0', 'blogControl': '99', 'postFormId': post_id,
             'relative_optype': 'saveDraft', "hostid": self.hostid, "requestToken": self.reqToken, "_rtk": self._rtk})
        self.auto_post(post_blog_url, post_data)


def get_cookie_by_name(cookiejar, name):
    return [cookie for cookie in cookiejar if cookie.name == name][0]


