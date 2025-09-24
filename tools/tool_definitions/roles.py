from api.roles import fetch_all_roles, fetch_role, update_role, create_role

roles_functions = {
    "get_roles": {
        "description": "Returns detailed information about the roles in the database.",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "fetcher": fetch_all_roles,
    },
    "get_role": {
        "description": "Returns detailed information about a specific role.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "Role ID"},
            },
            "required": ["id"],
        },
        "fetcher": fetch_role,
    },
    "update_role": {
        "description": "Updates a specific role.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "Role ID"},
                "name": {
                    "type": "object",
                    "description": '{"en": "Name of the role", "he": "שם של התפקיד", "ar": "اسم الدور"}',
                    "properties": {
                        "en": {"type": "string", "description": "Name in English"},
                        "he": {"type": "string", "description": "Name in Hebrew"},
                        "ar": {"type": "string", "description": "Name in Arabic"},
                    },
                    "required": ["en", "he", "ar"],
                },
            },
            "required": ["id", "name"],
        },
        "fetcher": update_role,
    },
    "create_role": {
        "description": "Creates a new role.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "object",
                    "description": '{"en": "Name of the role", "he": "שם של התפקיד", "ar": "اسم الدور"}',
                    "properties": {
                        "en": {"type": "string", "description": "Name in English"},
                        "he": {"type": "string", "description": "Name in Hebrew"},
                        "ar": {"type": "string", "description": "Name in Arabic"},
                    },
                    "required": ["en", "he", "ar"],
                },
            },
            "required": [
                "name",
            ],
        },
        "fetcher": create_role,
    },
}
