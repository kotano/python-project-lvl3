import pytest
from pathlib import Path


FIXTURES = Path(__file__).parent / 'fixtures'


@pytest.fixture(scope='module')
def page():
    return FIXTURES / 'page.html'


@pytest.fixture(scope='module')
def image():
    return FIXTURES / 'assets' / 'python.png'


@pytest.fixture(scope='module')
def style():
    return FIXTURES / 'assets' / 'style.css'


@pytest.fixture(scope='module')
def script():
    return FIXTURES / 'assets' / 'script.js'
