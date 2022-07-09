import hashlib
import pytest

from source.settings import settings
from source.utils import generate_short_url_based_on_hash, generate_random_hash


@pytest.mark.parametrize('target_str', ['test123', '!@#4test', 'google.com'])
def test_generate_random_hash(target_str: str):
    expected_value = hashlib.sha512(target_str.encode()).hexdigest()
    actual_result = generate_random_hash(target_str=target_str)

    assert expected_value[:settings.FILE_PATH_LENGTH] == actual_result


@pytest.mark.parametrize('given_hash', ['abc1', '==tuk'])
def test_generate_short_url_based_on_hash(given_hash: str):
    expected_result = f'{settings.HOST}{given_hash}'
    actual_result = generate_short_url_based_on_hash(given_hash=given_hash)

    assert expected_result == actual_result
