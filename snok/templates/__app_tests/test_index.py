from httpx import AsyncClient


async def test_index(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    response_content = response.content.decode("utf-8")
    assert "Hello, Snok!" in response_content
