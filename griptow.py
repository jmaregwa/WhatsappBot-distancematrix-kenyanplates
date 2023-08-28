from flask import Flask, request
import requests
from geopy.distance import geodesic as GD
from twilio.twiml.messaging_response import MessagingResponse
platesfound=False
gkplatesfound=False
locationfound=False
def processing(received):
   
        if received is None:
            print('nothing receiced')
            return('Nothing received')
        print('we are processing...'+received)
        platesfound=received.startswith('k',0)
        gkplatesfound=received.startswith('gk')
        if platesfound or gkplatesfound:
            numberplate=received
            #platesfound=True
            print('number plates found: '+numberplate)
        return platesfound
def distance():
     Mumbai =(19.0760, 72.8777)
     Pune =(18.5204, 73.8567)
 
     print("The distance between Mumbai and Pune is: ", GD(Mumbai,Pune).km)

def location(lat,long,text,address):
     if lat is not None and long is not None:
        
            if text is None:
                text = '/locationdata'
           
            metadata ={'LocationData':{'lat':lat,'long':long,'address':address}}
            print(type(metadata),'printing type of')
            string = str(metadata)
            print(string,"location")
            text = string
            print(lat,long,address)
            locationfound=True
     else:
        locationfound=False
     return locationfound

app = Flask(__name__)
@app.route('/griptow', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    corporate=False
    insuarance=False
    garage=False
    individual=False
    copdesc=False
    print(incoming_msg)
    platesfound=processing(incoming_msg)
    print('plates found status'+ str(platesfound))
    #starting location code
    sender = request.form.get("From", None)
    text = request.form.get("Body", None)

    lat = request.form.get("Latitude",None)
    long = request.form.get("Longitude",None)
    city =  request.form.get("city",None)
    address=request.form.get('Address',None)
    locationfound=location(lat,long,text,address)
    distance()            
    mainmenu='WELCOME TO GRIP AND TOW!\n Select type of Service\n1. Corporate:Insurance Covered\n2. Individual: Self-Sponsored\n'
    typemenu='Select the type of occurence:\n a. Accident related\n b. Breakdown related'
    insuarancemenu='Select the insuarance cover:\n i. Madison \n ii. ICEA\n iii. G.A\n iv. APA'
    if '1' in incoming_msg:
        msg.body(insuarancemenu)
        corporate=True
        responded = True
    if '2' in incoming_msg:
        # security dispatch
        msg.body('individual menu will be here')
        responded = True
        individual=True
    if ('i' in incoming_msg or'ii' in incoming_msg or'iii' in incoming_msg or'iv' in incoming_msg):
        # security dispatch
        msg.body(typemenu)
        responded = True
        individual=True
    if ('a' in incoming_msg or'b' in incoming_msg):
        # security dispatch
        
        msg.body('Enter Number Plate and then drop a location,pin and our agents will reach out shortly')
        responded = True
    if platesfound or gkplatesfound:
        msg.body('Share Location and our agents will contact you shortly')
        responded= True 
    if locationfound:
         msg.body('An agent is calling you shortly\nThank you for contacting Grip and Tow!')
         responded= True
    if not responded:
        msg.body(mainmenu)
    return str(resp)
if __name__ == '__main__':
    app.run(port=4000)