from enum import Enum

class Permission(Enum):
    VIEW_ROOM = "view_room"
    CONTROL_DEVICES = "control_devices"
    VIEW_ALL_ROOMS = "view_all_rooms"
    VIEW_ANALYTICS = "view_analytics"
    CONFIGURE_DEVICES = "configure_devices"
    MANAGE_USERS = "manage_users"
    MANAGE_HOTELS = "manage_hotels"