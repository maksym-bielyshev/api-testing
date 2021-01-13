import pytest

from client import Rest


class TestServer:
    def test_run_server(self, run_stop_server_function):
        client = Rest()
        status_code, json = client.get()
        assert status_code == 200

    def test_post_valid_border_alias_number_range(self,
                                                  run_stop_server_function):
        client = Rest()
        queues = [0, 1, 9999, 10000]
        for queue in queues:
            response = client.post("test_message", queue)
            assert response == 201

    @pytest.mark.parametrize("test_input", [-1, -2, -3, 10001, 10002, 10003])
    def test_post_invalid_alias_number_range(self,
                                             run_stop_server_function,
                                             test_input):
        client = Rest()
        response = client.post("test_message", test_input)
        assert response == 400

    def test_post_without_alias(self, run_stop_server_function):
        client = Rest()
        response = client.post("test_message")
        assert response == 201

    def test_post_default_alias_value_zero(self, run_stop_server_function):
        client = Rest()
        client.post("test_message")
        status_code, message = client.get(0)
        assert status_code == 200 and message == "test_message"

    def test_post_hundred_queues(self, run_stop_server_function):
        client = Rest()
        for q in range(100):
            response = client.post("test_message", q)
            assert response == 201

    def test_post_hundred_one_queues(self, run_stop_server_function):
        client = Rest()
        for q in range(100):
            client.post("test_message", q)
        response = client.post("test_message", 100)
        assert response == 400

    def test_post_hundred_messages(self, run_stop_server_function):
        client = Rest()
        for q in range(100):
            response = client.post("test_message" + str(q))
            assert response == 201

    def test_post_hundred_one_messages(self, run_stop_server_function):
        client = Rest()
        for q in range(101):
            client.post("test_message" + str(q))
        status_code, message = client.get(100)
        assert message == "no messages"

    def test_post_empty_message(self, run_stop_server_function):
        client = Rest()
        response = client.post("")
        assert response == 400

    def test_post_without_message(self, run_stop_server_function):
        client = Rest()
        response = client.post()
        assert response == 400
