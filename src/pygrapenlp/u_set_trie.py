from pygrapenlp import u_array_to_string
from pygrapenlp.pygrapenlp import ust_set_deref, u_array


def u_set_trie_string_to_string(native_u_set_trie_string):
    string_size = native_u_set_trie_string.size()
    native_u_array = u_array(string_size)
    native_u_set_trie_string.to_array(native_u_array)
    string = u_array_to_string(native_u_array)
    return string


def add_u_set_trie_strings_to_string_set(native_u_set_trie, string_set):
    ust_set = ust_set_deref(native_u_set_trie)
    for native_u_set_trie_string_ref in ust_set:
        string = u_set_trie_string_to_string(native_u_set_trie_string_ref)
        string_set.add(string)


def u_set_trie_to_string_set(native_u_set_trie):
    string_set = set()
    add_u_set_trie_strings_to_string_set(native_u_set_trie, string_set)
    return string_set
