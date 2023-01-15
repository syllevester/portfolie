#Her bliver der importeret nogle libraries, 
#såsam time.sleep som gør at man kan holde en pause i koden
#PiCamera bliver også importeret så man kan tage billeder, 
#og datetime gør så man kan man kan finde dato og klokkeslæt
from time import sleep
from picamera import PiCamera
from datetime import datetime
from datetime import date

#man definerer variablen "cam" som et nyt object af klassen PiCamera
cam = PiCamera()

def tagbilled():
    #her indstiller man shutterspeeden og iso'en (lysfølsomhed)
    cam.shutter_speed = 6000000
    cam.iso = 600
    #PiCamera.start_preview() starter et livedisplay hvor man kan se kamera inputtet
    cam.start_preview()
    #Ved hjælp af en for-løkke kan man regulere antallet af billeder der bliver taget
    for i in range(5):
        #sleep(1) gør at der er et sekunds pause mellem hver billede
        sleep(1)
        #nowtime=datetime.now() sætter variablen til at indeholde dato og klokkeslæt
        nowtime = datetime.now() #tid tekst
        #funktionen strftime formattere nowtime om til en string. I dette tilfælde i formatet:
        #dag+" "+time+":"+minut+":"+sekund
        timeN = nowtime.strftime("%D: %H:%M:%S") #tid tekst
    
        nowtime2 = datetime.now() #navn tid
        #navnTid er ligesom timeN bare uden dag.
        navnTid = nowtime2.strftime("%H:%M:%S") #navn tid

        #PiCamera.annotate_text gør at man kan skrive på billedet. Her bliver klokkeslættet skrevet på
        #i det første format.
        cam.annotate_text =  str(timeN)
        #Der bliver taget et billede, som bliver lagt i mappen Hawrfr4z med navnet "image"+navnTid+".jpg"
        cam.capture('/home/pi/Hawrfr4z/image%s.jpg' %navnTid)
    #efter der er taget fem billeder stoppet displayet.
    cam.stop_preview()
#Funktionen tagbilled bliver kaldt her. I virkeligheden behøves den ikke at gøres til en funktion,
#men det giver et overblik
tagbilled()