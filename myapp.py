import io
from random import randrange
from flask import Flask, send_file, redirect
from textGenerator.SentenceMaker import SentenceMaker
from PIL import Image, ImageDraw, ImageFont
app = Flask(__name__)

sentenceGenerator = SentenceMaker()

def serve_pil_image(pil_img):
  img_io = io.BytesIO()
  pil_img.save(img_io, "JPEG", quality=100)
  img_io.seek(0)
  return send_file(img_io, mimetype="image/jpeg")

def generateSentences(length):
  sentences = []
  for i in range(0,length):
    sentences.append(sentenceGenerator.makeSentence())
  return sentences

@app.route("/")
@app.route("/full/")
@app.route("/full/<string:messy>")
def hello_world():
  return {
    "username": "bob",
    "theme": "coucou",
    "image": "op",
  }

@app.route("/text-only/")
def textOnly():
  sentences = []
  for i in range(0,20):
    sentences.append(" ".join(generateSentences(randrange(1,12))))
  return {
    "text":sentences
  }

# ~ @app.route("/headers-only/<string:images>")

# ~ @app.route("/images/")
# ~ @app.route("/images/<int:qty>")
# ~ @app.route("/images/<int:qty>/<int:width>/<int:height>/")

@app.route("/randomImg/<int:minWidth>/<int:maxWidth>/<int:minHeight>/<int:maxHeight>/<string:text>")
@app.route("/randomImg/<int:minWidth>/<int:maxWidth>/<int:minHeight>/<int:maxHeight>/")
@app.route("/randomImg/")
def randomImg(minWidth=0,maxWidth=1000,minHeight=0,maxHeight=1000,text=""):
  return generateImg(
    randrange(minWidth,maxWidth),
    randrange(minHeight,maxHeight),
    text)

@app.route("/img/<int:width>/<int:height>/")
@app.route("/img/<int:width>/<int:height>/<string:text>")
def generateImg(width,height,text=""):
  r = randrange(0,255)
  g = randrange(0,255)
  b = randrange(0,255)
  img = Image.new("RGB", (width, height), color = (r,g,b))
  if (len(text) > 0):
    font = ImageFont.load_default()
    text_size = font.getsize(text)
    txt = ImageDraw.Draw(img)
    txt.text(((width-text_size[0])/2,(height-text_size[1])/2),
      text,
      fill = (255-r,255-g,255-b),
      font = font)
  return serve_pil_image(img)
  
@app.route("/sentence/")
def sentence():
  return " ".join(generateSentences(1))
