# -*- coding: UTF-8 -*-
import re
import config
import json

class Text:
  def __init__(self):
    self.start = {}
    self.sentences = {}
    self.length = {}
    self.dots = {}
    self.end = {}
    self.prepareText()
    self.analyzeText()

  def __getitem__(self,key):
    if (key == "start"):
      return self.start
    elif (key == "length"):
      return self.length
    elif (key == "dots"):
      return self.dots
    else:
      raise Exception("key "+key+" not subscriptable")

  def prepareText(self):
    print("Preparing text...")
    textFile = open(config.TEXT, "r")
    self.text = textFile.read()
    textFile.close()
    print("  -Removing notes calls...")
    self.text = re.sub("\[\d+\]","",self.text) #remove notes calls
    print("  -Removing linebreaks...")
    self.text = re.sub("[\n\r]+"," ",self.text) #remove linebreaks
    print("  -Normalizing whitespaces...")
    self.text = re.sub("\s+"," ",self.text) #normalize whitespace
    self.text = re.sub("(^\s|\s$)","",self.text) #remove initial & final whitespaces
    print("  -Splitting into words...")
    self.text = re.split(" ",self.text) #split into a list of words

  def analyzeWord(self,word):
    out = { "clean":"", "dot":False }
    out["clean"] = re.sub("([\(\)\.«»!?])","",word)
    if (len(out["clean"]) == 0):
      out["clean"] = False
    if (word[len(word)-1] == "."):
      out["dot"] = "."
    elif ((word == "!") or (word == "?")):
      out["dot"] = word
    return out

  def analyzeText(self):
    newSentence = True
    length = 0
    print("Analyzing text...")
    for i in range(0,len(self.text)):
      word = self.analyzeWord(self.text[i])
      if (word["clean"]):
        if (newSentence):
          self.start[word["clean"]] = self.start.get(word["clean"],0)+1
          length = 0
          newSentence = False
        length += 1
        if (word["dot"]):
          if (word["dot"] != "."):
            end = self.analyzeWord(self.text[i-1])["clean"]
          else:
            end = word["clean"]
          self.length[length] = self.length.get(length,0)+1
          self.dots[word["dot"]] = self.dots.get(word["dot"],0)+1
          if (not newSentence):
            self.end[end] = self.end.get(end,0)+1
          newSentence = True
        if (i < len(self.text)-1):
          nextword = self.analyzeWord(self.text[i+1])
        else:
          nextword = { "clean": False, "dot": False }
        self.sentences[word["clean"]] = self.sentences.get(word["clean"],{"next":{}})
        if (nextword["clean"]) and (not newSentence):
          self.sentences[word["clean"]]["next"][nextword["clean"]] = self.sentences[word["clean"]]["next"].get(nextword["clean"],0)+1

  def getMatrix(self):
    classes = ["start","dots","length"]
    output = {}
    print("Building probabilities matrix...")
    for i in classes:
      v = self[i]
      v = {"v":list(v.keys()), "p": list(v.values())}
      total = sum(v["p"])
      v["p"] = list(map(lambda p: p/total,v["p"]))
      output[i] = v
    for i in self.sentences:
      self.sentences[i] = {"v":list(self.sentences[i]["next"].keys()),"p":list(self.sentences[i]["next"].values())}
      total = sum(self.sentences[i]["p"])
      self.sentences[i]["p"] = list(map(lambda p: p/total,self.sentences[i]["p"]))
    output["structure"] = self.sentences
    output["end"] = self.end
    return output
    

  def exportToJSON(self):
    f = open(config.OUTPUT, "w")
    f.write(json.dumps(self.getMatrix(),ensure_ascii=False))
    print("Export to JSON:",config.OUTPUT)
    f.close()
