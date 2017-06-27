import pymongo

# class/static variables, we aren't creating DB objects, instead we are using static methods


class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    # removes self from this method and adds Database as the object
    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    # removes self and adds Database as the object
    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
