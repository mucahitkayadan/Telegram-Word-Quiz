# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 14:32:53 2021

@author: muham
"""
import random
import os



class Question(object):
    options = []
    def __init__(self):  
        self.it = []
        self.en = []
        self.options = []
        self.langs = [self.en, self.it]
        Question.start(self)
        
    def checkFile(self, file):
        if not file in os.listdir():
            print('')
            print('ERROR: text file "' + file + '" does not seem to exist')
            print('Did you set up the text file?')
            print('')
            raise IOError
    
    def fileOperations(self):
        Question.checkFile(self,"words.txt")
        with open('words.txt',"r",encoding='utf8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace("\n","")
                line = line.replace(")","")
                if "(" in line:
                    words = line.split("(")
                    self.it.append(words[0])
                    self.en.append(words[1])
                else:
                    line = ""
                    
    def setOptions(self, index, lang):
        #options = []
        nums = list(range(-2,3))
        random.shuffle(nums)
        try:
            for i in range(5):
                self.options.append(lang[index + nums[i]])
                print(str(i+1) + ".  " + str(self.options[i] + "\n"))
        except:
            print("error")
        #checkAnswer()
        
    def checkAnswer(self, answer, langFrom, langTo): 
        if self.options[answer-1] == self.en[Question.ask.number]:
            print("Correct!")
        elif self.options[answer-1] == self.it[Question.ask.number]:
            print("Correct!")
        else:
            print("Incorrect :( ")
        print(langFrom[Question.ask.number] + "  -------->  " + langTo[Question.ask.number])
        
    def ask(self, langFrom, langTo):
        if not len(langFrom) == len(langTo):
            raise Exception("ERROR: Word numbers must be same!")
        Question.ask.number = random.randint(0,len(langFrom))
        print("What is the meaning of " + langFrom[Question.ask.number] + "\n")
        Question.setOptions(self, Question.ask.number,langTo)
    
    def selectLang(self, lang):   
        if lang == 1:
            self.langs[0] = self.en
            self.langs[1] = self.it
        elif lang == 2:
            self.langs[0] = self.it
            self.langs[1] = self.en
        else:
            print("Please just enter 1 or 2!")
        
    def start(self):
        Question.fileOperations(self)
        # lang = int(input("1: English to Italian\n2: Italian to English\n")) 
        # Question.selectLang(self, lang)
        # Question.ask(self, self.langs[0], self.langs[1])
        # answer = int(input("Enter your answer:\n"))
        # Question.checkAnswer(self, answer,self.en,self.it)
        
    

    

