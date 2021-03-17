
import os
import pymongo

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
 
myclient = pymongo.MongoClient(Config.DATABASE_URI)
mydb = myclient['Cluster0']
mycol = mydb['connection']   


async def conn_grp(message, grid, usrid):

    data = {
        '_id': str(usrid),
        'group id': str(grid)   
    }

    try:
        mycol.update_one({'_id': str(usrid)},  {"$set": data}, upsert=True)
    except ValidationError:
        logger.exception('Couldnt save, check your db')
    
        
async def find_conn(usrid):

    query = mycol.find( {"_id": usrid} )
    try:
        for file in query:
            grid = file['group id']         
        return grid
    except:
        return None


async def delete_con(message, usrid):
    
    myquery = { "_id": usrid }
    try:
        mycol.delete_one(myquery)
    except:
       await message.reply_text('didnt connected!!', quote=True)
    else:
        await message.reply_text('disconnected',quote=True)
        
