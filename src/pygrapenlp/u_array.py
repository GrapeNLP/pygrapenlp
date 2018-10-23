from pygrapenlp import new_byte_array, byte_array_setitem, u_array, byte_array_getitem


def string_to_u_array(s):
    python_bytes = s.encode(encoding='utf-16le')
    byte_count = len(python_bytes)
    native_bytes = new_byte_array(byte_count)
    for i in range(byte_count):
        byte_array_setitem(native_bytes, i, python_bytes[i])
    my_u_array = u_array(byte_count >> 1)
    my_u_array.set_bytes(native_bytes)
    return my_u_array

def u_array_to_string(u):
    native_bytes = u.get_bytes()
    byte_count = u.size_in_bytes()
    python_bytes = bytearray(byte_count)
    for i in range(byte_count):
        python_bytes[i] = byte_array_getitem(native_bytes, i)
    s = python_bytes.decode(encoding='utf-16le')
    return s
