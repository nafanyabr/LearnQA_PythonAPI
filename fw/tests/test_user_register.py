import allure
import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("User registration cases")
class TestUserRegister(BaseCase):
    exclude_params = [("password"),("username"),("firstName"),("lastName"),("email")]

    @allure.feature("Register user")
    @allure.story("Successfull registration")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    @allure.story("Unsuccessfull registration - existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",\
            f"Unexpected response content: {response.content}"


    @allure.story("Unsuccessfull registration - invalid email")
    def test_create_user_with_broken_email(self):
        email = 'user.ya.ru'
        data = self.prepare_registration_data(email)

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format",\
            f"Unexpected response content: {response.content}"

    @allure.story("Unsuccessfull registration - absent param")
    @allure.title("Проверка создания юзера без поля [{exclude_param}]")
    @pytest.mark.parametrize('exclude_param', exclude_params)
    def test_create_user_without_parameter(self, exclude_param):
        data = self.prepare_registration_data()
        del data[exclude_param]

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == \
            f"The following required params are missed: {exclude_param}",\
            f"Unexpected response content: {response.content}"

    @allure.story("Unsuccessfull registration - very short username")
    def test_create_user_with_short_username(self):
        username = 'a'
        data = self.prepare_registration_data(username=username)

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short",\
            f"Unexpected response content: {response.content}"

    @allure.story("Unsuccessfull registration - very long username")
    def test_create_user_with_long_username(self):
        username = 'x' * 260
        data = self.prepare_registration_data(username=username)

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long",\
            f"Unexpected response content: {response.content}"