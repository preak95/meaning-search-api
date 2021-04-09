import json

"""
From what I can see, I need to use this file to:
1. Get text using the extract_text module
2. create entries in the database that look like this:

    if <word> in db:
        word: {
                "book_id_1": [<positions_that_the_words_appear_at_in_the_book>],
                "book_id_2": [<positions_that_the_words_appear_at_in_the_book>] 
        }
"""