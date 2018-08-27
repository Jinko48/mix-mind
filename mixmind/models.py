from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, Enum, Float, Text

from flask_security import UserMixin, RoleMixin

from . import db

class RolesUsers(db.Model):
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String(127), unique=True)
    first_name = Column(String(127))
    last_name = Column(String(127))
    nickname = Column(String(127))
    password = Column(String(127))
    # TODO timezone rip
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(63))
    current_login_ip = Column(String(63))
    login_count = Column(Integer)
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users', backref=backref('users', lazy='dynamic')) # many to many
    orders = relationship('Order') # one to many
    works_at = relationship('Bar', secondary='bartenders', backref=backref('bartenders', lazy='dynamic')) # many to many
    venmo_id = Column(String(63)) # venmo id as a string

    def get_name(self, short=False):
        if short:
            if self.nickname:
                return self.nickname
            else:
                return self.first_name
        return '{} {}'.format(self.first_name, self.last_name)

    def get_role_names(self):
        return ', '.join([role.name for role in self.roles])

class OrdersUsers(db.Model):
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    order_id = Column('order_id', Integer(), ForeignKey('order.id'))

class Order(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    bar_id = Column(Integer, ForeignKey('bar.id'))
    timestamp = Column(DateTime())
    confirmed = Column(Boolean(), default=False)
    recipe_name = Column(String(127))
    recipe_html = Column(Text())

class Bar(db.Model):
    id = Column(Integer(), primary_key=True)
    cname = Column(String(63), unique=True) # unique name for finding the bar
    name = Column(String(63))
    tagline = Column(String(255), default="Tips &mdash; always appreciated, never required")
    is_active = Column(Boolean(), default=False)
    bartender_on_duty = Column(Integer(), ForeignKey('user.id'))
    ingredients = relationship('Ingredient') # one to many
    orders = relationship('Order') # one to many
    # browse display settings
    markup     =  Column(Float(),    default=1.10)
    prices     =  Column(Boolean(),  default=True)
    stats      =  Column(Boolean(),  default=False)
    examples   =  Column(Boolean(),  default=True)
    prep_line  =  Column(Boolean(),  default=False)
    origin     =  Column(Boolean(),  default=False)
    info       =  Column(Boolean(),  default=True)
    variants   =  Column(Boolean(),  default=False)
    summarize  =  Column(Boolean(),  default=True)
    # if I include all_ingredients, we would have to reload the barstock


class Bartenders(db.Model):
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('user.id'))
    bar_id = Column(Integer(), ForeignKey('bar.id'))

