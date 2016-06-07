# coding: utf-8
import urllib.request as urllib
import webbrowser, time
from xml.etree.ElementTree import parse, fromstring, ElementTree
from itertools import chain

officeloc = dict(lat=41.980262, long=-87.668452)

def pollbuses(save=False):
    u = urllib.urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22')
    data = u.read()
    if save:
        with open('rt22.xml', 'wb') as f:
            f.write(data)
    return ElementTree(fromstring(data))

def origbuses():
    return getNorthbound(parse('rt22.xml'))
 
def getNorthbound(doc):
    nb_and_north = dict() #Northbound buses that are north of us
    for bus in doc.findall('bus'):
        if bus.findtext('d') != 'North Bound':
            continue
        if float(bus.findtext('lat')) < officeloc['lat']:
            continue
        nb_and_north[bus.findtext('id')] = float(bus.findtext('lat'))
    return nb_and_north

def distance(lat1, lat2):
    return 69*abs(lat1-lat2)

def popupmap(latlongs):
    baseurl = 'https://maps.googleapis.com/maps/api/staticmap?'
    center = 'center=' + ','.join([str(officeloc['lat']), str(officeloc['long'])])
    size = 'size=600x400'
    zoom = 'zoom=10'
    maptype = 'maptype=roadmap'
    markers = []
    for ll in latlongs:
        markers.append('markers=color:red%7Clabel:'+ll['id']+'%7C'+','.join([ll['lat'], ll['long']]))
    webbrowser.open(baseurl+'&'.join(chain([center, size, zoom, maptype], markers))) 


def monitor():
    doc = pollbuses()
    orig = origbuses()
    latlongs = []
    for bus in doc.findall('bus'):
        busid = bus.findtext('id')
        if busid in orig:
            buslat = float(bus.findtext('lat'))
            print('Bus: ', busid, ' Distance: ', distance(buslat,  officeloc['lat']))
            latlongs.append(dict(id=busid, lat=str(buslat), long=bus.findtext('lon')))
    print('____________________')
    return latlongs
    

def main(display=False):
    while True:
        latlongs = monitor()
        if display:
            popupmap(latlongs)
        time.sleep(60)
