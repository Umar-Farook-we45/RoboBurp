*** Settings ***
Library    RoboBurp.py
Library  Collections
Library  Selenium2Library

*** Variables ***
${BURP_PATH}  /Users/nithinjois/Documents/tools/BurpSuite/burpsuite_pro_v1.7.32.jar
${EXTENDER_PATH}  /Users/nithinjois/Desktop/tests/burp_tests/roboextender.py
${JYTHON_PATH}  /usr/local/jython-2.7.0/jython.jar
${PROXY}  8080
${TARGET}  http://104.236.85.150/
${BASE_URL}  http://104.236.85.150/
${LOGIN_URL}  http://104.236.85.150/login/
${APPNAME}  WeCare


*** Test Cases ***
Initiate BURP
    initiate burp  ${BURP_PATH}  ${EXTENDER_PATH}  ${JYTHON_PATH}  ${PROXY}

Open Healthcare App
    [Tags]  phantomjs
    ${service args}=    Create List    --proxy=127.0.0.1:${PROXY}
    Create WebDriver  PhantomJS  service_args=${service args}
    go to  ${LOGIN_URL}

Login to Healthcare App
    [Tags]  login
    input text  email_id  bruce.banner@we45.com
    input password  password  secdevops
    click button  id=submit
    set browser implicit wait  10
    location should be  ${BASE_URL}dashboard/

Visit Random Pages
    [Tags]  visit
    go to  ${BASE_URL}tests/
    input text  search  something
    click button  name=look
    go to  ${BASE_URL}secure_tests/

Initiate Scan
    initiate_scan  ${PROXY}

Scanning
    get status  ${PROXY}

Get Results
    get results  ${BURP_PATH}  ${PROXY}