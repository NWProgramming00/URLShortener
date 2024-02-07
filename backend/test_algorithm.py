import pytest
from algorithm import HashingAlgorithm


@pytest.fixture
def hashing_algorithm():
    return HashingAlgorithm(salt="test_salt")


def test_encode_and_decode(hashing_algorithm):
    input_number = 123
    encoded_text = hashing_algorithm.encode(input_number)
    decoded_number = hashing_algorithm.decode(encoded_text)
    assert decoded_number == input_number


def test_encode(hashing_algorithm):
    input_number = 123
    expected_result = "dAK8sp"
    encoded_text = hashing_algorithm.encode(input_number)
    assert encoded_text == expected_result


def test_decode(hashing_algorithm):
    input_code = "dAK8sp"
    expected_result = 123
    decoded_number = hashing_algorithm.decode(input_code)
    assert decoded_number == expected_result


def test_encode_with_invalid_input(hashing_algorithm):
    with pytest.raises(TypeError, match="Input must be an integer."):
        hashing_algorithm.encode("invalid_input")


def test_decode_with_invalid_input(hashing_algorithm):
    with pytest.raises(TypeError, match="Input must be a string."):
        hashing_algorithm.decode(123)


def test_reorder_alphabet():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    salt = "test_salt"
    reordered_alphabet = HashingAlgorithm._HashingAlgorithm__reorder_alphabet(alphabet, salt)
    assert isinstance(reordered_alphabet, str)
    assert set(reordered_alphabet) == set(alphabet)
    assert reordered_alphabet != alphabet


def test_reorder_alphabet_with_empty_salt():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    salt = ""
    reordered_alphabet = HashingAlgorithm._HashingAlgorithm__reorder_alphabet(alphabet, salt)
    assert reordered_alphabet == alphabet