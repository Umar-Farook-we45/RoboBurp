from burp import IBurpExtender
from burp import IBurpExtenderCallbacks
from burp import IHttpRequestResponse
from burp import IHttpService
from burp import IProxyListener
from burp import IScannerListener
from burp import IHttpListener
from burp import IScanQueueItem
from burp import IInterceptedProxyMessage
from java.io import PrintWriter
import json
import re
import copy
import os
import requests
from datetime import datetime
import time
from java.net import URL
from java.io import File
import sys


class BurpExtender(IBurpExtender, IScannerListener, IProxyListener, IHttpListener):
	def registerExtenderCallbacks(self, callbacks):
		try:
			self._callbacks = callbacks
			self._scanlist = []
			self._scantarget = []
			self.all_requests = []
			self.helpers = callbacks.getHelpers()
			callbacks.setExtensionName("RoboBurp")
			self._stdout = PrintWriter(callbacks.getStdout(), True)
			self._stderr = PrintWriter(callbacks.getStderr(), True)
			callbacks.registerScannerListener(self)
			callbacks.registerProxyListener(self)
			self._stdout.println(json.dumps({"running": 1}))
			self._stdout.flush()
			self.scan_status_url = 'http://localhost:1111'
			self.proxyDict = {"http": 'http://localhost:{0}'.format(os.environ.get('port', 8080))}
			return
		except BaseException as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			status = 'Failed - {0} {1}'.format(e, exc_traceback.tb_lineno)
			self._stdout.println(status)

	def processProxyMessage(self, messageIsRequest, message):
		try:
			callbacks = self._callbacks
			message.setInterceptAction(
				IInterceptedProxyMessage.ACTION_DONT_INTERCEPT)
			if messageIsRequest == 1:
				requestresponse = message.getMessageInfo()
				request = requestresponse.getRequest()
				target = requestresponse.getHttpService()
				host = target.getHost()
				port = target.getPort()
				protocol = target.getProtocol()

				if port == 1110:  # Initiate Scan
					if self.all_requests:
						for req in self.all_requests:
							scaninstance = callbacks.doActiveScan(req.get('host'), req.get('port'), req.get('https'), req.get('request'))
							self._scanlist.append(scaninstance)

				elif port == 1111:  # Gets Status
					message.setInterceptAction(
						IInterceptedProxyMessage.ACTION_DROP)
					statuses = []
					for scaninstance in self._scanlist:
						statuses.append(scaninstance.getStatus())
					self._stdout.println(json.dumps(statuses))
					if statuses:
						for index, item in enumerate(statuses):
							if 'abandoned' in item:
								statuses[index] = 'finished'
						if not all(stat == 'finished' for stat in statuses):
							try:
								for index, item in enumerate(statuses):
									if "finished" in item or "aborted" in item or "cancelled" in item:
										statuses[index] = 100
									elif "complete" in item:
										statuses[index] = int(item.split('%')[0])
									else:
										statuses[index] = 0
								percentage = (sum(statuses)/len(statuses))
								with open('.status', 'w') as f:
									f.write(str(percentage))
								status = {'status': 'Running', 'progress': '{0}'.format(percentage), 'scanner': 'Burp'}
								self._stdout.println(json.dumps(status))
							except BaseException as e:
								exc_type, exc_value, exc_traceback = sys.exc_info()
								status = 'Failed - {0} {1}'.format(e, exc_traceback.tb_lineno)
								self._stdout.println(status)
						if all(stat == 'finished' for stat in statuses):
							percentage = 100
							with open('.status', 'w') as f:
								f.write(str(percentage))
							self.get_issues()
					else:
						status = 'Failed - No scan status.'
						self._stdout.println(status)
					self._stdout.flush()
					return

				elif port == 1112:  # Get XML Report
					self.get_issues()
				urlpath = re.search('^\w+ (.+) HTTP', request.tostring())
				if urlpath is not None:
					url = protocol + "://" + host + urlpath.group(1)
					if self._scantarget.count(url) == 0:
						self._scantarget.append(url)
						https = 0
						if protocol == "https":
							https = 1
						self.all_requests.append({'host': host, 'port': port, 'https': https, 'request': request})
						# scaninstance = callbacks.doActiveScan(host, port, https, request)
						# self._scanlist.append(scaninstance)
			return
		except BaseException as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			status = 'Failed - {0} {1}'.format(e, exc_traceback.tb_lineno)
			self._stdout.println(status)


	def get_issues(self):
		file_name = 'BurpResults.xml'
		all_issues = []
		try:
			for scaninstance in self._scanlist:
				for scanissue in scaninstance.getIssues():
					all_issues.append(scanissue)
			self._callbacks.generateScanReport('XML', all_issues, File(file_name))
		except BaseException as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			status = 'Failed - {0} {1}'.format(e, exc_traceback.tb_lineno)
			self._stdout.println(status)
