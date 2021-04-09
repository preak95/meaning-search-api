import json
import sys
import pdfplumber
from logger import get_logger
"""
This is meant to:
1. As an input will accept the location of a PDF file
2. Extract text from it and convert it to a list
3.
"""
logger = get_logger(__name__)

def extract_text(file_location):
    # Accept the file location of the pdf file and 
    # then extract text from it and return a list 
    try:
        logger.info("Got the file \"{}\" as input".format(str(file_location)))

        # Try to open the file now and extract all of the text from it
        pdf = pdfplumber.open(file_location)

        word_list = []

        for i in range(len(pdf.pages)):
            text = pdf.pages[i].extract_text().split(" ")
            word_list += text

        return word_list
    except OSError as e:
        logger.error("Error retrieving the file: " + str(file_location) + " - " + str(e))
        return []
    except Exception as e:
        logger.error("An unexpected error occurred: " + str(e))
        return []

if __name__ == '__main__':
    try:
        print(sys.argv[1])
        print(extract_text(sys.argv[1]))
    except Exception as e:
        logger.error("Did you enter the path for the file: " + str(e))
        logger.info("run 'python3 add_item_to_ddb <full_file_path>")