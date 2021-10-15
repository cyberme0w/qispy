from requests import Session, get, post
import time




############
# Settings #
############
verbose = True
username = "YourUsernameHere"
password = "YourPasswordHere"

# 0. Helper functions
def print_verbose(string):
    if(verbose):
        print(string)


# 1. Create a session and get qis/compass's html
s = Session()
print_verbose("[INFO] Requesting website...")
r = s.get('https://compass.hs-rm.de/qisserver/pages/cs/sys/portal/hisinoneStartPage.faces?chco=y')

if(r.status_code != 200):
    print("[ERROR] Request returned code {}. Aborting now...".format(r.status_code))
    exit(-1)

print_verbose("[INFO] Request returned code 200. Grabbing cookies...")


# 2. Grab cookies and tokens
if(verbose):
    print("[INFO] Cookies")
    for cookie in s.cookies:
        print("       {}: {}".format(cookie.name, cookie.value))

content = str(r.content)
substring = 'authenticity_token'
auth_token_start = content.find(substring) + 27
auth_token_end = auth_token_start + 44
auth_token = content[auth_token_start:auth_token_end]
print_verbose("       authenticity_token: {}".format(auth_token))


# 3. Grab the AJAX CSRF token 
substring = 'name="ajaxToken"'
ajax_token_start = content.find(substring) - 38
ajax_token_end = ajax_token_start + 36
ajax_token = content[ajax_token_start:ajax_token_end]
print_verbose("       ajaxToken: {}".format(ajax_token))


# 4. Prepare Login POST Form
print_verbose("[INFO] Preparing for login POST")

post_url = "https://compass.hs-rm.de:443/qisserver/rds?state=user&amp;type=1&amp;category=auth.login"
post_data = {'userInfo': '', 'ajax-token': ajax_token, 'asdf': username, 'fdsa': password, 'submit': ''}

if(verbose):
    for d in post_data:
        print("       {}: {}".format(d, post_data.get(d)))


#r = s.post(post_url, data=post_data)

#print(r.headers)
#print("\n")
#print(r.content)