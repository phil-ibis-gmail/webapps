import MySQLdb
import urlparse
import sys
import json
import datetime

class weatherlog : 
	def run_application(self,environ,start_response):

		if(environ['REQUEST_METHOD'] == 'PUT'):
			return self.put(environ,start_response)
		elif(environ['REQUEST_METHOD'] == 'GET'):
			return self.get(environ,start_response)
		
		status = '404 not found';
		output = 'error';
		response_headers = [('Content-type', 'text/html'),('Content-Length', str(len(output)))]
		start_response(status, response_headers)
		return [output]		


	def put(self,environ,start_response) :
		
		params_dict = urlparse.parse_qs(environ['QUERY_STRING']); 
		status = '200 OK';

		db = MySQLdb.connect(host="localhost",user="pibis",passwd="demopassword",db="philtest");
		cur = db.cursor();

		temperature = float(params_dict['temperature'][0]);
		pressure = float(params_dict['pressure'][0]);
		timestamp = datetime.datetime.fromtimestamp(int(params_dict['timestamp'][0]));
		cur.execute("INSERT into philtest.weather_data (temperature,pressure,timestamp) values(%s,%s,%s);",(temperature,pressure,timestamp));
		db.commit();

		output='ok';
		response_headers = [('Content-type', 'text/html'),('Content-Length', str(len(output)))]
		start_response(status, response_headers)

		return [output];

	def get(self,environ,start_response) : 
	        db = MySQLdb.connect(host="localhost",user="pibis",passwd="demopassword",db="philtest");
                cur = db.cursor();

		output = "";
		output += '<body>';
		output += '<link rel="stylesheet" type="text/css" href="/javascript/nv.d3.css" media="screen"/>\n';
		output += '<script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>\n';
		output += '<script src="/javascript/nv.d3.min.js"></script>\n';		
		
		output += ('<div style="height:300;">\n'
	  		'<svg name="tempchart" id="tempchart" width="50" height="50">\n'
	  		'</svg>\n'
	  		'</div>\n'
 
	 		'<div style="height:300;">\n'
	  		'<svg name="pressurechart" id="pressurechart" width="50" height="50">\n'
 	  		'</svg>\n'
	  		'</div>\n')


		cur.execute("SELECT * from philtest.weather_data WHERE timestamp > DATE_SUB(NOW(), INTERVAL 24 HOUR) ORDER BY timestamp;");
		output += '<script>';
		data = cur.fetchall();
		temps = []
		pressures=[]
		index=0;
		for row in data :
			seconds=int(row[3].strftime("%s"))
			temps.append({'y': row[1],'x': seconds})
			pressures.append({'y':row[2],'x': seconds})
			index += 1

		output += '\n temps='+json.dumps(temps)+"\n"
		output += '\n pressures='+json.dumps(pressures)+"\n"
		output += "temp_data = [{values: temps, key: 'temps',color:'#ff7f0e'}]\n";
		output += "pressure_data = [{values: pressures,key:'pressure',color:'#2ca02c'}]\n";

		output += ('nv.addGraph(function() {\n'
		           'var temp_chart = nv.models.lineChart()\n'
                           'temp_chart.xAxis.tickFormat(function(d) {\n'
                           '    if(d == temps[0][\'x\'])\n'
                           '            return (d3.time.format(\'%m-%d-%Y %H:%M\')(new Date(d*1000)));\n'
                           '    else\n'
                           '            return (d3.time.format(\'%H:%M\')(new Date(d*1000)));\n'
                           '    });\n'
			   'temp_chart.yAxis.tickFormat(d3.format(\'0.1f\'));\n'
			   "d3.select('#tempchart').datum(temp_data).call(temp_chart);\n"
			   "nv.utils.windowResize(function() { temp_chart.update() });\n"
			   'return temp_chart});\n')


		output += ('nv.addGraph(function() {\n'
		           'var pressure_chart = nv.models.lineChart()\n'
			   'pressure_chart.xAxis.tickFormat(function(d) {\n'
                	   '	if(d == pressures[0][\'x\'])\n'
                           '		return (d3.time.format(\'%m-%d-%Y %H:%M\')(new Date(d*1000)));\n'
                	   '	else\n'
                           '		return (d3.time.format(\'%H:%M\')(new Date(d*1000)));\n'
                	   '	});\n'
			   "pressure_chart.yAxis.tickFormat(d3.format(\'0.1f\'));\n"
			   "d3.select('#pressurechart').datum(pressure_data).call(pressure_chart);\n"
			   'nv.utils.windowResize(function() { pressure_chart.update() });\n'
			   'return pressure_chart});\n')


		output += '</script>';
		output += '</body>';

		status = '200 OK';
		response_headers = [('Content-type', 'text/html'),('Content-Length', str(len(output)))]
		start_response(status,response_headers);

		return [output];

def test_response(a,b):
        print 'test_response';

if(__name__ == "__main__"):
        environ = {'REQUEST_METHOD': 'PUT','QUERY_STRING': 'pressure=100638.738363&temperature=19.7&timestamp=1413574261'}
	w=weatherlog()
	print w.run_application(environ,test_response)[0]


