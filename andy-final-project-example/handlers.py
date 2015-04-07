# TODO : Add comments throughout
# TODO : Minimize everything! LESS CODE, more abstraction
# TODO : Change duplicate names! No lines of code that say examples=examples!
# TODO : Change for loops to not ALL be `for element in elements` No Pluralization magic!

import os
import webapp2
import jinja2
from urlparse import urlparse

from content import COURSES, TOPICS, SECTIONS, CODE_PENS, guestbook_key, Submission, DEFAULT_GUESTBOOK_NAME
import urllib


template_dir = os.path.join(os.path.dirname(__file__), 'html_templates')
jinja_env = jinja2.Environment(
	loader = jinja2.FileSystemLoader(template_dir),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)


class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, courses=COURSES, sections=SECTIONS, **kw))

class MainPage(Handler):
	def get(self):
		self.render("/main_page.html", page_name="home")

class NanodegreeHandler(Handler):
	def get(self):
		self.render('nanodegree_notes.html', page_name="notes")

class CourseHandler(Handler):
	def get(self, course_number):
		self.render("course.html", course_number=int(course_number), course=COURSES[int(course_number)-1], page_name="notes")

class ResourcesHandler(Handler):
	def get(self):
		self.render('additional_resources.html', topics=TOPICS, page_name="resources")

class SubmissionListHandler(Handler):
	def get(self):
		guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		submissions_query = Submission.query(
			ancestor=guestbook_key(guestbook_name)).order(-Submission.date)
		submissions = submissions_query.fetch(10)
		self.render('guestbook.html', submissions=submissions, page_name="submissions")

class SubmissionHandler(Handler):
	def get(self):
		self.render('add_submission.html', page_name="submissions" )
	def post(self):
		guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		submission = Submission(parent=guestbook_key(guestbook_name))
		submission.name = self.request.get('name')
		submission.link = self.request.get('link')
		submission.description = self.request.get('description')
		submission.image_url = self.request.get('image_url')
		submission.put()
		# query_params = {'guestbook_name' : guestbook_name}
		self.redirect('/student_submissions/') # + urllib.urlencode(query_params))

class CodePenExampleListHandler(Handler):
	def get(self, error=False):
		self.render('code_pen_examples.html', examples=CODE_PENS, page_name="codepen")



