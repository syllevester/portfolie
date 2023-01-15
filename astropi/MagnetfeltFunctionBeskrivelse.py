#Der bliver her importeret nogle forskellige libraries. Blandt andet skyfield som bruges til
#at finde position af solen og månen.
#Numpy bruges til at finde pi og om math bruges til (arc)sinus, (arc)cosinus og kvadratrod
#Orbit.ISS bruges til at finde ISS's lokation
#sense_hat bruges til at få input fra senserne.
#urllib.request og json bruges til at få json data fra internettet om iss's position
from sense_hat import SenseHat
from math import *
import numpy as np
from orbit import ISS
from skyfield.api import load
import reverse_geocoder
import urllib.request, json
from time import sleep
from picamera import PiCamera
from datetime import datetime
from datetime import date


#Variable position
#Variablerne her bliver defineret her så de er globale, og kan bruges i alle funktioner.
lat=0
lon=0

#sense defineres som et nyt objekt af klassen SenseHat
#comp defineres som en variabel som indeholder kompas-dataen, som kan bruges til magnetfeltet
sense = SenseHat()
comp = sense.get_compass_raw()

#Her definere man t som et "Time" objekt som indeholder tid og dato 
#fra det øbjeklik linjen bliver kørt
t = load.timescale().now()

#Der bliver loadet de421.bsp filen som indeholder det data vi skal bruge.
#Variablerne sun, moon og earth bliver sat til at være objekter,
#der inderholder det data som hører til dem.
eph = load('de421.bsp')
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

#Her finder man solens position i forhold til jorden, på det tidspunkt som blev defineret før.
#Man finder blandt andet RA (right-ascension) og dec (declination), 
#som er koordinater på himlen, som svarer lidt til længdegrad og breddegrad.
#Man finder også afstanden til jorden (det bliver ikke brugt).
sunPosition = earth.at(t).observe(sun)
sra, sdec, distance = sunPosition.radec()

#Her omregner man RA og declination fra radianer til grader.
slon = sra.radians*180/np.pi
slat = sdec.radians*180/np.pi

#variable kamera
cam = PiCamera()

def magnetfelt():
    #til at finde magnetfeltet har vi fundet hjælp her: 
    #https://stackoverflow.com/questions/54370267/normalising-angled-earth-magnetic-field
    #man definere variablerne x, y og z til kompasdata i de retninger.
    #x og z er byttet om på grund af den måde sensehatten sidder på iss.
    x = float(comp["z"]) #nord syd intensitet
    y = float(comp["y"]) #øst vest intensitet
    z = float(comp["x"]) #vertikal intensitet
    #h er den horisontale intensitet i magnetfeltet, som regnes ved hjælp af pytagoras
    #f er den samlede intensitet
    #begge dele printes
    h = sqrt(x ** 2 + y ** 2)
    f = sqrt(h ** 2 + z ** 2)
    print(h)
    print(f)

def ISSLoc():
    #Den måde vi finder ISS's lokation er fra en live api, med en json fil med dataen
    #her loader vi filen og konvertere json filen til et objekt
    url = "http://api.open-notify.org/iss-now.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
      
    # Tager ISS location fra json
    location = result["iss_position"]
    latS = location['latitude']
    lonS = location['longitude']
  
    #konverterer fra string til float + print
    lat = float(latS)
    lon = float(lonS)
    print("\nLatitude: " + str(lat))
    print("\nLongitude: " + str(lon))
    
def vinkel(lat1, lon1, lat2, lon2):
    #I denne funktion regnes mellem ISS og solen med jordens kerne som toppunkt i vinklen
    #Inputtene er i grader, men for at regne med dem med de trigonometriske funktioner,
    #skal de konverteres til radianer, som vi gør her.
    lat1 = lat1*np.pi/180
    lon1 = lon1*np.pi/180
    lat2 = lat2*np.pi/180
    lon2 = lon2*np.pi/180
    #Her regner man vinklen mellem solen og ISS med noget kompliceret matematik
    return 2*asin(sqrt((sin((lat1-lat2)/2))**2 + cos(lat1)*cos(lat2)*(sin((lon1-lon2)/2))**2))

def pvinkel():
    #Her printer man vinklen mellem ISS og solen ved hjælp af funktionen før.
    #Outputtet er dog i radianer som vi regner det om til grader.
    v = vinkel(slat,slon,lat,lon)*180/np.pi
    print(f"vinkel ISS og Solen {v:.4f} grader")


ISSLoc()
pvinkel()



