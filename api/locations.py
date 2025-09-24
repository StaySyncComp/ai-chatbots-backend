from tools.utils import send_request
import api.requestsApi as requestsApi


def fetch_locations():
    """Fetch locations by organization ID."""
    id = requestsApi.request_context.payload.organizationId
    print(f"Fetching locations with an id of: {id}")
    response = send_request(
        "get",
        f"locations/list?organizationId={id}",
    )
    if response.status_code == 200:
        return {"locations data": response.json()}
    else:
        print(f"Error fetching locations: {response.status_code}, {response.text}")
        return {"error": "Failed to fetch locations"}


def fetch_location_guest():
    """Fetch locations by organization ID."""
    print(f"Fetching location of guest")
    response = send_request(
        "get",
        f"locations/guest",
    )
    if response.status_code == 200:
        return {"locations data": response.json()}
    else:
        print(f"Error fetching locations: {response.status_code}, {response.text}")
        return {"error": "Failed to fetch locations"}


def create_location(name, room_number, area_id):
    """Create a new location."""
    print(f"creating locations with an name of: {name}")
    organizationId = requestsApi.request_context.payload.organizationId

    response = send_request(
        "post",
        f"locations",
        {
            "organizationId": organizationId,
            "name": name,
            "roomNumber": room_number,
            "areaId": area_id,
        },
    )
    if response.status_code == 201:
        return {"locations data": response.json()}
    else:
        print(f"Error fetching locations: {response.status_code}, {response.text}")
        return {"error": "Failed to fetch locations"}


def update_location(location_id, name, room_number):
    """Update an existing location."""
    print(f"updating locations with an name of: {name}")
    organizationId = requestsApi.request_context.payload.organizationId

    response = send_request(
        "put",
        f"locations/{location_id}",
        {
            "organizationId": organizationId,
            "name": name,
            "roomNumber": room_number,
            "id": location_id,
        },
    )
    if response.status_code == 200:
        return {"locations data": response.json()}
    else:
        print(f"Error fetching locations: {response.status_code}, {response.text}")
        return {"error": "Failed to fetch locations"}


def upsert_locations(locations):
    print("Upserting locations")
    response = send_request("post", "locations/upsert", locations)
    if response.status_code == 200:
        return {"locations data": response.json()}
    else:
        print(f"Error fetching locations: {response.status_code}, {response.text}")
        return {"error": "Failed to fetch locations"}
