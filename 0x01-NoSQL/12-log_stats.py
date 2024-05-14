#!/usr/bin/env python3
"""Nginx logs"""

from pymongo import MongoClient


def log_stats():
    """Prints some stats about Nginx logs stored in MongoDB"""

    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    total_logs = collection.count_documents({})

    print("{} logs".format(total_logs))
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))

    status_check = collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(status_check))


if __name__ == "__main__":
    log_stats()
