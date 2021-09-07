import config
import urllib.parse
import re
import json
from urllib.request import Request, urlopen
from lxml.html import parse
from lxml.cssselect import CSSSelector

def Harvester():
  print("Harvesting text content...")
  f = open(config.TEXT, "w") #erase existing content
  f.write("")
  f.close()
  f = open(config.TEXT, "a")
  for source in config.SOURCES:
    try:
      print("Getting category members for:",source)
      url = "https://" + config.LANG + ".wikisource.org/w/api.php?action=query&cmtitle=" + urllib.parse.quote_plus(config.CATEGORY_PREFIX) + ":" + urllib.parse.quote_plus(source) + "&format=json&cmlimit=" + str(config.LIMIT) + "&list=categorymembers"
      with urlopen(Request(url, headers={"User-Agent": config.USER_AGENT})) as response:
        jsonResponse = json.loads(response.read())
        jsonResponse = jsonResponse["query"]["categorymembers"]
        for text in jsonResponse:
          if (text["ns"] != 0):
            #not a text
            continue
          print("  —Getting raw full-text for title",text["title"]);
          textUrl = "https://ws-export.wmcloud.org/?lang=" + config.LANG + "&page=" + urllib.parse.quote_plus(text["title"]) + "&format=txt&fonts="
          print("  —Fetching URL:",textUrl)
          with urlopen(Request(textUrl, headers={"User-Agent": config.USER_AGENT})) as textResponse:
            textResponse = textResponse.read().decode(textResponse.headers.get_content_charset())
            print("  —removing chapter separators")
            content = re.sub("\* \* \*","",textResponse)
            print("  —removing notes")
            content = re.sub("↑ .*","",content)
            print("  —removing line breaks")
            content = re.sub("[\n\r]+"," ",content)
            print("  —removing multiple spaces")
            content = re.sub("\s+"," ",content)
            print("  —removing wikisource credits")
            content = re.sub(config.TEXT_LIMIT+".*","",content)
            if (content != " "):
              f.write(content)
    except Exception as e:
      print("Error on source:",source)
      print(e)
  f.close()
