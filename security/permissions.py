from enum import Enum, auto

class Permission(Enum):
    """
    Enumeration of all possible permissions in the KQI platform.
    """
    CREATE_AGENT = auto()
    DEPLOY_AGENT = auto()
    VIEW_AGENT = auto()
    EDIT_AGENT = auto()
    DELETE_AGENT = auto()
    VIEW_REPORTS = auto()
    OPTIMIZE_AGENT = auto()
    MANAGE_USERS = auto()

class PermissionsManager:
    """
    Manages permissions for users and roles.
    """

    def __init__(self):
        self.roles_permissions = {}  # Maps roles to their permissions

    def add_role_permissions(self, role: str, permissions: list) -> None:
        """
        Add permissions to a role.

        Args:
            role (str): The name of the role.
            permissions (list): List of Permission enums.
        """
        if role not in self.roles_permissions:
            self.roles_permissions[role] = set()
        self.roles_permissions[role].update(permissions)

    def has_permission(self, role: str, permission: Permission) -> bool:
        """
        Check if a role has a specific permission.

        Args:
            role (str): The name of the role.
            permission (Permission): The permission to check.

        Returns:
            bool: True if the role has the permission, False otherwise.
        """
        return permission in self.roles_permissions.get(role, set())