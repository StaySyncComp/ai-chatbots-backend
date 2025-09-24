from google.genai import types


def part_to_dict(part: types.Part) -> dict:
    part_dict = {}
    if part.text:
        part_dict["text"] = part.text
    if part.function_call:
        part_dict["function_call"] = {
            "name": part.function_call.name,
            "args": dict(part.function_call.args),
        }
    if part.function_response:
        part_dict["function_response"] = {
            "name": part.function_response.name,
            "response": part.function_response.response,
        }
    return part_dict


def dict_to_part(data: dict) -> types.Part:
    if "text" in data:
        return types.Part(text=data["text"])
    if "function_call" in data:
        fc_data = data["function_call"]
        return types.Part(
            function_call=types.FunctionCall(name=fc_data["name"], args=fc_data["args"])
        )
    if "function_response" in data:
        fr_data = data["function_response"]
        return types.Part(
            function_response=types.FunctionResponse(
                name=fr_data["name"], response=fr_data["response"]
            )
        )
    return types.Part(text="")
