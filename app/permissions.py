from flask_principal import Permission, RoleNeed

from app.constants import (ROLE_API_KEY_EDITOR, ROLE_RECORDS_EDITOR,
                           ROLE_USERS_EDITOR)

access_to_users = Permission(RoleNeed(ROLE_USERS_EDITOR))
access_to_records = Permission(RoleNeed(ROLE_RECORDS_EDITOR))
access_to_api_keys = Permission(RoleNeed(ROLE_API_KEY_EDITOR))
