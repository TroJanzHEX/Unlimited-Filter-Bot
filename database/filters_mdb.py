import os
import re
import pymongo

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
 
myclient = pymongo.MongoClient(Config.DATABASE_URI)
mydb = myclient['Cluster0']



async def add_filter(message, grp_id, text, reply_text, btn, file):
    mycol = mydb[str(grp_id)]

    try:
        myquery = {'text':text }
        if myquery:
            mycol.delete_one(myquery)
        mycol.insert_one(
            {
                'text':str(text),
                'reply':str(reply_text),
                'btn':str(btn),
                'file':str(file)
            }
        )
    except Exception as e:
        print(e)
             
     
async def find_filter(group_id, name):
    mycol = mydb[str(group_id)]
    
    query = mycol.find( {"text":name})
    for file in query:
        reply_text = file['reply']
        btn = file['btn']
        file = file['file']
    return reply_text,btn,file


async def get_filters(group_id):
    mycol = mydb[str(group_id)]

    texts = []
    query = mycol.find()
    if query is not None:
        for file in query:
            text = file['text']
            texts.append(text)
    return texts


async def delete_fil(message, text, group_id):
    mycol = mydb[str(group_id)]
    
    myquery = {'text':text }
    query = mycol.count_documents(myquery)
    if query == 1:
        mycol.delete_one(myquery)
        await message.reply_text(f'{text} deleted')
    else:
        await message.reply_text("not found")


async def countfilters(group_id):
    mycol = mydb[str(group_id)]

    query = mycol.count()
    if query == 0:
        return 0
    else:
        return query
