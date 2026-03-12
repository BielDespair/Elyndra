from bson import ObjectId

from ..database import db


def serialize_mongo(doc):

    if isinstance(doc, list):
        return [serialize_mongo(d) for d in doc]

    if isinstance(doc, dict):
        return {k: serialize_mongo(v) for k, v in doc.items()}

    if isinstance(doc, ObjectId):
        return str(doc)

    return doc


def get_forum_posts_repo() -> list[dict]:

    collection = db["forum"]

    posts = list(collection.find())

    return [serialize_mongo(p) for p in posts]