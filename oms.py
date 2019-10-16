'''
Implementing Opinion Mining with Python
https://dzone.com/articles/opinion-mining-python-implementation
'''


import omsFunctions

def printResultChoice():
    userChoice = str(input("\nDo you want to print the result on output window? (Y/N) :"))
    if (userChoice == 'Y' or userChoice == 'y'):
        return True
    else:
        return False


if __name__ == "__main__":


    _FolderName = 'Data/Iberostar/' #'Data/MotoXPlay/'
    _ReviewDataset = _FolderName + '0.ReviewDataset.txt'
    _PreProcessedData = _FolderName + '1.PreprocessedData.txt'
    _TokenizedReviews = _FolderName + '2.TokenizedReviews.txt'
    _PosTaggerReviews = _FolderName + '3.PosTaggedReviews.txt'
    _Aspects = _FolderName + '4.Aspects.txt'
    _Opinions = _FolderName + '5.Opinions.txt'

    print("\nWelcome to Opinion Mining System ")
    print("------------------------------------------------")
    print("Please enter any key to continue... ")

    print("\n\n\n\nPreprocessing Data...")
    omsFunctions.preProcessing(_ReviewDataset, _PreProcessedData, printResultChoice())

    print("\n\n\n\nReading Review Collection...")
    omsFunctions.tokenizeReviews(_ReviewDataset, _TokenizedReviews, printResultChoice())

    print("\n\n\n\nPart of Speech Tagging...")
    omsFunctions.posTagging(_TokenizedReviews, _PosTaggerReviews, printResultChoice())

    print("\nThis function will list all the nouns as aspect.")
    omsFunctions.aspectExtraction(_PosTaggerReviews, _Aspects, printResultChoice())

    print("\n\n\n\nIdentifying Opinion Words...")
    omsFunctions.identifyOpinionWords(_PosTaggerReviews, _Aspects, _Opinions, printResultChoice())