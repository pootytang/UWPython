import cherrypy

class PootyTang(object):
    @cherrypy.expose
    def index(self):
        return "Hello from PootyTang"

class Add(object):
    @cherrypy.expose
    def index(self, var1='', var2=''):
        val = 0
        if var1 and var2:
            val = int(var1) + int(var2)
        else:
            val = "You done did it now!!!"

        return val


class BootySweat(object):
    pt = PootyTang()
    add = Add()

    @cherrypy.expose
    def index(self):
        return "BootySweat Engery Drink"

    @cherrypy.expose
    def bs(self):
        return "1 + 2 = %d" % 3

cherrypy.quickstart(BootySweat())
