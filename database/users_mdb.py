import os
import pymongo

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
 
myclient = pymongo.MongoClient(Config.DATABASE_URI)
mydb = myclient['Cluster0']
mycol = mydb['USERS']



async def adduser(id, username, name, dcid):
    data = {
        '_id': id,
        'username' : username,
        'name' : name,
        'dc_id' : dcid
    }
    try:
        mycol.update_one({'_id': id},  {"$set": data}, upsert=True)
    except:
        pass


async def allusers():
    count = mycol.count()
    return count