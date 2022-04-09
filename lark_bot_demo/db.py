from datetime import datetime

from mongoengine import Document, StringField, DateTimeField


class LarkMessage(Document):
    message_id = StringField(required=True, unique=True)
    created = DateTimeField(default=datetime.utcnow)
    meta = {
        'indexes': [{
            'fields': ['created'],
            'expireAfterSeconds': 7 * 24 * 60 * 60
        }]
    }
