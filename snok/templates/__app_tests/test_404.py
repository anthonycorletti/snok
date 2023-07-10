from httpx import AsyncClient


async def test_404(client: AsyncClient) -> None:
    response = await client.get("/thispathdoesnotexist")
    assert response.status_code == 307
    assert response.headers["location"] == "/404"
    response = await client.get("/404")
    assert response.status_code == 200
