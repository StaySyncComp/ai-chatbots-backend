from api.call_categories import (
    fetch_call_categories,
    create_call_category,
    update_call_category,
    upsert_call_categories,
)

call_categories_functions = {
    "get_call_categories": {
        "description": "Returns detailed information about the call categories in the database.",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "fetcher": fetch_call_categories,
    },
    "create_call_category": {
        "description": "Creates a new call category.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "object",
                    "description": 'en": "Name of the call category", "he": "שם של ההגדרת פנייה", "ar": "اسم فئة المكالمة',
                    "properties": {
                        "en": {"type": "string", "description": "Name in English"},
                        "he": {"type": "string", "description": "Name in Hebrew"},
                        "ar": {"type": "string", "description": "Name in Arabic"},
                    },
                    "required": ["en", "he", "ar"],
                },
                "department_id": {
                    "type": "integer",
                    "description": "Department ID",
                },
                "expectedTime": {
                    "type": "integer",
                    "description": "Expected time in minutes",
                },
            },
            "required": ["name", "department_id", "expectedTime"],
        },
        "fetcher": create_call_category,
    },
    "update_call_category": {
        "description": "Updates an existing call category.",
        "parameters": {
            "type": "object",
            "properties": {
                "call_category_id": {
                    "type": "integer",
                    "description": "Call Category ID",
                },
                "name": {
                    "type": "object",
                    "description": 'en": "Name of the call category", "he": "שם של ההגדרת פנייה", "ar": "اسم فئة المكالمة',
                    "properties": {
                        "en": {"type": "string", "description": "Name in English"},
                        "he": {"type": "string", "description": "Name in Hebrew"},
                        "ar": {"type": "string", "description": "Name in Arabic"},
                    },
                    "required": ["en", "he", "ar"],
                },
                "department_id": {
                    "type": "integer",
                    "description": "Department ID",
                },
                "expectedTime": {
                    "type": "integer",
                    "description": "Expected time in minutes",
                },
            },
            "required": [
                "call_category_id",
                "name",
                "department_id",
                "expectedTime",
            ],
        },
        "fetcher": update_call_category,
    },
    "upsert_call_categories": {
        "description": "Updates or creates call categories in bulk. use this when a user wants to update or create multiple call categories at once.",
        "parameters": {
            "type": "object",
            "properties": {
                "call_categories": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "object",
                                "description": 'en": "Name of the call category", "he": "שם של ההגדרת פנייה", "ar": "اسم فئة المكالمة',
                                "properties": {
                                    "en": {
                                        "type": "string",
                                        "description": "Name in English",
                                    },
                                    "he": {
                                        "type": "string",
                                        "description": "Name in Hebrew",
                                    },
                                    "ar": {
                                        "type": "string",
                                        "description": "Name in Arabic",
                                    },
                                },
                                "required": ["en", "he", "ar"],
                            },
                            "organization_id": {
                                "type": "integer",
                                "description": "Organization ID",
                            },
                            "department_id": {
                                "type": "integer",
                                "description": "Department ID",
                            },
                            "expectedTime": {
                                "type": "integer",
                                "description": "Expected time in minutes",
                            },
                        },
                        "required": [
                            "name",
                            "organization_id",
                            "department_id",
                            "expectedTime",
                        ],
                    },
                }
            },
        },
        "fetcher": upsert_call_categories,
    },
}
