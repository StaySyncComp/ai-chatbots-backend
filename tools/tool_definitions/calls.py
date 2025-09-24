from api.calls import fetch_calls, create_call

calls_functions = {
    "get_calls": {
        "description": "Returns detailed information about the calls in the database.",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "fetcher": fetch_calls,
    },
    "create_call": {
        "description": "Creates a new call. Fetch call_category_id to identify call category. and if the user didnt provide departmentId take it from the call_category.",
        "parameters": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "Description of the call",
                },
                "locationId": {"type": "integer", "description": "Location ID"},
                "callCategoryId": {
                    "type": "integer",
                    "description": "Call Category ID",
                },
            },
            "required": [
                "description",
                "locationId",
                "callCategoryId",
            ],
        },
        "fetcher": create_call,
    },
}
