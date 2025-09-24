from api.areas import fetch_areas, create_area, update_area

areas_functions = {
    "get_areas": {
        "description": "Returns detailed information about the areas aka wings in the database.",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "fetcher": fetch_areas,
    },
    "create_area": {
        "description": "Creates a new area.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "object",
                    "description": 'en": "Name of the area", "he": "שם של האזור", "ar": "اسم المنطقة',
                    "properties": {
                        "en": {"type": "string", "description": "Name in English"},
                        "he": {"type": "string", "description": "Name in Hebrew"},
                        "ar": {"type": "string", "description": "Name in Arabic"},
                    },
                    "required": ["en", "he", "ar"],
                },
                "color": {
                    "type": "string",
                    "description": 'Color of the area in hex format (e.g., "#FF5733")',
                },
            },
            "required": ["name", "color"],
        },
        "fetcher": create_area,
    },
    "update_area": {
        "description": "Updates an existing area.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "Area ID"},
                "name": {
                    "type": "object",
                    "description": 'en": "Name of the area", "he": "שם של האזור", "ar": "اسم المنطقة',
                    "properties": {
                        "en": {"type": "string", "description": "Name in English"},
                        "he": {"type": "string", "description": "Name in Hebrew"},
                        "ar": {"type": "string", "description": "Name in Arabic"},
                    },
                    "required": ["en", "he", "ar"],
                },
                "color": {
                    "type": "string",
                    "description": 'Color of the area in hex format (e.g., "#FF5733")',
                },
            },
            "required": ["id", "name", "color"],
        },
        "fetcher": update_area,
    },
}
