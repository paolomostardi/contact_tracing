
def trigger_red_user( red_user_id, proximity_db, user_db):
    orange_users = get_users_to_orange(red_user_id, proximity_db)
    orange_users = set_users_to_orange(orange_users, user_db)
    for orange_user in orange_users:
        yellow_users = get_users_to_yellow(orange_user)
        set_users_to_yellow(yellow_users, user_db)

def get_users_to_orange(red_user_id, db):
    
    query = {
        "$or": [
            {"user1": {"$in": red_user_id}},
            {"user2": {"$in": red_user_id}}
        ]
    }

    pairs_users = db.collection.find(query)
    orange_users = []

    for pair in pairs_users:
        if pair['user1'] in red_user_id:
            orange_users.append(pair["user2"])
        else:
            orange_users.append(pair["user1"])

    return orange_users

def set_users_to_orange(orange_users_ids, user_db):
    query = {"_id": {"$in": orange_users_ids}, "state": {"$ne": "red"}}
    update = {"$set": {"state": "orange"}}
    result = user_db.collection.update_many(query, update)
    # Fetch the updated users after the update operation
    updated_users = user_db.collection.find({"_id": {"$in": orange_users_ids}, "state": "orange"})
    orange_users = [user["_id"] for user in updated_users]
    return orange_users   

def get_users_to_yellow(orange_user_id, db):
    
    query = {
        "$or": [
            {"user1": {"$in": orange_user_id}},
            {"user2": {"$in": orange_user_id}}
        ]
    }
    pairs_users = db.collection.find(query)
    yellow_users = []

    for pair in pairs_users:
        
        if pair['user1'] in orange_user_id:
            yellow_users.append(pair["user2"])
        else:
            yellow_users.append(pair["user1"])
    return yellow_users

def set_users_to_yellow(yellow_users_ids, user_db):
    query = {"_id": {"$in": yellow_users_ids}, "state": {"$nin": ["orange", "red"]}}
    update = {"$set": {"state": "yellow"}}
    result = user_db.collection.update_many(query, update)
    # Fetch the updated users after the update operation
    updated_users = user_db.collection.find({"_id": {"$in": yellow_users_ids}, "state": "yellow"})
    yellow_users = [user["_id"] for user in updated_users]
    return yellow_users












