import webapp2
import cgi
from google.appengine.ext import db
import jinja2
import os
import datetime

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class student(db.Model):
   """Models a student detail entry with name, roll number, DOB, Mark"""
   Name = db.StringProperty()
   Sex = db.StringProperty()
   Age = db.StringProperty()
   DOB = db.StringProperty()
   Mark = db.StringProperty()
   Date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'html'
        template = jinja_environment.get_template('main.html')
        self.response.out.write(template.render({}));

class details(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('details.html')
        self.response.out.write(template.render({}));
    def post(self):
        name = self.request.get('studentname')
        sex = self.request.get('sex')
        age = self.request.get('age') 
        dob = self.request.get('dob')
        mark = self.request.get('mark')
        data = student(key_name=name, Name=name,Sex=sex ,Age=age, DOB=dob, Mark=mark)   
        data.put()
        self.redirect("/")
class view(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'html'
	self.response.write("""<html>
         <head>
         <title>Student Details</title>
         <link rel="stylesheet" type="text/css" href="/stylesheets/remove.css" />
          </head>
          <h1>STUDENT DETAILS</h1>
          <h3>Details of all students:</h3>
          </html>
                      """)
        details = db.GqlQuery('SELECT * FROM student ORDER BY Date DESC')
	self.response.headers['Content-Type'] = 'html' 
        for i in details:
      	    self.response.write('<p>'+i.Name +'    '+i.Sex+'    '+i.Age+'     '+i.DOB+'      '+i.Mark+ '</p>')
class sort_age(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'html'
	self.response.write("""<html>
          <head>
          <title>Student Details</title>
          <link rel="stylesheet" type="text/css" href="/stylesheets/remove.css" />
          </head>
          <body>
          <h1>STUDENT DETAILS</h1>
           <h3>Details of all students sorted by Age:</h3>
            </body>
            </html> """)
	details = db.GqlQuery('SELECT * FROM student ORDER BY Age ASC')
	self.response.headers['Content-Type'] = 'html'	
	for i in details:
      	    self.response.write('<p>'+i.Name +' '+i.Sex+' '+i.Age +' '+i.DOB+' '+i.Mark+ '</p>')

class sort_mark(webapp2.RequestHandler):
    def get(self):
	self.response.headers['Content-Type'] = 'html'
	self.response.write("""<html>
          <head>
          <title>Student Details</title>
          <link rel="stylesheet" type="text/css" href="/stylesheets/remove.css" />
          </head>
          <body>
          <h1>STUDENT DETAILS</h1>
           <h3>Details of all students sorted by Mark:</h3>
            </body>
            </html> """)
        details=db.GqlQuery('SELECT * FROM student ORDER BY Mark DESC')
        self.response.headers['Content-Type'] = 'html'
	for i in details:
      	    self.response.write('<p>'+i.Name +' '+i.Sex+' '+i.Age +' '+i.DOB+' '+i.Mark+ '</p>')

class remove_details(webapp2.RequestHandler):
    def get(self):
      	self.response.headers['Content-Type'] = 'html'
        template = jinja_environment.get_template('remove_details.html')
        self.response.out.write(template.render({}));         
    def post(self):
	remove_details=self.request.get('remove_details')
	address_key = db.Key.from_path('student', remove_details)
	db.delete(address_key)
        self.response.write("""<html>
          <head>
          <title>Student Details</title>
          <link rel="stylesheet" type="text/css" href="/stylesheets/remove.css" />
          </head>
          <body>
          <h1>STUDENT DETAILS</h1>
          <h2><center>!!_______ Deleted _______!!
                   </center></h2></html>""")

class search_details(webapp2.RequestHandler):		
    def get(self):	
	self.response.headers['Content-Type'] = 'html'
        template = jinja_environment.get_template('search.html')
        self.response.out.write(template.render({}));

class searchresult(webapp2.RequestHandler):
    def post(self):
	search=self.request.get('search')
	data = db.GqlQuery("""SELECT * FROM student WHERE Name = :1 """, search)
	self.response.headers['Content-Type'] = 'html'
        self.response.write("""<html>
          <head>
          <title>Student Details</title>
          <link rel="stylesheet" type="text/css" href="/stylesheets/remove.css" />
          </head>
          <body>
          <h1>STUDENT DETAILS</h1>
           <h3>Search Result:</h3>
            </body>
            </html> """)		
	for i in data:
      	    self.response.write('<p>'+i.Name +' '+i.Sex+' '+i.Age+' '+i.DOB+' '+i.Mark+ '</p>')
app = webapp2.WSGIApplication([('/', MainPage),('/details', details),('/view', view), ('/sort_age', sort_age), ('/sort_mark', sort_mark), ('/search_details', search_details), ('/remove_details', remove_details), ('/searchresult', searchresult)], debug=True)
