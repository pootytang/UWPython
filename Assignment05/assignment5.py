#!/usr/bin/python
import threading, cherrypy, os, sys
from bookdb import BookDB

#sys.path.append(os.path.dirname(os.path.abspath(__file__)))

cherrypy.config.update({'environment': 'embedded'})

class BookInfo(object):
    html_head = """
    <html>
    <head><title>Book Info</title></head>
    <body>
    """

    html_end = """
    </body>
    </html>
    """

    home = """<a href="/cpy">home</a>"""
    books = BookDB()

    @cherrypy.expose
    def index(self):
        anchor = ""
        # Books.titles returns a list where each element is a dictionary
        # Each dictionary has an id and a title key
        titles = self.books.titles()
        #return str(titles)
        for item in titles:
            anchor += """
            <a href="/cpy/details?id=%(id)s">%(title)s</a><br />
            """ % item
        return self.html_head + anchor + self.html_end

    @cherrypy.expose
    def details(self, id):
        output = ""
        # By passing in an id to title_info, a dictionary is returned
        # with the a key and the relevant info
        item = self.books.title_info(id)
        for key in item.keys():
            output += """
            <b>%s:</b> %s<br />
            """ % (key, item[key])
        return self.html_head + output + self.home + self.html_end

#cherrypy.quickstart(BookInfo())
application = cherrypy.Application(BookInfo(), script_name=None, config=None)
