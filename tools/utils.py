import api.requestsApi as requestsApi
import requests
import os
from fastapi import Request


async def save_request_context(request: Request, payload=None):
    headers = dict(request.headers)
    print("headers", headers)
    headers_to_remove = [
        "host",
        "content-length",
        "connection",
        "sec-websocket-key",
        "sec-websocket-version",
        "sec-websocket-extensions",
        "sec-websocket-protocol",
        "upgrade",
    ]
    for header in headers_to_remove:
        if header.lower() in headers:
            del headers[header.lower()]
    cookies = request.cookies
    query_params = dict(request.query_params)
    requestsApi.request_context.headers = headers
    requestsApi.request_context.cookies = cookies
    requestsApi.request_context.query_params = query_params
    requestsApi.request_context.payload = payload
    # get json body
    body = await request.json()
    requestsApi.request_context.body = body


async def save_websocket_context(websocket):
    # Get headers but filter out problematic ones immediately
    headers = dict(websocket.headers)

    # Headers that should be excluded when forwarding requests
    headers_to_remove = [
        "content-length",  # Will be calculated automatically
        "sec-websocket-key",  # WebSocket specific headers
        "sec-websocket-version",
        "sec-websocket-extensions",
        "sec-websocket-protocol",
        "upgrade",  # WebSocket upgrade header
    ]

    # Remove problematic headers right when saving to context
    for header in headers_to_remove:
        if header.lower() in headers:
            del headers[header.lower()]

    # Get cookies and convert to dict for consistency
    cookies = dict(websocket.cookies)

    # Extract query parameters from URL
    query_params = {}
    if "?" in websocket.url.path:
        query_string = websocket.url.path.split("?")[1]
        for param in query_string.split("&"):
            if "=" in param:
                key, value = param.split("=", 1)
                query_params[key] = value

    # Store clean data in context
    requestsApi.request_context.headers = headers
    requestsApi.request_context.cookies = cookies
    requestsApi.request_context.query_params = query_params
    requestsApi.request_context.body = (
        {}
    )  # WebSockets don't have a request body in the same way


def send_request(method, endpoint, json=None):
    """
    Send a request to the specified endpoint with the current request context.

    Args:
        method (str): HTTP method (get, post, put, delete, etc.)
        endpoint (str): API endpoint (without base URL)
        json (dict, optional): JSON body to send with the request

    Returns:
        Response object from the requests library
    """
    print("Sending request...")
    # Supabase client setup
    base_url = os.getenv("BASE_URL") or "http://localhost:3101"
    url = f"{base_url}/{endpoint}"

    # Convert method to lowercase for consistency
    method = method.lower()
    print("method", method)
    # Prepare request arguments
    request_args = {
        "headers": requestsApi.request_context.headers,
        "cookies": requestsApi.request_context.cookies,
        "params": requestsApi.request_context.query_params,
    }

    # Add JSON body if provided or use the context body
    if json is not None:
        request_args["json"] = json
    # Send the request with the appropriate method
    if method == "get":
        response = requests.get(url, cookies=request_args["cookies"])
    elif method == "post":
        response = requests.post(url, **request_args)
    elif method == "put":
        response = requests.put(url, **request_args)
    elif method == "delete":
        response = requests.delete(url, **request_args)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")
    print(response)
    return response
