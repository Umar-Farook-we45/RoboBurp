# RoboBurp

Robot Framework Library for BurpSuite to perform authenticated scan on an application.

### Description
The Robot Framework contacts the BurpSuite extender written in Jython to perfom functionalities such as Initiating a scan, getting the scan status and fetching the XML report. 


### Requirements:
* Jython
 * Installation:
 	
 	####
 		wget http://search.maven.org/remotecontent?filepath=org/python/jython-installer/2.7.0/jython-installer-2.7.0.jar && sudo java -jar jython-installer-2.7.0.jar -s -t standard -d /usr/local/jython-2.7.0 && sudo ln -s /usr/local/jython-2.7.0/jython /usr/local/bin/
* Install RoboBurpp libraries into the virtualenv with `python setup.py install`

### Important
    Please use absolute paths in the Robot Script. 
    BurpSuite Pro is required to use RoboBurp.

## Keywords Implemented

start burp gui
--------------
Arguments:  [BurpSuite path, extender path, jython path, proxy port]

Start BurpSuite GUI

Examples:

`| start burp gui  | BurpSuite path | extender path | jython path | proxy port |`

start burp
----------
Arguments:  [BurpSuite path, extender path, jython path, proxy port]

Start BurpSuite in headless mode

Examples:

`| start burp | BurpSuite path | extender path | jython path | proxy port |`


initiate burp scan
------------------
Arguments:  [proxy port]

Start BurpSuite GUI

Examples:

`| initiate burp scan  | proxy port |`


get burp status
---------------
Arguments:  [proxy port]

Get BurpSuite Scan status

Examples:

`| get burp status  | proxy port |`


get burp results
----------------
Arguments:  [BurpSuite path, proxy port, XML report path, report name, Burp DB path]

Generates an XML report

Examples:

`| get burp results  | BurpSuite path | proxy port | xml path | report name | burp db path |`


kill burp
---------
Arguments:  [proxy port]

Shutdown process for BurpSuite.

Examples:

`| kill burp | proxy port |`

