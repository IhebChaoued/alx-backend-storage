#!/usr/bin/env python3
"""Schools: topic module"""

from pymongo import MongoClient


def schools_by_topic(mongo_collection, topic):
    """Returns the list of schools having a specific topic"""
    return mongo_collection.find({"topics": topic})
