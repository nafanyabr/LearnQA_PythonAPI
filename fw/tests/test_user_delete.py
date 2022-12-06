from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserDelete(BaseCase):
    def test_delete_system_user(self):
        # LOGIN
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id")

        # DELETE
        response2 = MyRequests.delete(
            f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == \
            f"Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content: {response2.content}"

    def test_delete_just_created_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # DELETE
        response2 = MyRequests.delete(
            f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        Assertions.assert_code_status(response2, 200)

        # Get
        response3 = MyRequests.get(
            f"/user/{user_id}"
        )

        Assertions.assert_code_status(response3, 404)
        assert response3.content.decode("utf-8") == \
            f"User not found", \
            f"Unexpected response content: {response3.content}"

    def test_delete_another_user(self):
        # Register user1
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post('/user/', data=register_data1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user1_id = self.get_json_value(response1, "id")
        user1_username = register_data1["username"]

        # Register user2
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post('/user/', data=register_data2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email = register_data2['email']
        password = register_data2['password']

        # Login by user2
        login_data = {
            'email': email,
            'password': password
        }
        response3 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response3, 'auth_sid')
        token = self.get_header(response3, 'x-csrf-token')

        # DELETE
        response4 = MyRequests.delete(
            f'/user/{user1_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        Assertions.assert_code_status(response4, 200)

        # Get user1 info
        response5 = MyRequests.get(f"/user/{user1_id}")
        Assertions.assert_code_status(response5, 200)
        Assertions.assert_json_has_key(response5, "username")

        Assertions.assert_json_value_by_name(
            response5,
            'username',
            user1_username,
            'Username was deleted by another user!'
        )