import inspect
import logging
import subprocess
import pytest
import requests

from time import sleep, time
from client import Rest

log = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def run_stop_server_function(request):
    log.info("Run server")
    process = subprocess.Popen("python server.py")

    timeout = 5
    start_time = time()
    while time() - start_time < timeout:
        try:
            client = Rest()
            status_code, _ = client.get()
            assert status_code == 200
            break
        except(requests.exceptions.ConnectionError, AssertionError):
            sleep(5)
            continue
    else:
        raise Exception("Server is not started!")
    log.info(request.function)
    yield

    log.info("Kill server")
    process.kill()
