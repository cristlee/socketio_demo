import datetime
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, JSONAttribute, ListAttribute, BooleanAttribute
)


class User(Model):

    class Meta:
        table_name = 'User'
        region = 'us-west-2'

    device = UnicodeAttribute(hash_key=True)
    id = NumberAttribute()
    name = UnicodeAttribute(null=True)
    photo_url = UnicodeAttribute(null=True)
    lev = NumberAttribute(default=1)
    xp = NumberAttribute(default=0)
    tickets = NumberAttribute(default=2000)
    play_times = NumberAttribute(default=0)
    pay_times = NumberAttribute(default=0)
    bingo_times = NumberAttribute(default=1)
    fid = NumberAttribute(null=True)
    first_login = UTCDateTimeAttribute(null=True)
    last_login = UTCDateTimeAttribute(null=True)
    email = UnicodeAttribute(null=True)
    token = UnicodeAttribute(null=True)
    pk = UnicodeAttribute(null=True)
    card_data = ListAttribute(null=True)

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


class Room(Model):

    class Meta:
        table_name = 'Room'
        region = 'us-west-2'

    id = NumberAttribute(hash_key=True)
    tid = NumberAttribute()
    status = BooleanAttribute(default=True)
    runrobot = BooleanAttribute(default=True)
    goingdown = BooleanAttribute(default=True)
    start_time = UTCDateTimeAttribute(null=True)
    seqnumbers = ListAttribute(null=True)
    nextseqnumbers = ListAttribute(null=True)
    readcount = NumberAttribute(default=0)
    population = NumberAttribute(default=0)
    player = NumberAttribute(default=0)
    card = NumberAttribute(default=0)
    robot = NumberAttribute(default=0)
    robotcard = NumberAttribute(default=0)
    totalbingo = NumberAttribute(default=0)
    bingoleft = NumberAttribute(default=0)
    ranklist = ListAttribute(null=True)

    def join(self):
        self.update(actions=[Room.player.set(Room.player + 1)])


class Purchase(Model):

    class Meta:
        table_name = 'Purchase'
        region = 'us-west-2'

    identifier = UnicodeAttribute(hash_key=True)
    time = UTCDateTimeAttribute(null=True)
    uid = NumberAttribute(default=0)
    tickets = NumberAttribute(default=0)
    powerups = NumberAttribute(default=0)
    items = UnicodeAttribute(null=True)

# Room.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
