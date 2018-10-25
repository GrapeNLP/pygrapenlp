import json
import os
from collections import OrderedDict

import pytest

from src.pygrapenlp.grammar_engine import GrammarEngine
from src.pygrapenlp.u_out_bound_trie import u_out_bound_trie_string_to_string

tag_test_cases = [
    ('', '{}'),
    ('unrecognized sentence', '{}'),
    ('this is a test sentence', '{"label": {"value": "a", "start": 8, "end": 9}}'),
    ('this is another test sentence', '{"label": {"value": "another", "start": 8, "end": 15}}')
]


@pytest.fixture
def grammar_engine():
    base_dir = os.path.dirname(__file__)
    grammar_pathname = os.path.join(base_dir, '..', 'data', 'test_grammar.fst2')
    bin_delaf_pathname = os.path.join(base_dir, '..', 'data', 'test_delaf.bin')
    grammar_engine = GrammarEngine(grammar_pathname, bin_delaf_pathname)
    yield grammar_engine


def native_results_to_python_dic(sentence, native_results):
    top_segments = OrderedDict()
    if not native_results.empty():
        top_native_result = native_results.get_elem_at(0)
        top_native_result_segments = top_native_result.ssa
        for i in range(0, top_native_result_segments.size()):
            native_segment = top_native_result_segments.get_elem_at(i)
            native_segment_label = native_segment.name
            segment_label = u_out_bound_trie_string_to_string(native_segment_label)
            segment = OrderedDict()
            segment['value'] = sentence[native_segment.begin:native_segment.end]
            segment['start'] = native_segment.begin
            segment['end'] = native_segment.end
            top_segments[segment_label] = segment
    return top_segments


@pytest.mark.parametrize('sentence, expected_json', tag_test_cases)
def test_tag(sentence, expected_json, grammar_engine):
    native_results = grammar_engine.tag(sentence)
    actual = native_results_to_python_dic(sentence, native_results)
    actual_json = json.dumps(actual)
    assert expected_json == actual_json
