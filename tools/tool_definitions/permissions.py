from api.permissions import update_permissions

permissions_functions = {
    "update_permissions": {
        "description": "Update a specific permissions of permission by id.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "permission ID"},
                "action": {
                    "type": "string",
                    "description": "Action name like the Actions Enum (in the schema)",
                },
                "scope": {
                    "type": "string",
                    "description": "Scope name like the Scopes Enum (in the schema)",
                },
                "resource": {
                    "type": "string",
                    "description": "Resource name like the Resources Enum (in the schema)",
                },
            },
            "required": [
                "id",
                "action",
                "scope",
                "resource",
            ],
        },
        "fetcher": update_permissions,
    }
}
