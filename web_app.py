import os
from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

APP = Flask(__name__)

TFGM_API_KEY = os.environ.get('TFGM_API') #API subscription key available from developer.tfgm.com
API_HEADER = {'Ocp-Apim-Subscription-Key':TFGM_API_KEY} #the http header for requesting data

@APP.route('/display/<stop>')
def display(stop):
    return render_template('display.html', stop=stop, timetable=fetch_timetable(stop))

@APP.route('/timetable/<stop>')
def fetch_timetable(stop):
    if request.args.get('api'):
        timetable = api_timetable(stop)
    else:
        timetable = scrape_timetable(stop)
    return timetable

def scrape_timetable(stop):
    stop_url = "https://tfgm.com/public-transport/tram/stops/%s-tram" % (stop.lower().replace(' ', '-')) #TFGM's url convention for tram stops
    page = requests.get(stop_url) #load the page
    soup = BeautifulSoup(page.text, "lxml") #parse the HTML
    table = soup.find('table', attrs={'id':'departures-data'}) #find the departures table
    table_body = table.find('tbody') #grab the table's body
    return table_body #return it as a string

def api_timetable(stop):
    results = requests.get("https://api.tfgm.com/odata/Metrolinks?$filter=StationLocation eq '%s'" % (stop), headers=API_HEADER) #get all Metrolink board times
    boards = results.json().get('value') #create an list of boards per stop
    boards = {board.get('AtcoCode'):board for board in boards}.values() #filter out duplicate boards per platform using the Atco codes
    table = "" #create empty table string to pass to browser
    for board in boards:
        table += '<tbody>'#start a new tbody per board
        for i in range(3): #iterate over the next 3 arrivals
            destination = board.get('Dest%d'%(i)) # get destination
            status = board.get('Status%d'%(i)) # get status (due, arriving, departing)
            if status == 'Due':
                wait = "%s mins" % (board.get('Wait%d'%(i))) # if it's due, display the wait
            else:
                wait = status # otherwise display the status
            if destination:
                table += '<tr><td class="departure-destination">%s</td><td class="departure-wait">%s</td></tr>' % (destination, wait) # make the row
        table += '</tbody>' #end the tbody
    return table

if __name__ == '__main__':
    APP.run(host="0.0.0.0", debug=True)
