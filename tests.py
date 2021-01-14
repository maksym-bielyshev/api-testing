import pytest

from client import Rest

VALID_QUEUE_BORDER_VALUES = [0, 1, 9999, 10000]
INVALID_QUEUE_BORDER_VALUES = [-1, 10001]
MAX_QUEUES = MAX_MESSAGES = 100
TEST_MESSAGE = "test_message"
NO_MESSAGES = "no messages"


class TestServer:
    def test_run_server(self, run_stop_server_function):
        client = Rest()
        status_code, json = client.get()
        assert status_code == 200

    @pytest.mark.parametrize("valid_queue_border", VALID_QUEUE_BORDER_VALUES)
    def test_valid_border_alias_number_range_post(self,
                                                  run_stop_server_function,
                                                  valid_queue_border):
        client = Rest()
        response = client.post(TEST_MESSAGE, valid_queue_border)
        assert response == 201

    @pytest.mark.parametrize("invalid_input", INVALID_QUEUE_BORDER_VALUES)
    def test_invalid_alias_number_range_post(self,
                                             run_stop_server_function,
                                             invalid_input):
        client = Rest()
        response = client.post(TEST_MESSAGE, invalid_input)
        assert response == 400

    def test_without_alias_post(self, run_stop_server_function):
        client = Rest()
        response = client.post(TEST_MESSAGE)
        assert response == 201

    def test_default_alias_value_zero_post(self, run_stop_server_function):
        client = Rest()
        client.post(TEST_MESSAGE)
        _, message = client.get(0)
        assert message == TEST_MESSAGE

    def test_hundred_queues_post(self, run_stop_server_function):
        client = Rest()
        for q in range(MAX_QUEUES):
            response = client.post(TEST_MESSAGE, q)
            assert response == 201

    def test_hundred_one_queues_post(self, run_stop_server_function):
        INVALID_QUEUES_VALUE = 101
        client = Rest()
        for q in range(MAX_QUEUES):
            client.post(TEST_MESSAGE, q)
        client.post(TEST_MESSAGE, INVALID_QUEUES_VALUE)
        _, message = client.get(INVALID_QUEUES_VALUE)
        assert message == NO_MESSAGES

    def test_hundred_messages_post(self, run_stop_server_function):
        client = Rest()
        for q in range(MAX_MESSAGES):
            response = client.post(TEST_MESSAGE + str(q))
            assert response == 201

    def test_hundred_one_messages_post(self, run_stop_server_function):
        client = Rest()
        for q in range(MAX_MESSAGES + 1):
            client.post(TEST_MESSAGE)
        _, message = client.get()
        assert message == NO_MESSAGES

    def test_empty_message_post(self, run_stop_server_function):
        client = Rest()
        response = client.post("")
        assert response == 400

    def test_post_without_message(self, run_stop_server_function):
        client = Rest()
        response = client.post()
        assert response == 400

    def test_duplicate_messages(self, run_stop_server_function):
        client = Rest()
        for m in range(MAX_MESSAGES):
            client.post(TEST_MESSAGE + str(m))
            _, message = client.get()
            assert message == TEST_MESSAGE + str(m)

    def test_duplicate_queues(self, run_stop_server_function):
        client = Rest()
        for q in range(MAX_QUEUES):
            client.post(TEST_MESSAGE, q)
            _, message = client.get(q)
            assert message == TEST_MESSAGE

    @pytest.mark.parametrize("valid_queue_border", VALID_QUEUE_BORDER_VALUES)
    def test_valid_queue_alias_number_get(self, run_stop_server_function,
                                          valid_queue_border):
        client = Rest()
        client.post(TEST_MESSAGE, valid_queue_border)
        _, message = client.get(valid_queue_border)
        assert message == TEST_MESSAGE

    @pytest.mark.parametrize("invalid_queue_border",
                             INVALID_QUEUE_BORDER_VALUES)
    def test_invalid_queue_alias_number_get(self, run_stop_server_function,
                                            invalid_queue_border):
        client = Rest()
        client.post(TEST_MESSAGE, invalid_queue_border)
        _, message = client.get(invalid_queue_border)
        assert message == NO_MESSAGES

    def test_message_returning(self, run_stop_server_function):
        client = Rest()
        client.post(TEST_MESSAGE)
        _, message = client.get()
        assert message == TEST_MESSAGE

    def test_message_delete_after_returning(self, run_stop_server_function):
        client = Rest()
        client.post(TEST_MESSAGE)
        client.get()
        _, message = client.get()
        assert message == NO_MESSAGES

    def test_ignore_request_without_messages_in_queue(self,
                                                      run_stop_server_function
                                                      ):
        client = Rest()
        _, message = client.get()
        assert message == NO_MESSAGES
