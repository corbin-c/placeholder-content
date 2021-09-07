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

  def makeSentence(self):
    sentence = []
    extra_words = 3
    startWord = numpy.random.choice(self.start["v"],p=self.start["p"])
    length = numpy.random.choice(self.length["v"],p=self.length["p"])
    dot = numpy.random.choice(self.dots["v"],p=self.dots["p"])
    sentence.append(startWord)
    while (True):
      currentWord = self.structure[sentence[len(sentence)-1]]
      if (len(currentWord["v"]) > 0):
        if (len(sentence) >= length-1):
          if (extra_words > 0):
            end = {word: self.end[word] for word in self.end if word in currentWord["v"]}
          else:
            print("fallback to full sentence end");
            end = self.fullEnd
          if (len(end) > 0):
            if (extra_words > 0):
              print("computing end...")
              end = { "v":list(end.keys()), "p":list(end.values()) }
              total = sum(end["p"])
              end["p"] = list(map(lambda p: p/total,end["p"]))
              print("done")
            end = numpy.random.choice(end["v"],p=end["p"])
            sentence.append(end)
            break
          else:
            print(extra_words)
            extra_words -= 1
        nextWord = numpy.random.choice(currentWord["v"],p=currentWord["p"])
        sentence.append(nextWord)
      else:
        break
    if (dot != "."):
      sentence[len(sentence)-1] += " "
    sentence[len(sentence)-1] += dot
    print(sentence)
    return " ".join(sentence)
