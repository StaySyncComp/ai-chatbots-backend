from api.users import (
    fetch_current_user_data,
    fetch_user_organization_role,
    fetch_all_users,
)

users_functions = {
    "get_user_data": {
        "description": "Fetches user data from the database, including members, customers, and clients.",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "fetcher": fetch_current_user_data,
    },
    "fetch_all_users": {
        "description": "Returns detailed information about all users in the database.",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "fetcher": fetch_all_users,
    },
    "fetch_user_organization_role": {
        "description": "Returns detailed information about current user organizationRole Model",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "fetcher": fetch_user_organization_role,
    },
}
