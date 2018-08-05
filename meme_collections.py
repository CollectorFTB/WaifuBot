import json
import random

fp = 'data/collections.json'
def get_from_collection(name):
    with open(fp, 'r') as file:
        data = json.load(file)
    name = name.lower()
    if name in data:
        return random.choice(data[name])
    return 'Empty Collection'

def add_to_collection(name, item):
    with open(fp, 'r') as file:
        data = json.load(file)
    name = name.lower()
    if name not in data:
        data[name] = list()
    data[name].append(item)

    with open(fp, 'w') as file:
        json.dump(data, file)

    return 'Added successfully to ' + name + '.'

def delete_from_collection(name, item):
    reply = 'Item removed successfully.'
    with open(fp, 'r') as file:
        data = json.load(file)
    name = name.lower()
    if name in data:
        try:
            data[name].remove(item)
        except ValueError:
            reply = 'Item not in collection.'

    with open(fp, 'w') as file:
        json.dump(data, file)
    return reply
