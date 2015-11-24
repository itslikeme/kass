import urllib2

var = urllib2.urlopen("http://www.weather.com/weather/today/l/-22.66,-50.42?lat=-22.66&lon=-50.42&locale=pt_BR&temp=com")
html = var.read()
print html
inder = str(html).find('device')
#print str(inder)