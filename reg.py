import requests
import re
from selenium import webdriver
import time

TURN_ON_REAL_REGISTRATION = True

#set the module as the planner
module = 'reg/plan/add_planner.pl'
is_planner = 'Y'

if TURN_ON_REAL_REGISTRATION:
    #set the module for real class registration
    module = 'reg/add/confirm_classes.pl'
    is_planner = ''
    
    
'''
Press F12 in chrome, navigate to the Network tab, then go to your planner on student link, 
click on the item with a long number, under request headers find "Cookie: .... " 
Copy the `cookie` header below
'''
cookies = ''


#You might also have to copy the other headers into here
def generate_headers():
    return {'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': cookies,
    'DNT': '1',
    'Host': 'www.bu.edu',
    'Referer': 'https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1524338857/1524338857',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
    }



url = 'https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1524289373'

def generate_params(college, dept, course, section):
    return {
    'College': college,
    'Dept': dept,
    'Course': course,
    'Section': section,
    'ModuleName': 'reg/add/browse_schedule.pl',
    'AddPreregInd': '',
    'AddPlannerInd': '',
    'ViewSem': 'Fall 2018',
    'KeySem': '20193',
    'PreregViewSem':  '',
    'PreregKeySem':  '',
    'SearchOptionCd': 'S',
    'SearchOptionDesc': 'Class Number',
    'MainCampusInd': '',
    'BrowseContinueInd': '', 
    'ShoppingCartInd': '' ,
    'ShoppingCartList': '' }

def generate_reg_params(college, dept, course, section, ssid):
    return {'SelectIt': ssid, 
    'College':college.upper(),
    'Dept':dept.upper(),
    'Course':course, 
    'Section':section.upper(),
    'ModuleName': module,
    'AddPreregInd': '',
    'AddPlannerInd': is_planner,
    'ViewSem':'Fall 2018',
    'KeySem':'20193',
    'PreregViewSem':'',
    'PreregKeySem':'',
    'SearchOptionCd':'S',
    'SearchOptionDesc':'Class Number',
    'MainCampusInd':'',
    'BrowseContinueInd':'',
    'ShoppingCartInd':'',
    'ShoppingCartList':''}
    
# Replace with your own BU login and password.
# Your credentials are only stored in this file, and I am not liable if you expose this file to anyone else.
def credentials():
    return ('BU_username', 'BU_password')

def login():
    print('logging in...')
    driver = webdriver.Chrome()

    driver.get("https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1524541319?ModuleName=regsched.pl")
    username, password = credentials()
    driver.find_element_by_id('j_username').send_keys(username)
    driver.find_element_by_id('j_password').send_keys(password)
    driver.find_element_by_class_name('input-submit').click()
    while 'studentlink' not in driver.current_url:
        time.sleep(3)
        
    cookies_list = driver.get_cookies()
    global cookies
    cookies = ''
    for cookie in cookies_list:
        cookies = cookies + cookie['name'] + '=' + cookie['value'] + '; '
    print('Retrieving cookies: ' + cookies)
    driver.close()

'''
Finds course listing and tries to register for the class.

Sometimes course names are wrong, use at your own discretion. 
'''
def find_course(college, dept, course, section):
    name =  dept.upper() + course + ' ' + section.upper()
    print('searching for ' + name)
    params_browse = generate_params(college, dept, course, section)
    headers = generate_headers()
    ####
    for retry in range(1, 5):
        #logging.warning('[fetch] try=%d, url=%s' % (retry, url))
        retry_because_of_timeout = False
        try:
            r = requests.get(url, headers=headers,params=params_browse, timeout = 3)
            text = r.text
        except Exception as e:
            retry_because_of_timeout=True
            pass
    
        if retry_because_of_timeout:
            time.sleep(retry * 2 + 1)
        else:
            break
    ####
    #print(r.text)
    #(?<=abc)
    p = re.compile('<tr ALIGN=center Valign= top>.+?</td></tr>', re.DOTALL)
    m = p.findall(text)
    if len(m) == 0:
        print('Something went wrong with the request for ' + dept + course)
        login()
        find_course(college, dept, course, section)
        return
    s = college.upper() + dept.upper() + course + '%20' + section.upper()

    found = False
    for item in m:
        if re.search(s, item):
            found = True
            n = re.search('value="(\d{10})"', item)
            if n:
                params_reg = generate_reg_params(college, dept, course, section, n.group(1))
                reg = requests.get(url, headers=headers,params=params_reg)
                o = re.search('<title>Error</title>', reg.text)
                if o:
                    print('Can not register yet :/')
                else:
                    print('Registered successfully!')
            else:
                print('Class is full :(')
            break
    if not found:
        print('could not find course')

# Replace with your own course.
# Ex. ('cas','wr','100','a1')
my_courses = [('college', 'dept', 'course', 'section')]

beginning = time.time()
cycles = 0
login()
while True:
    for i in my_courses:
        print('\n['+str(time.asctime())+']')
        start = time.time()
        find_course(*i)
        duration = (time.time() - start)
        print('Took ' + str(round(duration, 1)) + ' seconds')
        cycles+=1
        print('Average time: ' + str(round((time.time() - beginning)/cycles,1)))


    
