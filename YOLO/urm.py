from datetime import datetime, timedelta
from collections import deque

class INGREDIENT:
    def __init__(self, Id, span, inbound_datetime):
        self.id = Id
        self.span = span
        self.inbound_datetime = inbound_datetime
        self.expiration_datetime = inbound_datetime + timedelta(days= span)

    def get_id(self):
        return self.id

    def get_expiration(self):
        return self.expiration_datetime

def stock(to_be_inbound, queue= deque()):
    for i in to_be_inbound:
        queue.append(i)

    expiration_datetimes = [i.get_expiration() for i in queue]
    print(expiration_datetimes[0])
    while queue:
        for d in expiration_datetimes:
            current = datetime.now()
            if current >= d:
                print("*****************")
                print('expired')
                print("*****************")
                break

def get_stock(queue):
    if queue is None:
        print('Your fridge is empty!')
        return None
    
    hashmap = {}
    for i in queue:
        iid  = i.get_id() 
        if str(iid) not in hashmap:
            hashmap[f'{iid}'] = 1
        else:
            hashmap[f'{iid}'] += 1
        
    print(hashmap)


ids = [1, 1, 1, 7, 2, 7, 1]
a = []
for id in ids:
    ingredient = INGREDIENT(id, 1/1440, datetime.now())
    a.append(ingredient)
    print('added')

get_stock(a)