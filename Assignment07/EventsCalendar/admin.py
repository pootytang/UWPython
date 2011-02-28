from EventsCalendar.models import Event, Location
from django.contrib import admin

# make it so that the Location can be created when the Event object is edited
class LocationAdmin(admin.ModelAdmin):
    pass

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'created')

admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)