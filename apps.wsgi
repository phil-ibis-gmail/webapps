#!/usr/bin/python

# this block allows importing from the local directory, so we can eg import rubik below.
import sys
import os

sys.path.append(os.path.dirname(__file__))
 
import rubik
import weatherlog
import weathermaps
import expenses

def application(environ, start_response):

	output = '';
	
	path = environ['PATH_INFO'];
	if(path == '/rubik'):
		rubika=rubik.rubik()
		return rubika.application(environ,start_response)
	elif(path == '/weather'):
		w=weatherlog.weatherlog()
		ret= w.run_application(environ,start_response)
		output += '{0}'.format(ret)
		return ret;
	elif(path.startswith('/weathermaps')):
		w=weathermaps.weathermaps()
		return w.application(environ,start_response)
	elif(path.startswith('/expenses')):
		e=expenses.expenses();
		return e.application(environ,start_response)

	output += 'not found: {0}'.format(path)
	
	status = '404 not found'
	response_headers = [('Content-type', 'text/html'),('Content-Length', str(len(output)))]
	start_response(status, response_headers)
	return [output];


def bla(a,b):
	print 'bla'

if(__name__ == "__main__"):
	#environ = {'PATH_INFO': '/rubik', 'REQUEST_METHOD': 'PUT','QUERY_STRING': 'seconds=100&tag=debug&moves=100&solved=not_solved&method=none'};
	#environ = {'PATH_INFO': '/weather', 'REQUEST_METHOD': 'PUT','QUERY_STRING': 'temperature=10&pressure=10'};
	#environ = {'PATH_INFO': '/weathermaps', 'REQUEST_METHOD': 'GET','QUERY_STRING': ''};
	environ = {'PATH_INFO': '/expenses', 'REQUEST_METHOD': 'GET','QUERY_STRING': ''};

	application(environ,bla);

