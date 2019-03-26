from pygrapenlp import ualxiw_manager, LEXMASK_X_WEIGHTED_EXTRACTION_RTNO, \
    TO_FPRTN_AND_TOP_BLACKBOARD_EXTRACT_RTNO_PARSER, LRB_TREE, STD, string_to_u_array, dico_to_u_context


class GrammarEngine:
    def __init__(self, grammar_pathname, bin_delaf_pathname):
        self.native_grammar_engine = ualxiw_manager(LEXMASK_X_WEIGHTED_EXTRACTION_RTNO, grammar_pathname,
                                                    bin_delaf_pathname)

    def reset_models(self, grammar_pathname, bin_delaf_pathname):
        self.native_grammar_engine = ualxiw_manager(LEXMASK_X_WEIGHTED_EXTRACTION_RTNO, grammar_pathname,
                                                    bin_delaf_pathname)

    def tag(self, sentence, context=None):
        if context is None:
            context = {}
        native_context = dico_to_u_context(context, self.native_grammar_engine.get_context_key_value_hasher())
        native_sentence = string_to_u_array(sentence)
        self.native_grammar_engine.process(native_sentence.const_begin(), native_sentence.const_end(), native_context,
                                           TO_FPRTN_AND_TOP_BLACKBOARD_EXTRACT_RTNO_PARSER, True, False, LRB_TREE, STD)
        return self.native_grammar_engine.get_simplified_weighted_output()
