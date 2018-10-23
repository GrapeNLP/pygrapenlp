import os

import pytest

from pygrapenlp.compressed_delaf import CompressedDelaf


@pytest.fixture
def compressed_delaf():
    base_dir = os.path.dirname(__file__)
    bin_delaf_pathname = os.path.join(base_dir, '..', 'data', 'test_delaf.bin')
    inf_delaf_pathname = os.path.join(base_dir, '..', 'data', 'test_delaf.inf')
    compressed_delaf = CompressedDelaf(bin_delaf_pathname, inf_delaf_pathname)
    yield compressed_delaf


get_word_properties_test_cases = [
    ('test', 'A')
]


@pytest.mark.parametrize('word, expected', get_word_properties_test_cases)
def test_get_word_semantic_traits(word, expected, compressed_delaf):
    actual = compressed_delaf.get_ambiguous_word_properties(word)
    properties = actual
    for i in range(properties.size()):
        property = properties[i]
        st = property.semantic_traits


get_set_of_ambiguous_word_serialized_semantic_properties_use_cases = [
    ('', set()),
    ('a', {'stopword'}),
    ('test', set())
]


@pytest.mark.parametrize('word, expected', get_set_of_ambiguous_word_serialized_semantic_properties_use_cases)
def test_get_set_of_ambiguous_word_serialized_semantic_properties(word, expected, compressed_delaf):
    actual = compressed_delaf.get_set_of_ambiguous_word_serialized_semantic_properties(word)
    assert expected == actual
