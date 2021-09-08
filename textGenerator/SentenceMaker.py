# -*- coding: UTF-8 -*-
import json
import numpy
import textGenerator.config as config

class SentenceMaker:
  def __init__(self):
    matrixFile = open("textGenerator/"+config.OUTPUT, "r")
    matrix = matrixFile.read()
    matrixFile.close()
    matrix = json.loads(matrix)
    self.start = matrix["start"]
    self.dots = matrix["dots"]
    self.length = matrix["length"]
    self.structure = matrix["structure"]
    self.end = matrix["end"]
    self.makeEnds()

  def makeEnds(self):
    self.fullEnd = { "v":list(self.end.keys()), "p":list(self.end.values()) }
    total = sum(self.fullEnd["p"])
    self.fullEnd["p"] = list(map(lambda p: p/total,self.fullEnd["p"]))

  def makeSentence(self, length=0):
    sentence = []
    startWord = numpy.random.choice(self.start["v"],p=self.start["p"])
    if (length == 0):
      length = numpy.random.choice(self.length["v"],p=self.length["p"])
    dot = numpy.random.choice(self.dots["v"],p=self.dots["p"])
    end = numpy.random.choice(self.fullEnd["v"],p=self.fullEnd["p"])
    sentence.append(startWord)
    for i in range(0,length-2):
      currentWord = self.structure[sentence[len(sentence)-1]]
      if (len(currentWord["v"]) > 0):
        nextWord = numpy.random.choice(currentWord["v"],p=currentWord["p"])
        sentence.append(nextWord)
      else:
        break
    if (dot != "."):
      end = end+" "
    end = end+dot
    sentence.append(end)
    return " ".join(sentence)
