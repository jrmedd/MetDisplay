# Overview

I find Manchester's Metrolink service to be one of the most frustrating daily experiences of my life. [TFGM](https://tfgm.com/)'s attempts at 'smart' infrastructure have [largely failed](https://startupsventurecapital.com/a-beginners-guide-to-using-my-get-me-there-manchester-s-hilarious-attempt-at-reinventing-london-s-70a6d1dde246) or passed me by so far, so while I'm waiting for great innovation to happen, I thought I'd write up an arrivals board for the office to replicate those found at the tram stops:

![Scrape Example](https://github.com/jrmedd/MetDisplay/blob/master/board_example.png?raw=true)

## Usage

I use [Flask](http://flask.pocoo.org/docs/0.12/quickstart/) to run the application, displaying only the variety of information found on the displays on the tramstops. This information is reloaded (using AJAX) after a scrolling message has finished being displayed, or every 50 seconds.

To use, you need an API key from https://developer.tfgm.com/, and to create an environment variable called 'TFGM_API'
