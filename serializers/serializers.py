def decodeblog(doc) -> dict:
    return {
        "id":str(doc["_id"]),
        "title": doc["title"],
        "subtitle":doc["subtitle"],
        "content": doc["content"],
        "author":doc["author"],
        "date": doc["date"],

        
    }
def decodeblogs(docs)-> list:
    return [decodeblog(doc) for doc in docs]
