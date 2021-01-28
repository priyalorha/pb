from mongoengine import *

connect()


class Images(Document):
    id= IntField(primary_key=True)
    name= StringField()

    meta = {
        'strict': False,
        'collect': 'photobooth'}

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,

        }



