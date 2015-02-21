#!/usr/bin/python

import sys;
import MySQLdb;
import pytz
import time
import calendar
from datetime import datetime;
from datetime import date;
from pytz import timezone;

import urlparse;

class weathermaps() :
	def __init__(self):
		self.link='gfs_namer_075_10m_wnd_precip_l.gif'; # 10m wind/precip
		self.link='http://mag.ncep.noaa.gov/data/gfs/12/gfs_namer_072_1000_850_thick_l.gif'; # precip and thickness.
	
	def application(self,environ, start_response):

		if(environ['PATH_INFO'] == '/weathermaps'):
			self.image_link = 'http://mag.ncep.noaa.gov/data/gfs/12/gfs_namer_{0}_850_vort_ht_l.gif';
		elif(environ['PATH_INFO'] == '/weathermaps/vort'):
			self.image_link = 'http://mag.ncep.noaa.gov/data/gfs/12/gfs_namer_{0}_850_vort_ht_l.gif';
		elif(environ['PATH_INFO'] == '/weathermaps/precip'):
			self.image_link = 'http://mag.ncep.noaa.gov/data/gfs/12/gfs_namer_{0}_10m_wnd_precip_l.gif';
		elif(environ['PATH_INFO'] == '/weathermaps/jet'):
			self.image_link = 'http://mag.ncep.noaa.gov/data/gfs/12/gfs_namer_{0}_250_wnd_ht_l.gif';
		if(environ['REQUEST_METHOD'] == 'GET'):
			return self.get(environ,start_response);
		elif(environ['REQUEST_METHOD'] == 'PUT'):
			return self.put(environ,start_response);

	def output_buttons(self,range,utc):
		output=''
		for x in range:
			padded=str(x).zfill(3);
			link = self.image_link.format(padded);
			time = utc+60*60*x;
			day = x//24
			color = 'FFFF00' if day%2==0 else 'FFFFFF';
			button_style = 'style="background-color:#{0}"'.format(color);
			output += '<button {3} onclick=\"newImage(\'{0}\',{2})\"> {1} </button>\n'.format(link,x,time,button_style);
		return output

	def get(self,environ,start_response):
    		output = ''
		today = date.today();
		base_time = datetime(today.year,today.month,today.day,12); #// i.e 12utc today
		utc = int(base_time.strftime("%s"))

		output+=self.output_buttons(xrange(0,192,3),utc)
		output+=self.output_buttons(xrange(192,384+12,12),utc)

		output += '<br/><p id="timestamp">ymd</p>';
		first_image = self.image_link.format('000');
		output += '<br/><img id="image" src="{0}"></img>'.format(first_image);

		output += ('<script> function newImage(link,utc){ '
			 'document.getElementById("image").src=link;'
			 'var date=new Date(utc*1000);'
			 'document.getElementById("timestamp").innerHTML=date;'
			'}'
			'newImage("'+first_image+'",'+str(utc)+');'
			'</script>');

        	response_headers = [('Content-type', 'text/html'),('Content-Length', str(len(output)))]
		status = '200 OK';
        	start_response(status, response_headers)

		return [output]	
	def put(self,environ,start_response):
		output = ''
		status = '404 not found';

        	response_headers = [('Content-type', 'text/html'),('Content-Length', str(len(output)))]
        	start_response(status, response_headers)

		return [output];

def test_response(a,b):
	print 'test_response';

if(__name__ == "__main__"):
	environ = {'REQUEST_METHOD': 'GET','PATH_INFO':'/weathermaps/precip', 'QUERY_STRING': ''};
	test=weathermaps();
	print(test.application(environ,test_response));

