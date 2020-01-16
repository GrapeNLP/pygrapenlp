'''
Wrapper of the Grammar Engine to produce recognizer-like results: identify some of
the symbols as intent or entities.
'''

import re
import os.path
from collections import namedtuple
from operator import itemgetter

from typing import Dict, List

from .grammar_engine import GrammarEngine
from .utils.u_out_bound_trie import u_out_bound_trie_string_to_string

# Prefixes for the emitted symbols
PREFIX_INTENT = 'intent.'
PREFIX_ENTITY = 'ent.'


RESULT = namedtuple('RESULT', 'intent entities tags score')

# ---------------------------------------------------------------------------

TYPE_REGEX = re.compile(r'([\w\._]+) (?: :(\w+) )?', flags=re.X)

NATIVE_RESULT = "::grapenlp::uaui_simple_segment_array_x_weight_array const &"

def parse_native_results(sentence: str, native_results: NATIVE_RESULT,
                         max_results: int=0, add_role: bool=True,
                         skip_empty: bool=True) -> List[RESULT]:
    '''
    Parse the result object produced by pygrapenlp
      :param sentence: the sentence that have been parsed
      :param native_results: the raw object returned by grapeNLP
      :param max_results: maximum number of matches to return
      :param add_role: add the (possible) role extracted from the entity name as
        an additional field
      :param skip_empty: skip empty entities (entities with no value)
    '''

    if native_results.empty():
        return [RESULT(None, [], [], 0.0)]

    results = []
    num_results = native_results.size()
    #print(".. RESULTS", num_results)

    for n, r in enumerate(range(num_results)):
        segments = native_results.get_elem_at(r).ssa
        #print("weight =", native_results.get_elem_at(r).w)

        entities = []
        tags = []
        for i in range(0, segments.size()):

            native_segment = segments.get_elem_at(i)
            native_segment_label = native_segment.name
            segment_label = u_out_bound_trie_string_to_string(native_segment_label)
            #print(".. SEGMENT", native_segment.begin, native_segment.end, segment_label)

            # If it's an intent, note it down & continue
            if segment_label.startswith(PREFIX_INTENT):
                intent = segment_label
                continue

            elem_start = native_segment.begin
            elem_end = native_segment.end
            elem_value = sentence[elem_start:elem_end]

            # If it's not an entity, add it as a tag & continue
            if not segment_label.startswith(PREFIX_ENTITY):
                tags.append({'key': segment_label, 'value': elem_value,
                             'start_index': elem_start, 'end_index': elem_end})
                continue

            # Skip empty entities
            if not elem_value and skip_empty:
                continue

            # Fill in the entity fields
            etype = TYPE_REGEX.fullmatch(segment_label)
            entity = {'type': etype[1],
                      'name': elem_value,
                      'score': 1.0,
                      'start_index': elem_start,
                      'end_index': elem_end}
            if etype[2] and add_role:
                entity['role'] = etype[2]

            # Add entity to results
            entities.append(entity)

        # Sort the entities by appearance in the utterance
        entities = sorted(entities, key=itemgetter('start_index'))

        # Add to result list
        results.append(RESULT(intent, entities, tags, 1.0))
        if max_results and n+1 == max_results:
            break

    return results


# ---------------------------------------------------------------------------


class RecognizerGrammarEngine(GrammarEngine):
    '''
    Wrapper of the Grammar Engine to produce recognizer-like results: identify
    some of the symbols as intent or entities.
    '''

    def __init__(self, grammar_name: str, delaf_name: str, basedir: str=None,
                 add_role: bool=True, skip_empty_entities=True):
        if basedir:
            grammar_name = os.path.join(basedir, grammar_name)
            delaf_name = os.path.join(basedir, delaf_name)
        self._role = add_role
        self._skip_empty = skip_empty_entities
        super().__init__(grammar_name, delaf_name)


    def __call__(self, utterance: str, context: Dict=None,
                 **kwargs) -> List[RESULT]:
        '''
        Return a list with all found matches
        '''
        results = self.tag(utterance, context or {})
        role = kwargs.pop('add_role', self._role)
        skip = kwargs.pop('skip_empty_entities', self._skip_empty)
        return parse_native_results(utterance, results, add_role=role,
                                    skip_empty=skip, **kwargs)


    def top_match(self, utterance: str, context: Dict=None,
                  add_role: bool=True) -> Dict:
        '''
        Return the match with the highest weight
        '''
        result = self.__call__(utterance, context, add_role=add_role,
                               max_results=1)[0]

        data = {'utterance': utterance,
                'intent': result.intent,
                'entities': result.entities}
        if result.tags:
            data['tags'] = result.tags
        return data
