import pytest


class Test01LoginUseCase:
    @pytest.mark.anyio
    async def test_with_valid_data(self, async_client, mocker) -> None:
        url = "/v1/auth/login"
        form_data = {"username": "username", "password": "password"}

        mocker.patch(
            "src.application.use_cases.auth.login.LoginUseCase._LoginUseCase__get_account",
            return_value={"username": "username"}
        )

        response = await async_client.post(url, json=form_data)
        decoded_response: dict = response.json()

        assert "access_token" in decoded_response.keys()
        assert "access_token" in response.cookies.keys()
