#!/usr/bin/python

import sys;
import MySQLdb;
import pytz
import time
import calendar
from datetime import datetime;
from pytz import timezone;
import urlparse;

class rubik() : 
	def application(self,environ, start_response):
		if(environ['REQUEST_METHOD'] == 'GET'):
			return self.get(environ,start_response);
		elif(environ['REQUEST_METHOD'] == 'PUT'):
			return self.put(environ,start_response);

	def get(self,environ,start_response):
    		status = '200 OK'
    		output = ''
	
		db = MySQLdb.connect(host="localhost",user="pibis",passwd="demopassword",db="philtest");
		cur = db.cursor();

		cur.execute("SELECT * From rubix order by when_added desc");

		output += '<table border="1">';

    		for row in cur.fetchall() :
			output += '<tr>';
			timestr = maketime_local(row[4]);
			output += '<td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td><td>{6}</td>'.format(row[0],row[1],row[2],row[3],timestr,row[5],row[6]);
			output += '</tr>\n';
	
    		output += '</table>';

    		response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    		start_response(status, response_headers)

    		return [output]

	def put(self,environ,start_response):
		params_dict = urlparse.parse_qs(environ['QUERY_STRING']);
		output='hella';
		status = '200 OK';

		db = MySQLdb.connect(host="localhost",user="pibis",passwd="demopassword",db="philtest");
		cur = db.cursor();

		seconds = int(params_dict['seconds'][0]);
		tag = params_dict['tag'][0];
		moves = int(params_dict['moves'][0]);
		solved = params_dict['solved'][0];
		method = params_dict['method'][0];

		cur.execute("INSERT INTO philtest.rubix (seconds,tag,moves,when_added,solved_state,method) VALUES(%s,%s,%s,NOW(),%s,%s);",(seconds,tag,moves,solved,method,));
		db.commit();

        	response_headers = [('Content-type', 'text/html'),('Content-Length', str(len(output)))]
        	start_response(status, response_headers)

		return [output];

def maketime_local(time_dt):
	utc = pytz.utc;
	utc_dt = utc.localize(time_dt)
	return utc_dt.astimezone(timezone("US/Pacific")).strftime('%Y-%m-%d %H:%M:%S %Z%z')

def test_response(a,b):
	print 'test_response';

if(__name__ == "__main__"):
	environ = {'REQUEST_METHOD': 'PUT','QUERY_STRING': 'seconds=100&tag=debug&moves=100&solved=not_solved&method=none'};
	test_rubik=rubik();
	test_rubik.application(environ,test_response);

