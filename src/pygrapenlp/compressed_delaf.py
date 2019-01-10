from pygrapenlp import compressed_delaf, u_read_compressed_delaf, string_to_u_array, \
    add_u_set_trie_strings_to_string_set


class CompressedDelaf:
    def __init__(self, bin_delaf_pathname, inf_delaf_pathname):
        self.native_compressed_delaf = compressed_delaf()
        u_read_compressed_delaf(bin_delaf_pathname, inf_delaf_pathname, self.native_compressed_delaf)

    def reset(self, bin_delaf_pathname, inf_delaf_pathname):
        u_read_compressed_delaf(bin_delaf_pathname, inf_delaf_pathname, self.native_compressed_delaf)

    def get_ambiguous_word_properties(self, word):
        native_word = string_to_u_array(word)
        result = self.native_compressed_delaf.get_word_properties(native_word.const_begin(), native_word.const_end())
        return result

    def get_set_of_ambiguous_word_serialized_semantic_properties(self, word):
        ambiguous_word_properties = self.get_ambiguous_word_properties(word)
        result_set = set()
        if ambiguous_word_properties:
            for word_properties in ambiguous_word_properties:
                add_u_set_trie_strings_to_string_set(word_properties.semantic_traits, result_set)
        return result_set
