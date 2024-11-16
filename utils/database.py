from __future__ import annotations
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

from utils.calculate import calculate_total_debts
from .password import encode



class MongoDB(object):
    def __init__(self, token: str) -> None:
        self.client = MongoClient(token)
        self.cluster = self.client["spliter"]

        self.users = self.cluster['users']
        self.events = self.cluster['events']
        self.splits = self.cluster['splits']



    def create_user(self, username: str, password: str):
        if self.users.count_documents({"username": username}) == 0:
            user_id = ObjectId()
            
            hashed_password = encode(password)
            
            self.users.insert_one({
                "_id": str(user_id),
                "username": username,
                "password": hashed_password,
            })
            return user_id    
        
        return None



    def login_user(self, username: str):
        user = self.users.find_one({"username":username})
        return user
    
    def get_user_by_id(self, user_id: str):
        return self.users.find_one({"_id": user_id})



    def create_event(self, name: str, image_url: str, creator: str):
        event_id = ObjectId()
        self.events.insert_one({
            "_id": str(event_id),
            "name": name,
            "creator": creator,
            "image_url": image_url
        })
        return event_id



    def find_events(self, creator: str):
        events = list(self.events.find({"creator": creator}))
        for event in events:
            splits = list(self.splits.find({"event": event['_id']}))
            event['count_splits'] = len(splits)
            event['price'] = 0
            event['remains_bill'] = 0
            for split in splits:
                event['price'] += sum([member['amount'] for member in split['members'].values()])
                event['remains_bill'] += sum([member['amount'] for member in split['members'].values() if not member['paid']])
        return events
    
    def create_split(self, name:str, event:str, icon:str, payer:str, members:list):
        splitId =  ObjectId()
        dictSplits = {
            "_id": str(splitId),
            "name": name,
            "event" : event,
            "icon" : icon,
            "payer": payer,
            "members": members
        }
        
        self.splits.insert_one(dictSplits)
        return dictSplits
    
    def find_event_by_id(self, event_id: str):
        splits = list(self.splits.find({"event": event_id}))
        debtors = calculate_total_debts(splits)
        return self.events.find_one({"_id": event_id}), debtors
    
    def get_event_splits(self, event_id: str):
        splits = list(self.splits.find({"event": event_id}))
        for split in splits:
            split['price'] = sum([member['amount'] for member in split['members'].values()])
        return splits
    
    def change_paid(self, event_id: str, username: str, paid: bool):
        for split in self.splits.find({f"members.{username}": {"$exists": True}, "event": event_id}):
            split["members"][username]["paid"] = paid
            self.splits.update_one({"_id": split['_id']}, {"$set": {"members": split['members']}})


    def closeDbConnection(self):
        self.client.close()