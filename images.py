import os

from mongoengine import *

connect(os.getenv("MONGODB_URL"))


class Images(Document):
    id = IntField(primary_key=True)
    name = StringField()

    meta = {
        'strict': False,
        'collect': 'photobooth'}

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,

        }
