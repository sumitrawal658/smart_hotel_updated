from enum import Enum
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserRole(Enum):
    GUEST = "guest"
    STAFF = "staff"
    MANAGER = "manager"
    ADMIN = "admin"

class Permission(Enum):
    VIEW_ROOM = "view_room"
    CONTROL_DEVICES = "control_devices"
    VIEW_ANALYTICS = "view_analytics"
    MANAGE_USERS = "manage_users"
    MANAGE_HOTELS = "manage_hotels"
    VIEW_ALL_ROOMS = "view_all_rooms"
    CONFIGURE_DEVICES = "configure_devices"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Enum(UserRole), default=UserRole.GUEST)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id')) 