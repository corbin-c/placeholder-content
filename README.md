# placeholder-content
provide random JSON content in order to test frontend

## Installation

* Create a python venv: `python3 -m venv ./venv`
* Activate it: `source venv/bin/activate`
* Install requirements: `pip -r requirements.txt`
* Configure the text generator editing the `textGenerator/config.py` file
* Initialize the text generator: `cd textGenerator && python newText.py`
* Launch flask: `export FLASK_APP=randomText.py && flask run`
