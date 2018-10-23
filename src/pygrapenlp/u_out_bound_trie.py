from pygrapenlp import u_array_to_string
from pygrapenlp.pygrapenlp import u_array


def u_out_bound_trie_string_to_string(native_u_out_bound_trie_string):
    string_size = native_u_out_bound_trie_string.size()
    native_u_array = u_array(string_size)
    native_u_out_bound_trie_string.to_array(native_u_array)
    string = u_array_to_string(native_u_array)
    return string
