from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from EventsCalendar.models import Event, Location, EventForm, LocationForm
from MyHTMLCalendar import DsHTMLCalendar
from datetime import date
from django.utils.safestring import mark_safe

@login_required
def index(request):
    '''
        Index shows the current month view of a calendar
        user must be logged in to see this
            '''
    r = HttpResponseRedirect('/accounts/login/')
    loggedin = False
    if request.user.is_authenticated():
        loggedin = True
        user = request.user
        today = date.today()
        cal = DsHTMLCalendar(user.id)
        calHTML = cal.formatmonth(today.year, today.month)
        r = render_to_response('EventsCalendar/index.html', {'loggedin':loggedin,'cal': mark_safe(calHTML)})
    return r

@login_required
def month(request):
    '''
        view the calendar for a specific month
        Month and year should be a post variable
            '''
    r = HttpResponseRedirect('/accounts/login/')
    loggedin = False
    if request.user.is_authenticated():
        loggedin = True
        user = request.user
        r = HttpResponseRedirect('/events/')
        if 'month' in request.POST and 'year' in request.POST:
            month = int(request.POST['month'])
            year = int(request.POST['year'])
            cal = DsHTMLCalendar(user.id)
            calHTML = cal.formatmonth(year, month)
            r = render_to_response('EventsCalendar/index.html', {'loggedin':loggedin,'cal': mark_safe(calHTML)})
    return r

@login_required
def year(request):
    '''
        view the calendar for a specific month
        Month and year should be a post variable
            '''
    r = HttpResponseRedirect('/accounts/login/')
    loggedin = False
    if request.user.is_authenticated():
        loggedin = True
        user = request.user
        r = HttpResponseRedirect('/events/')
        if 'year' in request.POST and 'rows' in request.POST:
            year = int(request.POST['year'])
            rows = int(request.POST['rows'])
            cal = DsHTMLCalendar(user.id)
            #cal = HTMLCalendar()
            calHTML = cal.formatyear(year, rows)
            r = render_to_response('EventsCalendar/index.html', {'loggedin':loggedin,'cal': mark_safe(calHTML)})
    return r

@login_required
def details(request, id):
    '''
    Retrieves the event details specified by id
    '''
    loggedin = False
    if request.user.is_authenticated():
        loggedin = True
        user = request.user
        event = Event.objects.filter(user__id__exact=user.id).get(pk=id)
        location = event.location

    return render_to_response('EventsCalendar/details.html', {'loggedin':loggedin, 'e':event, 'l':location})

@login_required
def search_results(request):
    '''
        Displays the results of the search
            '''
    events = []
    user = request.user
    loggedin = True
    if request.method == 'POST' and request.POST['search']:
        search = request.POST['search']
        events = Event.objects.filter(user__id__exact=user.id).filter(title__icontains=search)

    return render_to_response('EventsCalendar/results.html', {'loggedin':loggedin, 'e':events})

@login_required
def add_event(request, year, month, day):
    user = request.user
    loggedin = True
    event_form = EventForm()
    r = render_to_response('EventsCalendar/add_event.html', {'loggedin':loggedin, 'ef':event_form})

    if request.method == 'POST' and request.POST:
        # some of the fields were excluded so need to set them
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            import pprint
            pprint.pprint(dir(event))
            event.user = user
            event.date = '%s-%s-%s' % (year, month, day)
            event.save()
            r = HttpResponseRedirect('/events/')

    return r

@login_required
def add_location(request):
    user = request.user
    loggedin = True
    location_form = LocationForm()
    referer = ''
    if 'HTTP_REFERER' in request.META and 'add' in request.META['HTTP_REFERER']:
        referer = request.META['HTTP_REFERER']
    r = render_to_response('EventsCalendar/add_location.html',
                {'loggedin':loggedin, 'lf':location_form, 'ref':referer})

    if request.method == 'POST' and request.POST:
        location_form = LocationForm(request.POST)
        if location_form.is_valid():
            location = location_form.save(commit=False)
            location.user = user
            location.save()
            # only go here if the was the refering page
            print 'referer' in request.POST
            print request.POST
            if 'referer' in request.POST:
                r = HttpResponseRedirect(request.POST['referer'])
            else:
                r = HttpResponseRedirect('/events/')
    return r

def all_user_events(request):
    user = request.user
    events = Event.objects.filter(user__id=user.id)
    return render_to_response('EventsCalendar/allmyevents.html', {'events':events, 'u':user.username})

def register(request):
    # copied from http://www.djangobook.com/en/2.0/chapter14/
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/events/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {
        'form': form,
    })

def logout(request):
    logout(request)