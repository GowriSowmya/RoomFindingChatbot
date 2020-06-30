#Creating GUI with tkinter --version 4 - FINAL

import tkinter
import pymongo
from tkinter import *
from datetime import datetime
from pymongo import MongoClient

#include exception handling

def list_rooms(): #get from DB
    global db
    global location
    global building
    global floor
    rooms = []
    res = db.loc_details.find_one({"loc":location,"build":building,"floor":floor})
    if res:
        for i in res['rooms']:
            if check_room(i) == 'yes':
                rooms.append(i)
    return rooms

def check_room(Room): # get from DB
    global db
    res = db.room_details.find({})
    for doc in res:
        for key, val in doc.items():
            if Room in key:
                if val == 'y':
                    return 'yes'
                else:
                    return 'no'
    

def close_window(): #not working, need to check
    global base
    base.quit()
    
def sendk(k):  # 'enter' key event
    send()

def send():
    global Counter
    global user_id
    global Room
    global location
    global building
    global floor
    global db
    print(Counter)
    
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    
    if msg != '':

        if Counter == 0:  # Greetings+ Level 0 Question
            ChatLog.config(state=NORMAL)
            ChatLog.insert(END, "You: " + msg + '\n\n')
            user_id = msg.upper()
            ChatLog.config(foreground="#442265", font=("Verdana", 11 ))
            res = db.user_details.find()
            op = 'new'
            for doc in res:
                for key, val in doc.items():
                    if user_id == val:
                        op = 'old'
            if op == 'new':
                ChatLog.insert(END, "Bot: " + "To Register yourself, please enter location as shown in example \n[eg: SBO-BNG/4AB/5 -> location followed by building_name followed by floor_number]:" + '\n\n')
                user = db.user_details.insert_one({"id":user_id,"loc":"","build":"","floor":"","room":"","occ_time":"0","log_time":""})
                Counter = 7
            else:
                ChatLog.insert(END, "Bot: " + "Please choose location: \n 1. Default location \n 2. Change location " + '\n\n')
                Counter = 1
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)

        elif Counter == 1:  #Level 1 Questions
            ChatLog.config(state=NORMAL)
            ChatLog.insert(END, "You: " + msg + '\n\n')
            ChatLog.config(foreground="#442265", font=("Verdana", 11 ))
            if msg =='1':
                #location = 'SBO-BNG'
                #building = '4C' #get details from user table
                #floor = '8'
                res = db.user_details.find_one({'id':user_id})
                #for doc in res:
                #    for key, val in doc.items():
                #        if user_id == val:
                location = res['loc']
                building = res['build']
                floor = res['floor']
                ChatLog.insert(END, "Bot: " + "Please choose an option (default location): \n 1. Check available rooms \n 2. Check availability of a particular room \n 3. Change location \n 4. Exit" + '\n\n')
                Counter = 2
            elif msg == '2':
                ChatLog.insert(END, "Bot: " + "Please enter alternate location [eg: SBO-BNG/4AB/5 -> location followed by building_name followed by floor_number]: " + "\n\n")
                Counter = 6
            #elif msg == '3':
                #ChatLog.insert(END, "Bot: " + "Please enter location [eg: SBOBNG/4AB/5 -> location followed by building_name followed by floor_number]: " + "\n\n")
                #Counter = 7
            else:
                ChatLog.insert(END, "Bot: " + "Invalid Choice! Please enter a valid option." + '\n\n')
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)

        elif Counter == 2: # level 2 Questions
            ChatLog.config(state=NORMAL)
            ChatLog.insert(END, "You: " + msg + '\n\n')
            if msg == '1':
                res = list_rooms()
                if len(res) == 0:
                    ChatLog.insert(END, "Bot: " + "No rooms available at your location. Press 2 to change location! " + '\n\n')
                    Counter = 6
                else:
                    ChatLog.insert(END, "Bot: " + 'Available rooms: ' + '\n')
                    for i in range(len(res)):
                        ChatLog.insert(END,' ' + str(i+1) + '. ' + res[i] +'\n')
                    ChatLog.insert(END, "Bot: " + "Please select your option from given list: " + '\n\n')
                    Counter = 3
            elif msg == '2':
                ChatLog.insert(END, "Bot: " + "Please enter room number(integer): (eg: 1001)" + '\n\n')
                Counter = 5
            elif msg == '3':
                ChatLog.insert(END, "Bot: " + "Please enter location [eg: SBO-BNG/4AB/5 -> location followed by building_name followed by floor_number]: " + "\n\n")
                Counter = 6
            elif msg == '4':
                ChatLog.insert(END, "Bot: " + "Thank you! Have a Great Day! \n" + 'Please close the window.\n  (or)  \nPress 1 to get back to Start! \n\n')
                Counter = 1
            else:
                ChatLog.insert(END, "Bot: " + "Invalid Choice! Please enter a valid option." + '\n\n')
            ChatLog.config(foreground="#442265", font=("Verdana", 11 ))
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)

        elif Counter == 3: # Level 3 question from Level 2 Question 1
            ChatLog.config(state=NORMAL)
            ChatLog.insert(END, "You: " + msg + '\n\n')
            if msg.isnumeric() == False:
                ChatLog.insert(END, "Bot: " + "Invalid Choice! Please enter a valid option." + '\n\n')
            else:
                msg = int(msg)
                available_rooms = list_rooms()
                if msg > len(available_rooms):
                    ChatLog.insert(END, "Bot: " + "Invalid Choice! Please enter a valid option." + '\n\n')
                else:
                    Room = available_rooms[msg-1]
                    if Room in list_rooms():
                        ChatLog.insert(END, "Bot: " + "Please select your option for time of occupancy: \n 1. 15 mins \n 2. 30 mins \n 3. 45 mins \n 4. 60 mins \n 5. Exit" + '\n\n')
                        Counter = 4
                    else:
                        ChatLog.insert(END, "Bot: " + "Please select your option from given list : " + '\n\n')
            ChatLog.config(foreground="#442265", font=("Verdana", 11 ))
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)
            
        elif Counter == 4: #End Convo
            ChatLog.config(state=NORMAL)
            ChatLog.insert(END, "You: " + msg + '\n\n')
            if msg == '5':
                ChatLog.insert(END, "Bot: " + "Thank you! Have a Great Day! \n" + 'Please close the window.\n   (or) \nPress 1 get back to Start! \n\n')
                Counter = 1
            elif msg in ['1','2','3','4']: #enter details into DB
                Time = {'1':'15 mins','2':'30 mins','3':'45 mins','4':'60 mins'}
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                ChatLog.insert(END, "Bot: User " + user_id + " Occupied Room No. "+ Room  + ' for '+ Time[msg] + ' in location ' + location + '/' + building + '/' + floor + ' at '+ current_time+ ' !! \n\n')
                ChatLog.insert(END, "Bot: " + "Thank you! Have a Great Day! \n" + 'Please close the window.\n   (or) \nPress 1 to get back to Start! \n\n')
                Counter = 1
                res = db.user_details.find()
                myquery = { "id": user_id }
                newvalues = { "$set": { "room": Room, "occ_time": Time[msg].split()[0], "log_time": current_time } }
                db.user_details.update_one(myquery, newvalues)
                res = db.room_details.find()
                #print('room booked : ', Room)
                for doc in res:
                    for key, val in doc.items():
                        if Room in key:
                            if val == 'y':
                                myquery = { Room: 'y' }
                                newvalues = { "$set": { Room: 'n'} }
                                db.room_details.update_one(myquery, newvalues)
            else:
                ChatLog.insert(END, "Bot: " + "Invalid Choice! Please enter a valid option." + '\n\n')
            ChatLog.config(foreground="#442265", font=("Verdana", 11 ))
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)
            
        elif Counter == 5: #Level 3 question from Level 2 Question 2
            ChatLog.config(state=NORMAL)
            ChatLog.insert(END, "You: " + msg + '\n\n')
            Room = msg
            if check_room(Room) == "yes":
                ChatLog.insert(END, "Bot: " + "Yes Room " + Room + " is available.\nPlease select time of occupancy: \n 1. 15 mins \n 2. 30 mins \n 3. 45 mins \n 4. 60 mins \n 5. Exit" + '\n\n')
                Counter = 4
            else:
                ChatLog.insert(END, "Bot: " + "Sorry! Room No." + Room + " is not available. Please Select an option from below list: " + '\n\n')
                res = list_rooms()
                ChatLog.insert(END, "Bot: " + 'Available rooms: ' + '\n')
                for i in range(len(res)):
                    ChatLog.insert(END,' ' + str(i+1) + '. ' + res[i] +'\n')
                Counter = 3
            ChatLog.config(foreground="#442265", font=("Verdana", 11 ))
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)
            
        elif Counter == 6:
            ChatLog.config(state=NORMAL)
            ChatLog.insert(END, "You: " + msg + '\n\n')
            try:
                loc = msg.split('/')
                location = loc[0]
                building = loc[1]
                floor = loc[2]
                ChatLog.insert(END, "Bot: " + "Please choose an option: \n 1. Check available rooms \n 2. Check availability of a particular room \n 3. Change location \n 4. Exit" + '\n\n')
                Counter = 2
            except:
                ChatLog.insert(END, "Bot: " + "Please enter Valid location in format location/building_name/floor_number (eg: SBO-BNG/4AB/5)" + '\n\n')
            ChatLog.config(foreground="#442265", font=("Verdana", 11 ))
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)
            
        elif Counter == 7:
            ChatLog.config(state=NORMAL)
            ChatLog.insert(END, "You: " + msg + '\n\n')
            try:
                loc = msg.split('/')
                location = loc[0]
                building = loc[1]
                floor = loc[2]
                #update details into Database
                res = db.user_details.find()
                myquery = { "id": user_id }
                newvalues = { "$set": { "loc":location, "build":building, "floor":floor } }
                db.user_details.update_one(myquery, newvalues)
                ChatLog.insert(END, "Bot: " + "Please choose an option: \n 1. Check available rooms \n 2. Check availability of a particular room \n 3. Change location \n 4. Exit" + '\n\n')
                Counter = 2
            except:
                ChatLog.insert(END, "Bot: " + "Please enter Valid location in format location/building_name/floor_number (eg: SBO-BNG/4AB/5)" + '\n\n')
            ChatLog.config(foreground="#442265", font=("Verdana", 11 ))
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)
        
Counter = 0
user_id = ""
Room = ""
location = ""
building = ""
floor = ""

client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')
db = client['RoomFinder']

base = Tk()
base.title("Room Finding Chatbot")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)
#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="60", font=("Verdana", 11 ),foreground="#442265",)
ChatLog.insert(END, "Bot: " + "Hello, Greetings for the Day! :) \n\n" + "Please enter your ALIAS ID: " + '\n\n')
ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview)
ChatLog['yscrollcommand'] = scrollbar.set
#Create Button to send message
SendButton = Button(base, font=("Verdana",11,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )
#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font=("Verdana", 11 ))
EntryBox.bind("<Return>", sendk)
#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)
base.mainloop()
