import os
from flask import Flask, render_template
import requests

APP = Flask(__name__)

TFGM_API_KEY = os.environ.get('TFGM_API') #API subscription key available from developer.tfgm.com
API_HEADER = {'Ocp-Apim-Subscription-Key':TFGM_API_KEY} #the http header for requesting data
API_URL = "https://api.tfgm.com/odata/Metrolinks?$filter=StationLocation eq '%s'" #includes station
TABLE_ROW = '<tr><td class="departure-destination">%s</td><td class="departure-wait">%s</td></tr>'
MESSAGE_ROW = '<tbody><tr><td class="scroll" colspan="2"><p>%s</p></td></tr><tbody>'

@APP.route('/display/<stop>')
def display(stop):
    return render_template('display.html', stop=stop, timetable=fetch_timetable(stop))

@APP.route('/timetable/<stop>')
def fetch_timetable(stop):
    results = requests.get(API_URL % (stop), headers=API_HEADER) #get all Metrolink board times
    boards = results.json().get('value') #create an list of boards per stop
    boards = {board.get('AtcoCode'):board for board in boards}.values() #filter duplicate boards
    messages = ('. . .').join(set([board.get('MessageBoard') for board in boards])) #get messages
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
                table += TABLE_ROW % (destination, wait) # make the row
        table += '</tbody>' #end the tbody
    table += MESSAGE_ROW % (messages)
    return table

if __name__ == '__main__':
    APP.run(host="0.0.0.0", debug=True)
