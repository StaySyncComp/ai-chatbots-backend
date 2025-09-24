from dotenv import load_dotenv

load_dotenv()


class RequestContext:
    headers: dict = {}
    cookies: dict = {}
    query_params: dict = {}
    body: dict = {}
    payload: dict = {}


request_context = RequestContext()
