import datetime
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, JSONAttribute, ListAttribute
)


class User(Model):

    class Meta:
        table_name = 'User'
        region = 'us-west-2'

    device = UnicodeAttribute(hash_key=True)
    id = NumberAttribute()
    name = UnicodeAttribute(null=True)
    lev = NumberAttribute(default=1)
    xp = NumberAttribute(default=0)
    tickets = NumberAttribute(default=2000)
    play_times = NumberAttribute(default=0)
    pay_times = NumberAttribute(default=0)
    bingo_times = NumberAttribute(default=1)
    fid = NumberAttribute(null=True)
    first_login = UTCDateTimeAttribute(null=True)
    last_login = UTCDateTimeAttribute(null=True)

    @classmethod
    def create_by_device(cls, device):
        user_count = cls.get('user_count')
        try:
            u = cls.get(device)
            return u
        except cls.DoesNotExist:
            u = User(device)
            u.id = user_count.id + 1
            u.name = 'guest_' + str(u.id)
            user_count.update(actions=[User.id.set(User.id + 1)])
            u.save()
            return u

    def buy_cards(self, cards):
        self.tickets -= cards * 10
        self.save()

