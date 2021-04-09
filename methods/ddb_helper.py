import json
import pymongo
"""
Going back to the basics and trying to document everything that I come across

One idea was to use the a occal JSON file to store the reverse index instead of 
using a database. But that certianly would not scale. So sticking to a no-SQL database instead.
"""

class DB_client:
    ddb_name = "meaning-search-api-ddb"
    ddb_client = pymongo.MongoClient("mongodb://localhost:27017/")

    def get_ddb_client(self):
        return self.ddb_client

    def create(self, record):
        pass

    def update(self, record):
        pass