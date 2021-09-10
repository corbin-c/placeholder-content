# random generator

Python script designed to generate pseudo random text usign Markov Chain. It uses WikiSource to build a model corpus. It can be configured to generate text about a specific thematic by providing it one or several WikiSource categories.

## Installation

* Create a python venv: `python3 -m venv ./venv`
* Activate it: `source venv/bin/activate`
* Install requirements: `pip -r requirements.txt`
* Configure the text generator editing the `textGenerator/config.py` file
* Initialize the text generator: `cd textGenerator && python newText.py`

## Usage
* Launch flask: `export FLASK_APP=randomText.py && flask run`
* Browse to `http://localhost:5000/` to get a list of available routes:
  * `/sentence/`: returns one sentence of random word count
  * `/sentence/<int:sentenceLength>`: returns one sentence of given `sentenceLength` word count
  * `/text/`: returns 20 paragraphs, each composed of 1 to 12 sentences. Each sentence has a random word count.
  * `/text/<int:textLength>`: returns a `textLength` given number of paragraphs, each composed of 1 to 12 sentences. Each sentence has a random word count."
