import urllib2
import re

# Googles weather api - http://blog.programmableweb.com/2010/02/08/googles-secret-weather-api/
# according to http://ipinfodb.com/ip_location_api.php
# omitting the IP param will check with my IP
ipinfodb_key = 'a8164d16a7dff696913ab25169789c9a19d954a7f3c1d157ef74e71e697662dd'
ipinfodb_cityURL = 'http://api.ipinfodb.com/v2/ip_query.php?key=%s&timezone=false' % ipinfodb_key
googleWeatherURL = 'http://www.google.com/ig/api?weather=%s'

def getXMLResponse(url):
    print 'getting response from:\n%s\n\n' % url
    resp = urllib2.urlopen(url).read()
    return resp

def getIPInfoDBCityState(xml):
    print 'retrieving the city and state your ip belongs to\n'
    c = re.search('<City>(.*)</City>', xml)
    s = re.search('<RegionName>(.*)</RegionName>', xml)
    city = c.group(1)
    state = s.group(1)
    return '%s, %s' % (city,state)

def getGoogleForecast(googleXMLResponse):
    print 'retrieving forcast from google\n'
    c = googleXMLResponse.split("<current_conditions><condition data=\"")[-1].split("\"")[0]
    return c

if __name__ == '__main__':
    r = getXMLResponse(ipinfodb_cityURL)
    cs = getIPInfoDBCityState(r)
    r = getXMLResponse(googleWeatherURL % urllib2.quote(cs))
    weather = getGoogleForecast(r)
    print "It's going to be %s in %s" % (weather, cs)
