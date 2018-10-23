import pytest

from pygrapenlp import string_to_u_array, u_array_to_string

encode_string_decode_u_array_test_cases = [
    (''),
    ('a'),
    ('á'),
    ('ab'),
    ('öü'),
    ('Probando probando un, dos, tres.')
]

@pytest.mark.parametrize('string', encode_string_decode_u_array_test_cases)
def test_encode_string_decode_u_array(string):
    native_u_array = string_to_u_array(string)
    actual = u_array_to_string(native_u_array)
    assert actual == string
