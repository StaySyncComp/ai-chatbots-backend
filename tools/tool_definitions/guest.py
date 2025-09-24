from api.guest import (
    fetch_call_guest_categories,
    fetch_guest_information,
    create_guest_call,
    fetch_organization_guest,
)

guest_functions = {
    # "get_guest_calls": {
    #     "description": "Returns detailed information about the guest calls in the database.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {},
    #     },
    #     "fetcher": fetch_guest_calls,
    # },
    "get_call_categories": {
        "description": "Returns detailed information about the call categories in the database.",
        "parameters": {
            "type": "object",
            "properties": {},
        },
        "fetcher": fetch_call_guest_categories,
    },
    "get_guest_information": {
        "description": "Returns detailed information about the guest in the database.",
        "parameters": {
            "type": "object",
            "properties": {},
        },
        "fetcher": fetch_guest_information,
    },
    "get_hotel_information": {
        "description": "Returns detailed information about the hotel in the database.",
        "parameters": {
            "type": "object",
            "properties": {},
        },
        "fetcher": fetch_organization_guest,
    },
    "create_call": {
        "description": "Creates a new call. Fetch get_call_categories to identify call category.",
        "parameters": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "Description of the call",
                },
                "callCategoryId": {
                    "type": "integer",
                    "description": "Call Category ID",
                },
            },
            "required": [
                "description",
                "callCategoryId",
            ],
        },
        "fetcher": create_guest_call,
    },
}
