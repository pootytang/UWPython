from calendar import HTMLCalendar
from EventsCalendar.models import Event
from datetime import date

# Helpful links
# http://journal.uggedal.com/creating-a-flexible-monthly-calendar-in-django
# http://stackoverflow.com/questions/1101524/python-calendar-htmlcalendar/1458077#1458077

class DsHTMLCalendar(HTMLCalendar):
    def __init__(self, user_id):
        self.user_id = user_id
        super(DsHTMLCalendar, self).__init__()

    def formatday(self, day, weekday):
        '''
                Query mysql database for events for this day and return the table cell
        '''
        isodate = '%s-%s-%s' % (self.year, self.month, day)
        day_span = '<span id="day"><a href="/events/add/%d/%d/%d">%d</a></span>' % (self.year, self.month, day, day)

        if day != 0:
            css = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                css += ' today'

            title_list = self.__get_titles_list__(isodate)
            if len(title_list) > 0:
                # get data from db for day
                css += ' items'
                body = []
                body.append('<span id="event_items">')
                body.append('<ul>')
                for title in title_list:
                    id = title['id']
                    t = title['title']
                    body.append('<li><a href="/event/details/%d">%s</a></li>' % (id, t))
                body.append('</ul>')
                body.append('</span>')
                celldata = '%s %s' % (day_span, ''.join(body))

                return '<td valign="top" class="%s"><div class="day_cell">%s</div></td>' % (css, celldata)
            return '<td class="%s"><div class="day_cell">%s</div></td>' % (css, day_span)
        return '<td class="noday">&nbsp;</td>'
            

    def formatmonth(self, theyear, themonth, withyear=True):
        self.year, self.month = theyear, themonth
        return super(DsHTMLCalendar, self).formatmonth(self.year,self.month,withyear=withyear)

    def __get_titles_list__(self, isodate):
        '''
                returns a list containing a dictionary which contains an id and title key and their corresponding values
                        '''
        events = Event.objects.filter(user__id__exact=self.user_id).filter(date=isodate)
        # events is in the form [{user_id:value, title:value, id:value...}, {...}]
        return [{'id':event['id'], 'title':event['title']} for event in events.values()]