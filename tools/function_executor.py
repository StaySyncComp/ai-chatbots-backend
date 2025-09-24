import asyncio
from .tool_definitions.tool_definitions import function_definitions, guest_functions
from google.genai import types


async def execute_function_call(function_call: types.FunctionCall, isGuest=False):
    fn_name = function_call.name
    parameters = function_call.args or {}
    if isGuest:
        fetcher = guest_functions.get(fn_name, {}).get("fetcher")
    else:
        fetcher = function_definitions.get(fn_name, {}).get("fetcher")

    if not fetcher:
        return types.Part.from_function_response(
            name=fn_name,
            response={"error": f"No fetcher defined for function '{fn_name}'"},
        )

    try:
        if asyncio.iscoroutinefunction(fetcher):
            data = await fetcher(**parameters)
        else:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: fetcher(**parameters))

        # Legacy
        return types.Part.from_function_response(
            name=fn_name,
            response={"result": data},
        )
        # New
        # return types.FunctionResponse(
        #     name=function_call.name,
        #     response={"result": data},
        #     id=function_call.id,
        # )

    except Exception as e:
        return types.Part.from_function_response(
            name=fn_name,
            response={"error": str(e)},
        )


async def process_function_calls(function_calls: list[types.FunctionCall], isGuest):
    tasks = [execute_function_call(fn, isGuest) for fn in function_calls]
    return await asyncio.gather(*tasks)
