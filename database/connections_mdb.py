import os
import pymongo

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
 
myclient = pymongo.MongoClient(Config.DATABASE_URI)
mydb = myclient[Config.DATABASE_NAME]
mycol = mydb['CONNECTION']   


async def add_connection(group_id, user_id):
    query = mycol.find_one(
        { "_id": user_id },
        { "_id": 0, "active_group": 0 }
    )
    if query is not None:
        group_ids = []
        for x in query["group_details"]:
            group_ids.append(x["group_id"])

        if group_id in group_ids:
            return False

    group_details = {
        "group_id" : group_id
    }

    data = {
        '_id': user_id,
        'group_details' : [group_details],
        'active_group' : group_id,
    }
    
    if mycol.count_documents( {"_id": user_id} ) == 0:
        try:
            mycol.insert_one(data)
            return True
        except:
            print('Some error occured!')

    else:
        try:
            mycol.update_one(
                {'_id': user_id},
                {
                    "$push": {"group_details": group_details},
                    "$set": {"active_group" : group_id}
                }
            )
            return True
        except:
            print('Some error occured!')

        
async def active_connection(user_id):

    query = mycol.find_one(
        { "_id": user_id },
        { "_id": 0, "group_details": 0 }
    )
    if query:
        group_id = query['active_group']
        if group_id != None:
            return int(group_id)
        else:
            return None
    else:
        return None


async def all_connections(user_id):
    query = mycol.find_one(
        { "_id": user_id },
        { "_id": 0, "active_group": 0 }
    )
    if query is not None:
        group_ids = []
        for x in query["group_details"]:
            group_ids.append(x["group_id"])
        return group_ids
    else:
        return None


async def if_active(user_id, group_id):
    query = mycol.find_one(
        { "_id": user_id },
        { "_id": 0, "group_details": 0 }
    )
    if query is not None:
        if query['active_group'] == group_id:
            return True
        else:
            return False
    else:
        return False


async def make_active(user_id, group_id):
    update = mycol.update_one(
        {'_id': user_id},
        {"$set": {"active_group" : group_id}}
    )
    if update.modified_count == 0:
        return False
    else:
        return True


async def make_inactive(user_id):
    update = mycol.update_one(
        {'_id': user_id},
        {"$set": {"active_group" : None}}
    )
    if update.modified_count == 0:
        return False
    else:
        return True


async def delete_connection(user_id, group_id):

    try:
        update = mycol.update_one(
            {"_id": user_id},
            {"$pull" : { "group_details" : {"group_id":group_id} } }
        )
        if update.modified_count == 0:
            return False
        else:
            query = mycol.find_one(
                { "_id": user_id },
                { "_id": 0 }
            )
            if len(query["group_details"]) >= 1:
                if query['active_group'] == group_id:
                    prvs_group_id = query["group_details"][len(query["group_details"]) - 1]["group_id"]

                    mycol.update_one(
                        {'_id': user_id},
                        {"$set": {"active_group" : prvs_group_id}}
                    )
            else:
                mycol.update_one(
                    {'_id': user_id},
                    {"$set": {"active_group" : None}}
                )                    
            return True
    except Exception as e:
        print(e)
        return False

