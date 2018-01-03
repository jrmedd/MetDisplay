from flask import Flask, url_for, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

tfgm_api_key = os.environ.get('TFGM_API') #API subscription key available from developer.tfgm.com
api_header = {'Ocp-Apim-Subscription-Key':tfgm_api_key} #the http header for requesting data

@app.route('/display/<stop>')
def display(stop):
    return render_template('display.html',stop=stop,timetable=fetch_timetable(stop))

@app.route('/timetable/<stop>')
def fetch_timetable(stop):
    if request.args.get('api'):
        timetable=api_timetable(stop)
    else:
        timetable=scrape_timetable(stop)
    return timetable

def scrape_timetable(stop):
    stop_url = "https://tfgm.com/public-transport/tram/stops/%s-tram" % (stop.lower().replace(' ', '-')) #TFGM's url convention for tram stops
    page = requests.get(stop_url) #load the page
    soup = BeautifulSoup(page.text, "lxml") #parse the HTML
    table = soup.find('table',attrs={'id':'departures-data'}) #find the departures table
    table_body = table.find('tbody') #grab the table's body
    return table_body #return it as a string

@app.route('/api_timetable/<stop>')
def api_timetable(stop):
    results = requests.get("https://api.tfgm.com/odata/Metrolinks?$filter=StationLocation eq '%s'" % (stop),headers=api_header) #get all Metrolink board times
    boards = results.json().get('value') #create an list of boards per stop
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
    app.run(host="0.0.0.0", debug=True)
