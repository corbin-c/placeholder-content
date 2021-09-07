import config
import urllib.request
import re
from lxml.html import parse
from lxml.cssselect import CSSSelector

def Harvester():
  print("Harvesting text content...")
  f = open(config.TEXT, "w") #erase existing content
  f.write("")
  f.close()
  f = open(config.TEXT, "a")
  for i in range(0,len(config.SOURCES)):
    try:
      with urllib.request.urlopen(config.SOURCES[i]) as response:
        #html = response.read()
        print("  -Fetching URL:",config.SOURCES[i])
        html = parse(response).getroot()
        for p in html.cssselect("#ws-summary>p"):
          #print("coucou")
          text = p.text_content()
          text = re.sub("[\n\r]+"," ",text)
          text = re.sub("\s+"," ",text)
          if (text != " "):
            f.write(text)
    except:
      print("Error on URL:",config.SOURCES[i])
  f.close()
