from flask_principal import Permission, RoleNeed

from app.constants import ROLE_USERS_EDITOR, ROLE_RECORDS_EDITOR

access_to_users = Permission(RoleNeed(ROLE_USERS_EDITOR.get('name')))
access_to_records = Permission(RoleNeed(ROLE_RECORDS_EDITOR.get('name')))
