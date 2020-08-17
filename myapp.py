import io
from random import randrange
from flask import Flask, send_file, redirect
from PIL import Image, ImageDraw, ImageFont
app = Flask(__name__)

def serve_pil_image(pil_img):
  img_io = io.BytesIO()
  pil_img.save(img_io, "JPEG", quality=70)
  img_io.seek(0)
  return send_file(img_io, mimetype="image/jpeg")

@app.route("/")
def hello_world():
  return {
      "username": "bob",
      "theme": "coucou",
      "image": "op",
  }

@app.route("/randomImg/<int:minWidth>/<int:maxWidth>/<int:minHeight>/<int:maxHeight>/<string:text>")
@app.route("/randomImg/<int:minWidth>/<int:maxWidth>/<int:minHeight>/<int:maxHeight>/")
@app.route("/randomImg/")
def randomImg(minWidth=0,maxWidth=1000,minHeight=0,maxHeight=1000,text=""):
  # ~ return redirect("/img/"
    # ~ +str(randrange(minWidth,maxWidth))
    # ~ +"/"+str(randrange(minHeight,maxHeight))
    # ~ +"/"+text)
  return generateImg(
    randrange(minWidth,maxWidth),
    randrange(minHeight,maxHeight),
    text)

@app.route("/img/<int:width>/<int:height>/")
@app.route("/img/<int:width>/<int:height>/<string:text>")
def generateImg(width,height,text=""):
  img = Image.new("RGB", (width, height), color = (200, 210, 190))
  if (len(text) > 0):
    font = ImageFont.load_default()
    text_size = font.getsize(text)
    txt = ImageDraw.Draw(img)
    txt.text(((width-text_size[0])/2,(height-text_size[1])/2),
      text,
      fill = (242,105,54),
      font = font)
  return serve_pil_image(img)
