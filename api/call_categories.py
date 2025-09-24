from tools.utils import send_request
import api.requestsApi as requestsApi


def fetch_call_categories():
    id = requestsApi.request_context.payload.organizationId
    """Fetch call categories by organization ID."""
    print(f"Fetching call categories with an id of: {id}")
    response = send_request(
        "get",
        f"calls/categories/list?organizationId={id}",
    )
    if response.status_code == 200:
        data = response.json()
        return {"call categories data": data, "count": len(data)}
    else:
        print(
            f"Error fetching call categories: {response.status_code}, {response.text}"
        )
        return {
            "error": f"Failed to fetch call categories {response.text} {response.status_code}"
        }


def create_call_category(name, department_id, expectedTime):
    """Create a new call category."""
    print(f"creating call categories with an name of: {name}")
    organization_id = requestsApi.request_context.payload.organizationId
    response = send_request(
        "post",
        f"calls/categories",
        {
            "organizationId": organization_id,
            "name": name,
            "departmentId": department_id,
            "expectedTime": expectedTime,
        },
    )
    if response.status_code == 200:
        return {"call categories data": response.json()}
    else:
        print(
            f"Error fetching call categories: {response.status_code}, {response.text}"
        )
        return {
            "error": f"Failed to fetch call categories {response.text} {response.status_code}"
        }


def update_call_category(call_category_id, name, department_id, expectedTime):
    """Update an existing call category."""
    print(f"creating call categories with an name of: {name}")
    organization_id = requestsApi.request_context.payload.organizationId

    response = send_request(
        "put",
        f"calls/categories/{call_category_id}",
        {
            "organizationId": organization_id,
            "name": name,
            "departmentId": department_id,
            "expectedTime": expectedTime,
        },
    )
    if response.status_code == 200:
        return {"call categories data": response.json()}
    else:
        print(
            f"Error fetching call categories: {response.status_code}, {response.text}"
        )
        return {
            "error": f"Failed to fetch call categories {response.text} {response.status_code}"
        }


def upsert_call_categories(call_categories):
    print("Upserting call categories")
    response = send_request("post", "calls/categories/upsert", call_categories)
    if response.status_code == 200:
        return {"call categories data": response.json()}
    else:
        print(
            f"Error fetching call categories: {response.status_code}, {response.text}"
        )
        return {
            "error": f"Failed to fetch call categories: {response.text} {response.status_code}"
        }
