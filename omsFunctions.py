import nltk
import ast
import re
import sys

from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import sentiwordnet


# Pre-processing
def preProcessing(inputFileStr, outputFileStr, printResult):
    inputFile = open(inputFileStr, 'r').read()
    outputFile = open(outputFileStr, 'w+')

    cachedStopWords = nltk.corpus.stopwords.words('english')
    cachedStopWords.append('OMG')
    cachedStopWords.append(':-)')
    result = (' '.join([word for word in inputFile.split() if word.lower() not in cachedStopWords]))

    if (printResult):
        print("Following are the Stop Words")
        print(cachedStopWords)
        print(str(result))

    outputFile.write(str(result))
    outputFile.close()


def tokenizeReviews(inputFileStr, outputFileStr, printResult):
    tokenizedReviews = {}
    inputFile = open(inputFileStr, 'r').read()
    outputFile = open(outputFileStr, 'w')

    tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
    uniqueId = 1
    cachedStopWords = nltk.corpus.stopwords.words("english")

    for sentence in tokenizer.tokenize(inputFile):
        tokenizedReviews[uniqueId] = sentence
        uniqueId += 1

    outputFile.write(str(tokenizedReviews))

    if(printResult):
        for key, value in tokenizedReviews.items():
            print(key, ' ', value)

    outputFile.close()


def posTagging(inputFileStr, outputFileStr, printResult):
    inputFile = open(inputFileStr, 'r').read()
    outputFile = open(outputFileStr, 'w')

    # Split the input, which is the output of a dictionary as text, into a dictionary
    inputTupples = ast.literal_eval(inputFile)
    outputPost = {}

    for key, value in inputTupples.items():
        #print("key", key)
        #print("Value", value)
        outputPost[key] = nltk.pos_tag(nltk.word_tokenize(value))

    if (printResult):
        for key, value in outputPost.items():
            print(key, ' ', value)

    outputFile.write(str(outputPost))
    outputFile.close()


def aspectExtraction(inputFileStr, outputFileStr, printResult):
    inputFile = open(inputFileStr, 'r').read()
    outputFile = open(outputFileStr, 'w')

    inputTupples = ast.literal_eval(inputFile)

    prevWord = ''
    prevTag = ''
    currWord = ''
    aspectList = []
    outputDict = {}

    #Extracting aspects
    for key, value in inputTupples.items():
        for word, tag in value:
            if (tag=='NN' or tag=='NNP'):
                if (prevTag == 'NN' or prevTag=='NNP'):
                    if (prevWord == word):
                        currWord = word     # music music
                    else:
                        currWord = prevWord + ' ' + word
                else:
                    aspectList.append(prevWord.upper())
                    currWord = word

            prevWord = currWord
            prevTag = tag


    #Eliminating aspect wich has 1 or less count
    for aspect in aspectList:
        if(aspectList.count(aspect) > 1):
            if(outputDict.keys() != aspect):
                outputDict[aspect] = aspectList.count(aspect)

    outputAspect = sorted(outputDict.items(), key=lambda x: x[1], reverse=True)

    if(printResult):
        print(outputAspect)

    outputFile.write(str(outputAspect))
    outputFile.close()


def identifyOpinionWords(inputReviewedListStr, inputAspectListStr, outputAspectOpinionListStr, printResult):
    inputReviewList = open(inputReviewedListStr, 'r').read()        # This is POSTagged reviews
    inputAspectList = open(inputAspectListStr, 'r').read()          # This is Aspect list
    outputAspectOpinionList = open(outputAspectOpinionListStr, 'w')

    inputReviewsTupples = ast.literal_eval(inputReviewList)         #POS tags
    inputAspectTupples = ast.literal_eval(inputAspectList)

    outputAspectOpinionTupples = {}
    orientationCache = {}

    negativeWordSet = {"don't","never", "nothing", "nowhere", "noone", "none", "not", "hasn't",
                       "hadn't","can't","couldn't","shouldn't","won't", "wouldn't","don't","doesn't",
                       "didn't","isn't","aren't","ain't"}

    changeDirectionWordSet = {'but', 'than'}

    for aspect, no in inputAspectTupples:
        aspectTokens = word_tokenize(aspect)
        count = 0
        for key, value in inputReviewsTupples.items():
            condition = True
            isNegativeSen = False
            for subWord in aspectTokens:
                if(subWord in str(value).upper()):
                    condition = condition and True

                else:
                    condition = condition and False     # The compound aspect does not exists in this line
                                                        # (problem: it could exist in different parts of the sentence
                                                        # ... Amazon ....... their apps , which is different from
                                                        # Amazon Apps

            if (condition):
                for negWord in negativeWordSet:
                    if(not isNegativeSen): #once sentences is negative no need to check this condition again
                        if negWord.upper() in str(value).upper():
                            isNegativeSen = isNegativeSen or True

                outputAspectOpinionTupples.setdefault(aspect, [0,0,0])

                for word, tag in value:
                    if (tag=='JJ' or tag=='JJR' or tag=='JJS' or tag=='RB' or tag=='RBR' or tag=='RBS'):
                        count+=1
                        if (word not in orientationCache):
                            orien = orientation(word)           # Get the orientation
                            orientationCache[word] = orien
                        else:
                           orien = orientationCache[word]

                        if (isNegativeSen and orien is not None):
                            orien = not orien

                        if (orien == True):
                            outputAspectOpinionTupples[aspect][0] += 1      # Positive

                        elif (orien==False):
                            outputAspectOpinionTupples[aspect][1] += 1      # Negative

                        elif (orien is None):
                            outputAspectOpinionTupples[aspect][2] += 1      # Neutral

        if (count > 0):
            #print(aspect, ' ',  outputAspectOpinionTupples[aspect][0], ' ',
            #                    outputAspectOpinionTupples[aspect][1], ' ',
            #                    outputAspectOpinionTupples[aspect][2])
            outputAspectOpinionTupples[aspect][0] = round((outputAspectOpinionTupples[aspect][0] / count) * 100, 2)
            outputAspectOpinionTupples[aspect][1] = round((outputAspectOpinionTupples[aspect][1] / count) * 100, 2)
            outputAspectOpinionTupples[aspect][2] = round((outputAspectOpinionTupples[aspect][2] / count) * 100, 2)

            print(aspect,
                  ':\t\tPositive => ', outputAspectOpinionTupples[aspect][0],
                  ':\tNegative => ', outputAspectOpinionTupples[aspect][1])

    if (printResult):
        print(outputAspectOpinionList)




    outputAspectOpinionList.write(str(outputAspectOpinionTupples))
    outputAspectOpinionList.close()



def orientation(inputWord):
    wordSynset = wordnet.synsets(inputWord)
    if (len(wordSynset) != 0):
        word = wordSynset[0].name()
        #print("input Word", inputWord)
        #print(word)
        orientation = sentiwordnet.senti_synset(word)
        #print(orientation)
        if(orientation.pos_score() > orientation.neg_score()):
            return True
        elif (orientation.pos_score() < orientation.neg_score()):
            return False













