# trello-export
Create a CSV of Trello cards and actions

## Usage

> ./trello-export-parser.py -h
usage: trello-export-parser.py [-h] [-f FILE] [-p]

Output Trello Cards with Actions by Date

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  json input file
  -p, --print           set to print console output


## Supporting tools 

* explore_json.py: contains support kid functions to descend Trello json trees. Might be easier to visually parse than pretty json. Can be run stand-alone from command line or kidD/kidL functions can be called after import. 

## Other info

* export-test.json is test input file
* export-test.json.csv is expected output 
* trello-extract.ods shows object fields for card and action objects as well as how they map to the csv 
