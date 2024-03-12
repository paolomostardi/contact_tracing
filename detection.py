from pymongo import MongoClient

def split_users_in_lists(db, startDate, endDate):
    pipeline = [
        {
            "$match": {
                "Timestamp": {"$gte": startDate, "$lte": endDate}
            }
        },
        {
            "$bucket": {
                "groupBy": "$Timestamp",
                "boundaries": [
                    startDate + i * 5000 for i in range((endDate - startDate).seconds // 5000 + 1)
                ],
                "default": "Other",
                "output": {
                    "documents": {"$push": "$$ROOT"}
                }
            }
        },
        {
            "$unwind": "$documents"
        },
        {
            "$group": {
                "_id": {
                    "Timestamp": "$_id",
                    "X": "$documents.X",
                    "Y": "$documents.Y"
                },
                "users": {"$push": "$documents"}
            }
        }
    ]
    result = db.collection.aggregate(pipeline)


    return list(result)


def detect_collision(db, startDate, endDate):
    list_of_connections = []
    for user_list in split_users_in_lists(db, startDate, endDate):
        users = user_list['users']        
        for i in range(len(users)):
            location = i['location']
            timestamp = i['timestamp']
            for j in range(i + 1, len(users)):
                user1 = users[i]
                user2 = users[j]
                connection = {
                        "user1": user1,
                        "user2": user2,
                        "location": location,
                        "timestamp": timestamp
                    }
                list_of_connections.append(connection)

    return list_of_connections
