from google.genai import types
from tools.tool_definitions.users import users_functions
from tools.tool_definitions.organizations import organization_functions
from tools.tool_definitions.departments import departments_functions
from tools.tool_definitions.call_categories import call_categories_functions
from tools.tool_definitions.locations import locations_functions
from tools.tool_definitions.roles import roles_functions
from tools.tool_definitions.permissions import permissions_functions
from tools.tool_definitions.areas import areas_functions
from tools.tool_definitions.calls import calls_functions
from tools.tool_definitions.guest import guest_functions

function_definitions = {
    **users_functions,
    **organization_functions,
    **departments_functions,
    **call_categories_functions,
    **locations_functions,
    **roles_functions,
    **permissions_functions,
    **areas_functions,
    **calls_functions,
}


guest_definitions = {**guest_functions}

house_tools = [
    types.Tool(
        function_declarations=[
            {
                "name": name,
                "description": data["description"],
                "parameters": data["parameters"],
            }
            for name, data in function_definitions.items()
        ]
    )
]

guest_tools = [
    types.Tool(
        function_declarations=[
            {
                "name": name,
                "description": data["description"],
                "parameters": data["parameters"],
            }
            for name, data in guest_definitions.items()
        ]
    )
]
