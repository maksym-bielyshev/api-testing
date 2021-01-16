import json

import requests
import logging
from config import URL, PORT

log = logging.getLogger(__name__)


class Rest:  # port
    def post(self, message=None, queue=None):
        log.info(f"> Message: {message}, queue: {queue}")

        if message is None:
            param = {}
        else:
            param = {"message": message}
        if queue is not None:
            param.update({'queue': queue})

        response = requests.post(f"{URL}:{PORT}", json=param)
        log.info(f"< Response status code: {response.status_code}")

        return response.status_code, response.reason

    def get(self, queue=None):
        log.info(f"> Queue: {queue}")

        if queue is None:
            param = {}
        else:
            param = {"queue": queue}

        response = requests.get(f"{URL}:{PORT}", params=param)
        json_data = json.loads(response.text)

        log.info(f"< Response status code: {response.status_code}, "
                 f"response body: {json_data['message']}")

        return response.status_code, json_data['message']

    def put(self, queue=None):
        log.info(f"> Queue: {queue}")

        if queue is None:
            param = {}
        else:
            param = {"queue": queue}

        response = requests.put(f"{URL}:{PORT}", params=param)
        log.info(f"< Response status code: {response.status_code}")

        return response.status_code, response.reason

    def delete(self, queue=None):
        log.info(f"> Queue: {queue}")

        if queue is None:
            param = {}
        else:
            param = {"queue": queue}

        response = requests.delete(f"{URL}:{PORT}", params=param)
        log.info(f"< Response status code: {response.status_code}")

        return response.status_code, response.reason
