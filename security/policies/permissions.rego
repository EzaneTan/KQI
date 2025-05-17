package kqi.security

# Default deny
default allow = false

# Admins can do anything
allow {
    input.user_role == "admin"
}

# Operators can deploy but not change perms
allow {
    input.user_role == "operator"
    input.action == "deploy"
}

# Auditors can only read logs
allow {
    input.user_role == "auditor"
    input.action == "read_audit"
}
