from app.models.user import UserRole
from app.models.permission import Permission

ROLE_PERMISSIONS = {
    UserRole.GUEST: {
        Permission.VIEW_ROOM,
        Permission.CONTROL_DEVICES
    },
    UserRole.STAFF: {
        Permission.VIEW_ROOM,
        Permission.CONTROL_DEVICES,
        Permission.VIEW_ALL_ROOMS,
        Permission.VIEW_ANALYTICS
    },
    UserRole.MANAGER: {
        Permission.VIEW_ROOM,
        Permission.CONTROL_DEVICES,
        Permission.VIEW_ALL_ROOMS,
        Permission.VIEW_ANALYTICS,
        Permission.CONFIGURE_DEVICES,
        Permission.MANAGE_USERS
    },
    UserRole.ADMIN: {
        Permission.VIEW_ROOM,
        Permission.CONTROL_DEVICES,
        Permission.VIEW_ALL_ROOMS,
        Permission.VIEW_ANALYTICS,
        Permission.CONFIGURE_DEVICES,
        Permission.MANAGE_USERS,
        Permission.MANAGE_HOTELS
    }
} 