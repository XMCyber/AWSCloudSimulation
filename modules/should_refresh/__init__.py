import datetime
from modules import simple_storage


def update(topic_name):
    simple_storage.insert("should_refresh", {'topic': topic_name, 'date': datetime.datetime.now()})


def should_refresh(topic):
    db_topic = simple_storage.search("should_refresh", simple_storage.where('topic') == topic)
    if not db_topic:
        return True
    return (datetime.datetime.now() - db_topic[0]['date']).seconds > 60 * 60 * 24
