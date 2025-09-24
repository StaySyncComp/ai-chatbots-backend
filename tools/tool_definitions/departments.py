from api.departments import fetch_departments, create_department, update_department

departments_functions = {
    "get_departments": {
        "description": "Returns detailed information about the departments in the database.",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "fetcher": fetch_departments,
    },
    "create_department": {
        "description": "Creates a new department inside the organization in the database.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "object",
                    "description": '{"en": "Name of the department", "he": "שם המחלקה", "ar": "اسم القسم"}',
                    "properties": {
                        "en": {"type": "string", "description": "Name in English"},
                        "he": {"type": "string", "description": "Name in Hebrew"},
                        "ar": {"type": "string", "description": "Name in Arabic"},
                    },
                    "required": ["en", "he", "ar"],
                },
            },
            "required": ["name"],
        },
        "fetcher": create_department,
    },
    # "delete_department": {
    #     "description": "Deletes a department from the database.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "department_id": {
    #                 "type": "integer",
    #                 "description": "ID of the department to delete",
    #             },
    #         },
    #         "required": ["department_id"],
    #     },
    #     "fetcher": delete_department,
    # },
    "update_department": {
        "description": "Updates information of an existing department. firstly fetch get_departments and then get the department id and the fetch ",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "object",
                    "description": '{"en": "Name of the department", "he": "שם המחלקה", "ar": "اسم القسم"}',
                    "properties": {
                        "en": {"type": "string", "description": "Name in English"},
                        "he": {"type": "string", "description": "Name in Hebrew"},
                        "ar": {"type": "string", "description": "Name in Arabic"},
                    },
                    "required": ["en", "he", "ar"],
                },
                "department_id": {
                    "type": "integer",
                    "description": "ID of the department to update",
                },
            },
            "required": ["department_id", "name"],
        },
        "fetcher": update_department,
    },
}
