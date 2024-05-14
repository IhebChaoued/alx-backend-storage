#!/usr/bin/env python3
"""Students's score"""
from pymongo import MongoClient


def top_students(mongo_collection):
    """filter by average score"""
    return mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
                }
            },
        {"$sort": {"averageScore": -1}}
        ])
