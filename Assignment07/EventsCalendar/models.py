from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User



class Location(models.Model):
    STATE_CHOICES = (
        ('AL', 'ALABAMA'), ('AK', 'ALASKA'), ('AS', 'AMERICAN SAMOA'),
        ('AZ', 'ARIZONA'), ('AR', 'ARKANSAS'), ('CA', 'CALIFORNIA'),
        ('CO', 'COLORADO'), ('CT', 'CONNECTICUT'), ('DE', 'DELAWARE'),
        ('DC', 'DISTRICT OF COLUMBIA'), ('FM', 'FEDERATED STATES OF MICRONESIA'),
        ('FL', 'FLORIDA'), ('GA', 'GEORGIA'), ('GU', 'GUAM'), ('HI', 'HAWAII'),
        ('ID', 'IDAHO'), ('IL', 'ILLINOIS'), ('IN', 'INDIANA'), ('IA', 'IOWA'),
        ('KS', 'KANSAS'), ('KY', 'KENTUCKY'), ('LA', 'LOUISIANA'),
        ('ME', 'MAINE'), ('MH', 'MASHALL ISLANDS'), ('MD', 'MARYLAND'),
        ('MA', 'MASSACHUSETTS'), ('MI', 'MICHIGAN'), ('MN', 'MINNESOTA'),
        ('MS', 'MISSISSIPPI'), ('MO', 'MISSOURI'), ('MT', 'MONTANA'),
        ('NE', 'NEBRASKA'), ('NV', 'NEVADA'), ('NH', 'NEW HAMPSHIRE'),
        ('NJ', 'NEW JERSEY'), ('NM', 'NEW MEXICO'), ('NY', 'NEW YORK'),
        ('NC', 'NORTH CAROLINA'), ('ND', 'NORTH DAKOTA'), ('MP', 'NORTHERN MARIANA ISLANDS'),
        ('OH', 'OHIO'), ('OK', 'OKLAHOMA'), ('OR', 'OREGON'), ('PW', 'PALAU'),
        ('PA', 'PENNSYLVANIA'), ('PR', 'PUERTO RICO'), ('RI', 'RHODE ISLAND'),
        ('SC', 'SOUTH CAROLINA'), ('SD', 'SOUTH DAKOTA'), ('TN', 'TENNESSEE'),
        ('TX', 'TEXAS'), ('UT', 'UTAH'), ('VT', 'VERMONT'),
        ('VI', 'VIRGIN ISLANDS'), ('VA', 'VIRGINIA'), ('WA', 'WASHINGTON'),
        ('WV', 'WEST VIRGINIA'), ('WI', 'WISCONSIN'), ('WY', 'WYOMING'),
    )
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    zip_code = models.CharField(max_length=5)
    desc = models.TextField('Location Description', default='')
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    location = models.ForeignKey(Location)
    date = models.DateField('Event Date')
    start_time = models.TimeField('Start Time', default='00:00:00')
    end_time = models.TimeField('End Time', default='00:00:00')
    desc = models.TextField('Description')
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

class LocationForm(ModelForm):
    class Meta:
        model = Location
        exclude = ('user', 'created')

class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ('user','date', 'created')

