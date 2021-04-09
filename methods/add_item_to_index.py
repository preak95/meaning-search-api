import json
import re
import hashlib
import os
import sys
import time
from logger import get_logger
from pymongo import MongoClient
from extract_text import extract_text

logger = get_logger(__name__)
"""
Documentation

Hello there. For the purpose of eas in understanding this project at later times in life, and also
for the purpose of the understanding of others, I intend to heavily and very extensively documents
this python file and all the python files to come. Thank you. Enjoy coding.


The purpose of this script:
This script is meant to enable the user to choose a particular df file of their choice
and create an inverted idex like data structure for the same.

How?
1. Open the respective text file and extract all the words(let them repeat. We want all the
    words in their order) into a list

2. We'll use dictionaries for maintaining abstraction
                uniqueWordEntry {
                    "word"     : ___What word it is___,
                    "BookId"   : ___The ID of the book___,
                    "Position" : ___Array of numbers representing the position of words in the book"
                }

                //We'll try and implement auto-increment for bookID so we won't need to maintain them
                 anywhere else

3. We will scan through each of the words in the text file,
    If "The word is present in the index" :
        Update the item whose ID corresponds to the book we are scanning
        (In this case, even if the book didn't exist, it will create it for us)
    elif "word absent" :
        Enter the words and enter the details as mentioned in the above mentioned dictionary
"""

# Create a new connection to a single MongoDB instance at host:port.
connection = MongoClient()
db = connection.wordsearch

# This is a different part where I will try and make use of hash
# tables to deal with the problem

def create_index_from_words(wordarray, filename):
    wordHashTable = {}
    wordfrequency = {}
    pos = 1
    for word in wordarray:
        if word.lower() not in wordHashTable:
            wordHashTable[word.lower()] = [pos]
        else:
            wordHashTable[word.lower()].append(pos)

        if word.lower() not in wordfrequency:
            wordfrequency[word.lower()] = 1
        else:
            wordfrequency[word.lower()] += 1

        pos += 1

    wordDictionaryList = []
    filename = os.path.basename(filename)
    for k in wordHashTable:
        wordDictionaryList.append({
            'word': k,
            'positions': wordHashTable[k],
            'fileName': str(filename)
        })

    for word in wordfrequency:
        # This would deal with maintaining a frequency of words
        db.freq.update_one({
            "word": word
        }, {
            "$inc": {"count": wordfrequency[word]}
        }, True)

    for word in wordDictionaryList:
        db.index.insert_one({
            "word": word['word'],
            "positions": word['positions'],
            "fileName": word['fileName']
        })


def filechooser(dir):
    for txtfile in os.listdir(dir): #iterate through pdfs in pdf directory
        fileExtension = txtfile.split(".")[-1]
        wordarray = []
        if fileExtension == "txt":
            textfile = open(dir + txtfile)
            wordarray = re.compile('\w+').findall(textfile.read())

            # Extract the name of the book
            filename = re.compile("(.*/)*").split(textfile.name)[-1]

            create_index_from_words(wordarray, textfile)
            # This line is to make sure we add the name of the file that is being added,
            # so we do not add it again in future
            db.allFileDirectory.insert({"filename": str(filename), "timestamp": time.ctime()})

            # This line is supposed to add the wordarray along with the filename
            # so as to allow us too gain access to all the words of a particular book
            db.wordsInFileList.insert({"filename": filename, "wordlist": wordarray})
            logger.info("Added to index: " + filename)

# Execution

if __name__ == '__main__':
    try:
        logger.info("Trying to extract text from the specified file")
        word_list = extract_text(sys.argv[1])
        create_index_from_words(word_list, sys.argv[1])

    except Exception as e:
        logger.error("Did you enter the path for the file: " + str(e))
        logger.info("run 'python3 add_item_to_index <full_file_path>")
