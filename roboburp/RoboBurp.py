import lxml.etree as xml
from robot.api import logger
from datetime import datetime
import requests
import importlib
import json
from base64 import b64encode
import os
import re
import os.path
import sys
reload(sys)
sys.setdefaultencoding('UTF8')
import time
import subprocess


class RoboBurp(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self.results = None

    def user_config(self, extender_file_path, jython_jar_path,user_config_path):
        try:
            user_conf = json.load(open(user_config_path,'r'))
            user_conf['user_options']['extender']['extensions'][0]['extension_file'] = str(extender_file_path)
            user_conf['user_options']['extender']['python']['location_of_jython_standalone_jar_file'] = str(jython_jar_path)
            with open('user.json', 'w') as f:
                json.dump(user_conf, f)
            return '{0}/user.json'.format(os.getcwd())
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))

    def config_file(self, proxy_port, project_config_path):
        try:
            project_conf = json.load(open(project_config_path, 'r'))
            project_conf['proxy']['request_listeners'][0]['listener_port'] = int(proxy_port)
            with open('project.json', 'w') as f:
                json.dump(project_conf, f)
            return '{0}/project.json'.format(os.getcwd())
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))

    def start_burp(self, burp_jar_path, extender_file_path='{0}/roboextender.py'.format(os.getcwd()), jython_jar_path='/usr/local/jython-2.7.0/jython.jar', proxy_port=8080, user_config_path='{0}/default_userconf.json'.format(os.getcwd()), project_config_path='{0}/default_projectconf.json'.format(os.getcwd())):
        try:
            user_config = self.user_config(extender_file_path, jython_jar_path, user_config_path)
            project_config = self.config_file(proxy_port, project_config_path)
            cmd = 'java -jar -Djava.awt.headless=true {0} --user-config-file={1} --config-file={2}'.format(burp_jar_path, user_config, project_config)
            logger.info('{0}'.format(cmd))
            subprocess.Popen(cmd.split(),stdout=open(os.devnull, 'w'),stderr=subprocess.STDOUT)
            time.sleep(30)
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))

    def start_burp_gui(self, burp_jar_path, extender_file_path='{0}/roboextender.py'.format(os.getcwd()), jython_jar_path='/usr/local/jython-2.7.0/jython.jar', proxy_port=8080, user_config_path='{0}/default_userconf.json'.format(os.getcwd()), project_config_path='{0}/default_projectconf.json'.format(os.getcwd())):
        try:
            user_config = self.user_config(extender_file_path, jython_jar_path, user_config_path)
            project_config = self.config_file(proxy_port, project_config_path)
            cmd = 'java -jar {0} --user-config-file={1} --config-file={2}'.format(burp_jar_path, user_config, project_config)
            logger.info('{0}'.format(cmd))
            subprocess.Popen(cmd.split(),stdout=open(os.devnull, 'w'),stderr=subprocess.STDOUT)
            time.sleep(30)
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))



    def initiate_burp_scan(self, proxy_port=8080):
        try:
            initiate_scan_url = 'http://localhost:1110'
            proxyDict = {"http": 'http://localhost:{0}'.format(proxy_port)}
            requests.get(url=initiate_scan_url, proxies=proxyDict)
            with open('.status', 'w') as f:
                f.write('0')
            time.sleep(20)
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))

    def get_burp_status(self, proxy_port=8080):
        try:
            status = True
            scan_status_url = 'http://localhost:1111'
            proxyDict = {"http": 'http://localhost:{0}'.format(proxy_port)}
            while status:
                requests.get(url=scan_status_url, proxies=proxyDict)
                time.sleep(5)
                with open('.status', 'r') as f:
                    status = f.read()
                logger.info('Scan running at {0}%'.format(int(status)))
                if int(status) == 100:
                    status = False
                else:
                    time.sleep(10)
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))

    def kill_burp(self, proxy_port=8080):
        try:
            kill_burp_url = 'http://localhost:1113'
            proxyDict = {"http": 'http://localhost:{0}'.format(proxy_port)}
            requests.get(url=kill_burp_url, proxies=proxyDict)
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))



    def get_burp_results(self, burp_jar_path, proxy_port=8080, xml_path='{0}'.format(os.getcwd()), xml_name='BurpResults.xml', burp_db_path='{0}/burp_db.json'.format(os.getcwd())):
        try:
            generate_report_url = 'http://localhost:1112'
            burp_path = '/'.join(burp_jar_path.split('/')[0:-1])
            proxyDict = {"http": 'http://localhost:{0}'.format(proxy_port)}
            requests.get(url=generate_report_url, proxies=proxyDict)
            time.sleep(30)
            logger.info('XML PATH: {0}/{1}'.format(xml_path, xml_name))
            self.parse_result('BurpResults.xml', burp_db_path)
            os.rename('BurpResults.xml', '{0}/{1}'.format(xml_path, xml_name))
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))


    def cwe_dict(self, burp_db_path):
        try:
            cwe_dict = json.load(open(burp_db_path, 'r'))
            return cwe_dict
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))

    def parse_result(self, xml_file, burp_db_path):
        try:
            nreport = xml.parse(xml_file)
            root_elem = nreport.getroot()
            reg_path = r'issue/name'
            uniq_objs = root_elem.xpath(reg_path)
            vuls = set([i.text for i in uniq_objs])
            p = '{0}[text() = $name]'.format(reg_path)
            severity_dict = {
                'Information': 0,
                'Low': 1,
                'Medium': 2,
                'High': 3
            }
            burp_confidence_dict = {
                "Certain": 3,
                "Firm": 2,
                "Tentative": 1,
            }
            for v in vuls:
                obj = root_elem.xpath(p, name=v)
                url_param_list = []
                for u in obj:
                    parent_obj = u.getparent()
                    req = parent_obj.find('requestresponse/request')
                    res = parent_obj.find('requestresponse/response')
                    request = response = b64encode('')
                    if req is not None:
                        is_base64_encoded = True if req.get('base64') == 'true' else False
                        if is_base64_encoded:
                            request = req.text
                        else:
                            request = b64encode(req.text)
                    if res is not None:
                        is_base64_encoded = True if res.get('base64') == 'true' else False
                        if is_base64_encoded:
                            response = res.text
                        else:
                            response = b64encode(res.text)
                    url = 'http:/{0}'.format(parent_obj.findtext('path', default=''))
                    url_param_list.append({
                        'url': parent_obj.findtext('location', default=''),
                        'attack': parent_obj.findtext('issueDetailItems/issueDetailItem', default=None),
                        'name': parent_obj.findtext('issueDetailItems/issueDetailItem', default=''),
                        'request': request,
                        'response': response,
                    })
                vul_name = parent_obj.findtext('name', default='')
                severity = parent_obj.findtext('severity', '')
                issue_type = parent_obj.findtext('type', '8389632')
                if severity:
                    severity = severity_dict.get(severity)
                cwe_present = self.cwe_dict(burp_db_path).get(issue_type, [])
                cwe = 0
                if cwe_present:
                    cwe = cwe_present[0]
                desc = parent_obj.findtext('issueBackground', default='')
                solution = parent_obj.findtext('remediationBackground', default='')
                observation = parent_obj.find('issueDetail')
                confidence = parent_obj.findtext('confidence', default='')

                if confidence:
                    confidence = burp_confidence_dict.get(confidence)
                if observation is not None:
                    s = '''You should manually examine the application behavior and attempt to identify any unusual input validation or other obstacles that may be in place.'''
                    obs = observation.text.replace(s, '')
                else:
                    obs = ''
                vul_dict = {}
                vul_dict['vulnerability'] = {
                    'tool': 'Burp',
                    'name': vul_name,
                    'created_on': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'description': desc,
                    'remediation': solution,
                    'severity': severity,
                    'confidence': confidence,
                    'observations': obs,
                }
                vul_dict['vulnerability']['evidences'] = url_param_list
                vul_dict['vulnerability']['cwe'] = {
                    'cwe_id': cwe
                }
                logger.info(vul_dict)
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))
