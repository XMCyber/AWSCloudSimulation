import asyncio
import glob
import os
import time
from collections import deque
from datetime import datetime


import tinydb
import tinydb.operations
from tinydb import TinyDB
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization import Serializer
from tinydb.storages import MemoryStorage
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

where = tinydb.where
set_value = tinydb.operations.set

class DateTimeSerializer(Serializer):
    OBJ_CLASS = datetime  # The class this serializer handles

    def encode(self, obj):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')

    def decode(self, s):
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')


queues = {}
Query = tinydb.Query


def not_in_list_query(value, all_list):
    def not_in_list(value_test):
        return value_test not in all_list
    return tinydb.Query()[value].test(not_in_list)


QUEUE_MAX_SIZE = 1000 * 1000 * 10

#serialization = SerializationMiddleware()
#serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

dbs = {}

# DB Functions - can be easily replaced with mongo

tdb = None


def get_or_create(db_name):
    global tdb
    if not tdb:
        #tdb = TinyDB('storage' + '.json', storage=CachingMiddleware(JSONStorage))
        tdb = TinyDB('storage' + '.json')
        #tdb = TinyDB(storage=MemoryStorage)
    if db_name not in dbs:
        dbs[db_name] = tdb.table(db_name)
    return dbs[db_name]


def close_dbs():
    global tdb
    if tdb is not None:
        tdb.close()


def clean_all_dbs():
    global tdb
    if tdb is not None:
        tdb.close()
    if os.path.exists('storage.json'):
        os.remove('storage.json')

    for json_path in glob.iglob(os.path.join('.', '*.json')):
        os.remove(json_path)


def insert(db_name, data):
    db = get_or_create(db_name)
    return db.insert(data)


def upsert(db_name, data, query):
    db = get_or_create(db_name)
    return db.upsert(data, query)


def update(db_name, data, query):
    db = get_or_create(db_name)
    return db.update(data, query)


def search(db_name, query):
    db = get_or_create(db_name)
    return db.search(query)


def remove(db_name, query):
    db = get_or_create(db_name)
    return db.remove(query)


def all_records(db_name):
    db = get_or_create(db_name)
    return db.all()


# Streams - can easily replaced with Kafka

def get_push_queue(topic_name):
    if topic_name not in queues:
        queues[topic_name] = {'write_queue': deque([], QUEUE_MAX_SIZE), 'read_queues': []}
    return queues[topic_name]['write_queue']


def get_read_queue(topic_name):
    push_queue = get_push_queue(topic_name)
    new_queue = push_queue.copy()
    queues[topic_name]['read_queues'].append(new_queue)
    return new_queue


def put_in_topic(topic_name, data):
    queue = get_push_queue(topic_name)
    queue.append(data)
    for read_queue in queues[topic_name]['read_queues']:
        read_queue.append(data)


# Streams operations - Can easily replaced with Spark



