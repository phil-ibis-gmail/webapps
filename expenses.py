import MySQLdb
import urlparse
import sys
import json
import datetime
import decimal
import cgi

class expenses : 
	def application(self,environ,start_response):

		if(environ['REQUEST_METHOD'] == 'GET'):
			if(environ['PATH_INFO'] == '/expenses/details'): 
				return self.get_details(environ,start_response)
			elif(environ['PATH_INFO'] == '/expenses'):
				return self.get_summary(environ,start_response)
		elif(environ['REQUEST_METHOD'] == 'POST'):
			return self.post(environ,start_response)
	
		status = '404 not found';
		output = 'error';
		response_headers = [('Content-type', 'text/html'),('Content-Length', str(len(output)))]
		start_response(status, response_headers)
		return [output]		


	def post(self,environ,start_response) :
		
		status = '200 OK';

		db = MySQLdb.connect(host="localhost",user="pibis",passwd="demopassword",db="philtest");
		cur = db.cursor();

		body_size = int(environ.get('CONTENT_LENGTH',0))
		body_text = environ['wsgi.input'].read(body_size);
		params_dict = urlparse.parse_qs(body_text); 

		#timestamp = datetime.datetime.fromtimestamp(int(params_dict['timestamp'][0]));
		person=params_dict['person'][0]
		amount=decimal.Decimal(params_dict['amount'][0])
		description=params_dict['description'][0]
		category=params_dict['category'][0]
		cur.execute("INSERT into philtest.expenses (timestamp,person,amount,description,category) values(now(),%s,%s,%s,%s);",(person,amount,description,category));
		db.commit();

		output='ok';
		#output += str(params_dict)+'<br>';
		#output += str(environ)+'<br>';
		#output += str(body_text)+'<br>';
		output += '<p> <a href="/apps/expenses"> back </a></p>'		

		response_headers = [('Content-type', 'text/html'),('Content-Length', str(len(output)))]
		start_response(status, response_headers)

		return [output];

	def get_summary(self,environ,start_response) : 
		output = "";

		output += '<form action="expenses" method="post">'
		output += '<p style="text-align:left"><select name="person">'
		output += ' <option value="Phil">Phil</option>'
		output += ' <option value="Christina">Christina</option>'
		output += '</select>'
		output += 'Person </p>'
		output += '<p style="text-align:left"><input type="number" step="any" name="amount"> Amount </p>'
		output += '<p style="text-align:left"><input type="text" name="description">Description</p>'
		output += '<p style="text-align:left"><input type="text" name="category">Category</p>'
		output += '<input type="submit" value="Submit">'
		output += '<p> <a href="/apps/expenses/details"> details </a></p>'
		output += '</form>'
	

		status = '200 OK';
		response_headers = [('Content-type', 'text/html'),('Content-Length', str(len(output)))]
		start_response(status,response_headers);

		return [output];

	def get_details(self,environ,start_response):
	        db = MySQLdb.connect(host="localhost",user="pibis",passwd="demopassword",db="philtest");
                cur = db.cursor();

		cur.execute("SELECT * from philtest.expenses ORDER BY timestamp;");
		output = ''
		data = cur.fetchall();
		for row in data:
			output += cgi.escape(str(row))+'<br/>'
		
		status = '200 OK';
		response_headers = [('Content-type', 'text/html'),('Content-Length', str(len(output)))]
		start_response(status,response_headers);

		return [output]
		
def test_response(a,b):
        print 'test_response';

if(__name__ == "__main__"):
        environ = {'PATH_INFO': '/expenses/details', 'REQUEST_METHOD': 'GET','QUERY_STRING': 'person=phil&amount=1234.5&description=a%20bc&category=house'}
	w=expenses()
	print w.application(environ,test_response)[0]


