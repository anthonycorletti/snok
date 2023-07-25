from uuid import uuid4

from httpx import AsyncClient
from {{ __template_name }}.const import API_V0


async def test_create_{{ __template_plural_namespace }}(client: AsyncClient) -> None:
    data = {"name": "John Doe", "age": 30}
    response = await client.post(f"{API_V0}/{{ __template_plural_namespace }}", json=data)
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "John Doe"
    assert response.json()["age"] == 30
    assert response.json()["id"]


async def test_get_{{ __template_plural_namespace }}(client: AsyncClient) -> None:
    data = {"name": "John Doe", "age": 30}
    response = await client.post(f"{API_V0}/{{ __template_plural_namespace }}", json=data)
    assert response.status_code == 200, response.text
    _id = response.json()["id"]
    response = await client.get(f"{API_V0}/{{ __template_plural_namespace }}/{_id}")
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "John Doe"
    assert response.json()["age"] == 30
    assert response.json()["id"]


async def test_update_{{ __template_plural_namespace }}(client: AsyncClient) -> None:
    data = {"name": "John Doe", "age": 30}
    response = await client.post(f"{API_V0}/{{ __template_plural_namespace }}", json=data)
    assert response.status_code == 200, response.text
    _id = response.json()["id"]
    data = {"name": "Jane Doe", "age": 40}
    response = await client.put(f"{API_V0}/{{ __template_plural_namespace }}/{_id}", json=data)
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Jane Doe"
    assert response.json()["age"] == 40
    assert response.json()["id"]


async def test_delete_{{ __template_plural_namespace }}(client: AsyncClient) -> None:
    data = {"name": "John Doe", "age": 30}
    response = await client.post(f"{API_V0}/{{ __template_plural_namespace }}", json=data)
    assert response.status_code == 200, response.text
    _id = response.json()["id"]
    response = await client.delete(f"{API_V0}/{{ __template_plural_namespace }}/{_id}")
    assert response.status_code == 204
    response = await client.get(
        f"{API_V0}/{{ __template_plural_namespace }}/{_id}", headers={"accept": "application/json"}
    )
    assert response.status_code == 404


async def test_list_{{ __template_plural_namespace }}(client: AsyncClient) -> None:
    data = {"name": "John Doe", "age": 30}
    response = await client.post(f"{API_V0}/{{ __template_plural_namespace }}", json=data)
    assert response.status_code == 200, response.text
    data = {"name": "Jane Doe", "age": 40}
    response = await client.post(f"{API_V0}/{{ __template_plural_namespace }}", json=data)
    assert response.status_code == 200, response.text
    response = await client.get(f"{API_V0}/{{ __template_plural_namespace }}")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 2
    assert response.json()[1]["name"] == "John Doe"
    assert response.json()[1]["age"] == 30
    assert response.json()[0]["name"] == "Jane Doe"
    assert response.json()[0]["age"] == 40
    assert response.json()[0]["id"]
    assert response.json()[1]["id"]


async def test_get_{{ __template_plural_namespace }}_not_found(client: AsyncClient) -> None:
    response = await client.get(f"{API_V0}/{{ __template_plural_namespace }}/{uuid4()}")
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Not found"


async def test_update_{{ __template_plural_namespace }}_not_found(client: AsyncClient) -> None:
    data = {"name": "Jane Doe", "age": 40}
    response = await client.put(f"{API_V0}/{{ __template_plural_namespace }}/{uuid4()}", json=data)
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Not found"


async def test_delete_{{ __template_plural_namespace }}_not_found(client: AsyncClient) -> None:
    response = await client.delete(f"{API_V0}/{{ __template_plural_namespace }}/{uuid4()}")
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Not found"
