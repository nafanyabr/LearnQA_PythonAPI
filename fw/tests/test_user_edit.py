from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):

        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
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

        # Edit
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # Get
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            'firstName',
            new_name,
            'Wrong name of user after edit'
        )

    def test_edit_user_no_auth(self):

        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # Edit
        new_name = "Anonymous"

        response2 = MyRequests.put(
            f'/user/{user_id}',
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == f"Auth token not supplied",\
            f"Unexpected response content: {response2.content}"

    def test_edit_another_user(self):

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

        # Edit user1 info by user2
        new_name = "Nemo"

        response4 = MyRequests.put(
            f'/user/{user1_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(response4, 200)

        # Check user1 info
        response5 = MyRequests.get(
            f"/user/{user1_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response5, 200)

        Assertions.assert_json_value_by_name(
            response5,
            'username',
            user1_username,
            'Username was changed by another user!'
        )


    def test_edit_user_wrong_email(self):
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

        # Edit
        new_email = "wrong.email.mail.ru"

        response3 = MyRequests.put(
            f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'email': new_email}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == "Invalid email format",\
            f"Unexpected response content: {response3.content}"


    def test_edit_user_short_username(self):

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

        # Edit
        new_name = "X"

        response3 = MyRequests.put(
            f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == \
            '{"error":"Too short value for field firstName"}',\
            f"Unexpected response content: {response3.content}"