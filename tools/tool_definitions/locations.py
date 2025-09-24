from api.locations import (
    fetch_locations,
    create_location,
    update_location,
    upsert_locations,
    fetch_location_guest,
)

locations_functions = {
    "get_locations": {
        "description": "Returns detailed information about the locations in the database. including rooms, wings, and buildings.",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "fetcher": fetch_locations,
    },
    "create_location": {
        "description": "Creates a new location",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "object",
                    "description": '{"en": "Name of the location", "he": "שם של המיקום", "ar": "اسم الموقع"}',
                    "properties": {
                        "en": {"type": "string", "description": "Name in English"},
                        "he": {"type": "string", "description": "Name in Hebrew"},
                        "ar": {"type": "string", "description": "Name in Arabic"},
                    },
                    "required": ["en", "he", "ar"],
                },
                "room_number": {
                    "type": "integer",
                    "description": "Room number of the location. If not provided, it will be set to null.",
                },
                "area_id": {
                    "type": "integer",
                    "description": "Area ID. If not provided, it will be set to null.",
                },
            },
            "required": ["name", "room_number", "area_id"],
        },
        "fetcher": create_location,
    },
    "update_location": {
        "description": "Updates an existing location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location_id": {
                    "type": "integer",
                    "description": "Location ID",
                },
                "name": {
                    "type": "object",
                    "description": '{"en": "Name of the location", "he": "שם של המיקום", "ar": "اسم الموقع"}',
                    "properties": {
                        "en": {"type": "string", "description": "Name in English"},
                        "he": {"type": "string", "description": "Name in Hebrew"},
                        "ar": {"type": "string", "description": "Name in Arabic"},
                    },
                    "required": ["en", "he", "ar"],
                },
                "room_number": {
                    "type": "integer",
                    "description": "Room number of the location. If not provided, it will be set to null.",
                },
            },
            "required": ["location_id", "name", "room_number"],
        },
        "fetcher": update_location,
    },
    "upsert_locations": {
        "description": "Updates or creates locations in bulk. use this when a user wants to update or create multiple locations at once.",
        "parameters": {
            "type": "object",
            "properties": {
                "locations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "object",
                                "description": '{"en": "Name of the location", "he": "שם של המיקום", "ar": "اسم الموقع"}',
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
                            "roomNumber": {
                                "type": "integer",
                                "description": "Room number of the location. If not provided, it will be set to null.",
                            },
                            "organizationId": {
                                "type": "integer",
                                "description": "Organization ID. If not provided, it will be set to null.",
                            },
                            "areaId": {
                                "type": "integer",
                                "description": "Area ID. If not provided, it will be set to null.",
                            },
                        },
                        "required": ["name", "roomNumber", "organizationId", "areaId"],
                    },
                },
            },
            "required": ["locations"],
        },
        "fetcher": upsert_locations,
    },
}

guest_functions = {
    "get_location": {
        "description": "Returns detailed information about the guest location in the database.",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "fetcher": fetch_location_guest,
    }
}
