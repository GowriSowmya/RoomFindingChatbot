#DB connection
#location_details : {loc, bui, flo, rooms=[]}
#room_details : {room:status}
#user_details : {user, loc, bui, flo, room, occ_time, log_time)

import pymongo
from pymongo import MongoClient
client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')
db = client['RoomFindings']
#collection = db.test
#print(collection.find_one())
#t1 = db.test1.insert_one({"pm2":"hi"})
#print(t1)
'''
l8 = {"loc":"BNG","build":"AB","floor":"8","rooms":["8001","8002","8003","8004","8005","8006"]}
l7 = {"loc":"BNG","build":"AB","floor":"7","rooms":["7001","7002","7003","7004","7005"]}
l6 = {"loc":"BNG","build":"AB","floor":"6","rooms":["6001","6002","6003","6004","6005"]}
l5 = {"loc":"BNG","build":"AB","floor":"5","rooms":["5001","5002","5003","5004","5005","5006","5007"]}

i1 = db.loc_details.insert_many([l8,l7,l6,l5])
print(i1)

L4 = {"loc":"BNG","build":"C","floor":"4","rooms":["4101","4102","4103","4104","4105","4106"]}
L8 = {"loc":"BNG","build":"C","floor":"8","rooms":["8101","8102","8103","8104","8105","8106","8107"]}

i2 = db.loc_details.insert_many([L8,L4])
print(i2)

r1 = {"8001":"y","8002":"n","8003":"y","8004":"n","8005":"y","8006":"n","7001":"n","7002":"n","7003":"n","7004":"y","7005":"y","6001":"n","6002":"n","6003":"y","6004":"n","6005":"y","5001":"n","5002":"n","5003":"y","5004":"y","5005":"n","5006":"y","5007":"n"}
r2 = {"4101":"n","4102":"y","4103":"y","4104":"n","4105":"y","4106":"n","8101":"y","8102":"n","8103":"n","8104":"y","8105":"y","8106":"n","8107":"n"}

i3 = db.room_details.insert_many([r1,r2])
print(i3)

u1 = {"id":"ABCD12","loc":"BNG","build":"AB","floor":"8","room":"8002","occ_time":"30","log_time":"13:24:35"}
u2 = {"id":"WXYZ89","loc":"BNG","build":"C","floor":"4","room":"4101","occ_time":"15","log_time":"05:36:10"}

i4 = db.user_details.insert_many([u1,u2])
print(i4)

myquery = { "floor": "C" }
newvalues = { "$set": { "floor": "4" } }

i5 = db.user_details.update_one(myquery, newvalues)
print(i5)
'''
location = "SBO-BNG"
building = "4AB"
floor = "8"
res = db.loc_details.find_one({"loc":location,"build":building,"floor":floor})
print(res['rooms'])

Room = "8002"
res = db.room_details.find({})
for doc in res:
    for key, val in doc.items():
        if Room in key:
            print(val)
            
uid = 'ABCD12'
res = db.user_details.find()
for doc in res:
    for key, val in doc.items():
        if uid == val:
            print('y',val)

Time = '15 mins'
current_time = "12:37:55"
res = db.user_details.find()
myquery = { "id": user_id }
newvalues = { "$set": { "room": Room, "occ_time": Time.split()[0], "log_time": current_time } }
res = db.user_details.update_one(myquery, newvalues)
print(res)


#free room booked in bot
Room = '7006'
res = db.room_details.find({})
for doc in res:
    for key, val in doc.items():
        if Room in key:
            if val == 'n':
                myquery = { Room: 'n' }
                newvalues = { "$set": { Room: 'y'} }
                r = db.room_details.update_one(myquery, newvalues)
                print(r)
