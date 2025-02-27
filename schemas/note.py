# this fuction we are writing to convert our mongo dictonary to pytong dictonary
def noteEntity(item)-> dict: 
    return {
        "id":str(item["_id"]),
        "title":item["title"],
        "desc":item["desc"],
        "important":item["important"]

    }
# take input as list and convert into list
def notesEntity(items)-> list: 
    return [noteEntity(item) for item in items]