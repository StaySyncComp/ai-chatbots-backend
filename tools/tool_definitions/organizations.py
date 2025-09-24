from api.organizations import fetch_organization, get_organization_id

organization_functions = {
    "get_current_organization_data": {
        "description": "Returns detailed information about the current organization in the database.",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "fetcher": fetch_organization,
    },
    "get_organization_id": {
        "description": "Returns the organization id",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "fetcher": get_organization_id,
    },
}
