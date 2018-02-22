*** Settings ***
Library  RoboBurp.py
Library  Collections
Library  Selenium2Library

*** Variables ***
${PROXY_PORT}  8080
${BURP_PATH}  /Applications/Burp_Suite_Professional.app/Contents/java/app/burpsuite_pro.jar
${EXTENDER_PATH}  /Users/abhaybhargav/Documents/Code/Python/RoboBurp/roboburp/roboextender.py
${JYTHON_PATH}  /usr/local/Cellar/jython/2.7.0/libexec/jython.jar
${PROXY}  8080
${TARGET}  http://﻿104.236.85.150/
${BASE_URL}  http://104.236.85.150/
${LOGIN_URL}  http://104.236.85.150/login/
${APPNAME}  WeCare


*** Test Cases ***
Initiate BURP
    start burp gui  ${BURP_PATH}  ${EXTENDER_PATH}  ${JYTHON_PATH}  ${PROXY_PORT}

Open Healthcare App
    [Tags]  phantomjs
    ${service args}=    Create List    --proxy=127.0.0.1:${PROXY_PORT}
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

Initiate Burp Scan
    initiate burp scan  ${PROXY_PORT}

Scanning
    get burp status  ${PROXY_PORT}

Get Burp Results
    get burp results  ${BURP_PATH}  ${PROXY_PORT}

Kill Burp
    kill burp  ${PROXY_PORT}