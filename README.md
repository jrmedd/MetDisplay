# Overview

I find Manchester's Metrolink service to be one of the most frustrating daily experiences of my life. [TFGM](https://tfgm.com/)'s attempts at 'smart' infrastructure have [largely failed](https://startupsventurecapital.com/a-beginners-guide-to-using-my-get-me-there-manchester-s-hilarious-attempt-at-reinventing-london-s-70a6d1dde246) or passed me by so far, so while I'm waiting for great innovation to happen, I thought I'd write up an arrivals board for the office to replicate those found at the tram stops:

![Scrape Example](https://github.com/jrmedd/MetDisplay/blob/master/scrape_board.png?raw=true)

## Usage

I use [Flask](http://flask.pocoo.org/docs/0.12/quickstart/) to run the application, displaying only the variety of information found on the displays on the tramstops. This information is reloaded (using AJAX) every 30 seconds.

When I started writing this, I had no idea there was an API available for this info, so I had to scrape the data from TFGM's live departures page using [Requests](http://docs.python-requests.org/en/master/)/[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/). This still works if you run the app and go to http://127.0.0.1:5000/display/MediaCityUK.

If you want to make use of the API, get a key from https://developer.tfgm.com/ and create an environment variable called 'TFGM_API'. By appending ***?api=anything*** to the aforementioned display URL, you'll get a table for each LED board at that station.
