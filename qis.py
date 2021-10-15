from requests import Session, get, post
import time


############
# Settings #
############
verbose = True
username = "yourusername"
password = "yourpassword"


# 1. Create a session and get qis/compass's html
s = Session()
print("[INFO] Requesting website...")
r = s.get('https://compass.hs-rm.de/qisserver/pages/cs/sys/portal/hisinoneStartPage.faces?chco=y')

if(r.status_code != 200):
    print("[ERROR] Request returned code {}".format(r.status_code))
    print("        Aborting now.")
    exit(-1)

elif(verbose):
    print("[INFO] Request returned code 200. Grabbing cookies...")


# 2. Grab cookies and tokens
if(verbose):
    print("[INFO] Cookies:")
    print("       JSESSIONID            = {}".format(s.cookies.get("JSESSIONID")))
    print("       Flash Rendermap Token = {}".format(s.cookies.get("oam.Flash.RENDERMAP.TOKEN")))

content = str(r.content)
substring = 'authenticity_token'
auth_token_start = content.find(substring) + 27
auth_token_end = auth_token_start + 44
auth_token = content[auth_token_start:auth_token_end]

if(verbose):
    print("       Auth Token            = {}".format(auth_token))


# 3. Grab the AJAX CSRF token 
substring = 'name="ajaxToken"'
ajax_token_start = content.find(substring) - 38
ajax_token_end = ajax_token_start + 36
ajax_token = content[ajax_token_start:ajax_token_end]

if(verbose):
    print("       AJAX CSRF Token       = {}".format(ajax_token))


# 4. Send POST with login info, AJAX token and auth token
# URL for Login form (POST)
post_url = "https://compass.hs-rm.de:443/qisserver/rds?state=user&amp;type=1&amp;category=auth.login"
post_data = {'userInfo': '', 'ajax-token': ajax_token, 'asdf': username, 'fdsa': password, 'submit': ''}
r = s.post(post_url, data=post_data)

print(r.content)
