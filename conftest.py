import logging
import subprocess
import pytest

log = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def run_stop_server_function():
    log.info("Run server")
    process = subprocess.Popen("python server.py")
    yield

    log.info("Kill server")
    process.kill()
