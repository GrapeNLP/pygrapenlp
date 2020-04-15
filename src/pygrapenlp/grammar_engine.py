'''
Raw grammar engine wrapper
'''

from .pygrapenlp import ualxiw_manager, LEXMASK_X_WEIGHTED_EXTRACTION_RTNO, \
    TO_FPRTN_AND_TOP_BLACKBOARD_EXTRACT_RTNO_PARSER, LRB_TREE, STD

from .utils.u_array import string_to_u_array
from .utils.u_context import dico_to_u_context


from typing import Dict


class GrammarEngine:
    '''
    Raw grammar engine wrapper
    '''

    def __init__(self, grammar_pathname: str, bin_delaf_pathname: str):
        self._build_model(grammar_pathname, bin_delaf_pathname)


    def _build_model(self, grammar_pathname: str, bin_delaf_pathname: str):
        '''
        Create the grammar
        '''
        self.native_grammar_engine = \
            ualxiw_manager(LEXMASK_X_WEIGHTED_EXTRACTION_RTNO, grammar_pathname,
                           bin_delaf_pathname)


    def reset_models(self, grammar_pathname: str, bin_delaf_pathname: str):
        '''
        Re-create the grammar
        '''
        self._build_model(grammar_pathname, bin_delaf_pathname)


    def tag(self, sentence: str, context: Dict=None):
        '''
        Run the engine & get tags for a sentence
        '''
        # Check data
        if context is None:
            context = {}
        elif not isinstance(context, dict):
            raise Exception("invalid context object: {}".format(type(context)))
        if not isinstance(sentence, str):
            raise Exception("invalid utterance object: {}".format(type(sentence)))

        # Convert data
        native_context = dico_to_u_context(context, self.native_grammar_engine.get_context_key_value_hasher())
        native_sentence = string_to_u_array(sentence)

        # Parse (call ul_manager::process)
        self.native_grammar_engine.process(
            native_sentence.const_begin(),      # InputIterator input_begin,
            native_sentence.const_end(),        # InputIterator input_end,
            native_context,                     # const u_context &ctx,
            TO_FPRTN_AND_TOP_BLACKBOARD_EXTRACT_RTNO_PARSER,    # rtno_parser_type
            True,                               # bool trie_strings,
            False,                              # bool no_output,
            LRB_TREE,                           # assoc_container_impl_choice the_execution_state_set_impl_choice,
            STD)                                # assoc_container_impl_choice the_output_set_impl_choice)

        # Fetch results
        return self.native_grammar_engine.get_simplified_weighted_output()

    def __call__(self, *args, **kwargs):
        return self.tag(*args, **kwargs)
