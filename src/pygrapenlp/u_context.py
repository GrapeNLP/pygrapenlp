from pygrapenlp import u_context_key_value_hasher, u_context, string_to_u_array


def dico_to_u_context(dico, c_hasher: u_context_key_value_hasher):
    ctx = u_context(c_hasher)
    for key, value in dico.items():
        native_key = string_to_u_array(key)
        native_value = string_to_u_array(value)
        ctx.ua_set(native_key.const_begin(), native_key.const_end(), native_value.const_begin(), native_value.const_end())
    return ctx

