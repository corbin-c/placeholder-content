import io
from random import randrange
from flask import Flask, send_file, redirect
from textGenerator.SentenceMaker import SentenceMaker
app = Flask(__name__)

sentenceGenerator = SentenceMaker()

def generateSentences(maxSentences,sentenceLength=0):
  sentences = []
  for i in range(0,maxSentences):
    sentences.append(sentenceGenerator.makeSentence(sentenceLength))
  return sentences

@app.route("/")
def definitions():
  return {
    "routes": {
      "/sentence/": "returns one sentence of random word count",
      "/sentence/<int:sentenceLength>": "returns one sentence of given sentenceLength word count",
      "/text/": "returns 20 paragraphs, each composed of 1 to 12 sentences. Each sentence has a random word count.",
      "/text/<int:textLength>": "returns a textLength given number of paragraphs, each composed of 1 to 12 sentences. Each sentence has a random word count."
    }
  }

@app.route("/sentence/")
@app.route("/sentence/<int:sentenceLength>")
def sentence(sentenceLength=0):
  return {
    "sentence": " ".join(generateSentences(1,sentenceLength))
  }

@app.route("/text/")
@app.route("/text/<int:textLength>")
def textOnly(textLength=20):
  sentences = []
  for i in range(0,textLength):
    sentences.append(" ".join(generateSentences(randrange(1,12))))
  return {
    "text":sentences
  }
