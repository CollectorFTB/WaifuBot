import json
import random


# add new item to collection - .. <collection> <item>
# get item from collection  - ... <collection> - ... <collection>
# remove item from collection - .... <collection> <item>
def handle_collections(message):
    split_message = message.content.split()
    prefix = split_message[0]
    ADD, GET, DELETE = '..',  '...', '....'

    if prefix == DELETE:
        reply = delete_from_collection(split_message[1], " ".join(split_message[2:]))
    if prefix == ADD:
        reply = add_to_collection(split_message[1], " ".join(split_message[2:]))
    if prefix == GET and len(split_message) == 2:
        reply = get_from_collection(split_message[1])
    print(reply)
    return reply


fp = 'data/collections.json'
def get_from_collection(name):
    """Get item from the collection file
    
    Arguments:
        name {str} -- name of collection to retrieve from
    
    Returns:
        [str] -- retrieved item or error message
    """

    with open(fp, 'r') as file:
        data = json.load(file)
    name = name.lower()
    if name in data:
        return random.choice(data[name])
    return 'Empty Collection'

def add_to_collection(name, item):
    """Add item to collection file
    
    Arguments:
        name {str} -- name of collection to retrieve from
        item {str} -- new item to add to the collectoin
    
    Returns:
        str -- status message
    """

    with open(fp, 'r') as file:
        data = json.load(file)
    name = name.lower()
    if name not in data:
        data[name] = list()
    data[name].append(item)

    with open(fp, 'w') as file:
        json.dump(data, file)

    return f'Added successfully to {name}.'

def delete_from_collection(name, item):
    """[summary]
    
    Arguments:
        name {[type]} -- [description]
        item {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

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
