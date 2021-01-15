import pytest

from client import Rest

VALID_QUEUE_BORDER_VALUES = [0, 1, 9999, 10000]
INVALID_QUEUE_BORDER_VALUES = [-1, 10001]
MAX_QUEUES = 100
MAX_MESSAGES = 100
TEST_MESSAGE = "test_message"
NO_MESSAGES = "no messages"


class TestServer:
    def test_run_server(self, run_stop_server_function):
        client = Rest()
        status_code, json = client.get()
        assert status_code == 200


class TestGet:
    def test_message_returning_get(self, run_stop_server_function):
        client = Rest()
        client.post(TEST_MESSAGE)
        _, message = client.get()
        assert message == TEST_MESSAGE

    def test_message_delete_after_returning_get(self,
                                                run_stop_server_function):
        client = Rest()
        client.post(TEST_MESSAGE)
        client.get()
        _, message = client.get()
        assert message == NO_MESSAGES

    def test_ignore_request_without_messages_in_queue_get(
            self, run_stop_server_function):
        client = Rest()
        _, message = client.get()
        assert message == NO_MESSAGES

    def test_get_dont_delete_messages(self, run_stop_server_function):
        client = Rest()

        for m in range(MAX_MESSAGES):
            client.post(TEST_MESSAGE)
        client.get()

        for m in range(MAX_MESSAGES - 1):
            _, message = client.get()
            assert message == TEST_MESSAGE


class TestPost:
    @pytest.mark.parametrize("invalid_queue_border",
                             INVALID_QUEUE_BORDER_VALUES)
    def test_invalid_queue_alias_number_post(self, run_stop_server_function,
                                             invalid_queue_border):
        client = Rest()
        _, message = client.post(TEST_MESSAGE, invalid_queue_border)
        assert message == 'Queue must be <= 10000'

    def test_without_alias_post(self, run_stop_server_function):
        client = Rest()
        status_code, _ = client.post(TEST_MESSAGE)
        assert status_code == 201

    def test_default_alias_value_zero_post(self, run_stop_server_function):
        client = Rest()
        client.post(TEST_MESSAGE)
        _, message = client.get(0)
        assert message == TEST_MESSAGE

    def test_valid_limit_queues_post(self, run_stop_server_function):
        client = Rest()
        for q in range(MAX_QUEUES):
            status_code, _ = client.post(TEST_MESSAGE, q)
            assert status_code == 201

    def test_invalid_limit_queues_post(self, run_stop_server_function):
        client = Rest()
        for q in range(MAX_QUEUES):
            client.post(TEST_MESSAGE, q)
        client.post(TEST_MESSAGE, MAX_QUEUES + 1)
        _, message = client.get(MAX_QUEUES + 1)
        assert message == NO_MESSAGES

    def test_valid_limit_messages_post(self, run_stop_server_function):
        client = Rest()
        for q in range(MAX_MESSAGES):
            status_code, _ = client.post(f"{TEST_MESSAGE}{q}")
            assert status_code == 201

    def test_invalid_limit_messages_post(self, run_stop_server_function):
        client = Rest()
        for q in range(MAX_MESSAGES):
            _, message = client.post(TEST_MESSAGE)
        for m in range(MAX_MESSAGES):
            _, message = client.get()
            assert message == TEST_MESSAGE
        _, message = client.get()
        assert message == NO_MESSAGES

    def test_empty_message_post(self, run_stop_server_function):
        client = Rest()
        status_code, message = client.post("")
        assert message == 'Message is empty'

    def test_without_message_post(self, run_stop_server_function):
        client = Rest()
        status_code, _ = client.post()
        assert status_code == 400

    def test_duplicate_messages_post(self, run_stop_server_function):
        client = Rest()
        for m in range(MAX_MESSAGES):
            client.post(f"{TEST_MESSAGE}{m}")
            _, message = client.get()
            assert message == f"{TEST_MESSAGE}{m}"

    def test_duplicate_queues_post(self, run_stop_server_function):
        client = Rest()
        for q in range(MAX_QUEUES):
            client.post(TEST_MESSAGE, q)
            _, message = client.get(q)
            assert message == TEST_MESSAGE


class TestPostGet:
    @pytest.mark.parametrize("valid_queue_border", VALID_QUEUE_BORDER_VALUES)
    def test_valid_queue_alias_number_get(self, run_stop_server_function,
                                          valid_queue_border):
        client = Rest()
        status_code, _ = client.post(TEST_MESSAGE, valid_queue_border)
        assert status_code == 201
        _, message = client.get(valid_queue_border)
        assert message == TEST_MESSAGE


class TestDelete:
    def test_message_without_queue_delete(self, run_stop_server_function):
        client = Rest()
        client.post(TEST_MESSAGE)
        client.delete()
        _, message = client.get()
        assert message == NO_MESSAGES

    def test_message_with_queue_delete(self, run_stop_server_function):
        client = Rest()
        client.post(TEST_MESSAGE, 0)
        client.delete(0)
        _, message = client.get(0)
        assert message == NO_MESSAGES

    def test_default_alias_zero_delete(self, run_stop_server_function):
        client = Rest()
        client.post(TEST_MESSAGE, 0)
        client.post(TEST_MESSAGE, 1)
        client.delete()
        _, message = client.get()
        assert message == NO_MESSAGES

        _, message = client.get(1)
        assert message == TEST_MESSAGE

    def test_oldest_message_delete(self, run_stop_server_function):
        client = Rest()
        client.post("oldest message")
        client.post("newest message")
        client.delete()
        _, message = client.get()
        assert message == "newest message"

    def test_no_message_in_queue_delete(self, run_stop_server_function):
        client = Rest()
        _, message = client.delete()
        assert message == 'Not Found'
