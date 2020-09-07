

from ..pygrapenlp import (new_byte_array,
                          u_array, byte_array_setitem, byte_array_getitem)


def is_debug_build() -> bool:
    '''
    Detect if we have a DEBUG or RELEASE build of the native engine, since they
    use different internal representations for character strings.
    '''
    ann = u_array.__init__.__annotations__
    return 'wchar_t' in ann.get('count_', '')


def u_array_to_string(u: u_array) -> str:
    '''
    Convert a engine character array representation to a Python string
    '''
    native_bytes = u.get_bytes()
    byte_count = u.size_in_bytes()
    python_bytes = bytearray(byte_count)
    for i in range(byte_count):
        python_bytes[i] = byte_array_getitem(native_bytes, i)
    encoding = 'utf-32le' if is_debug_build() else 'utf-16le'
    s = python_bytes.decode(encoding=encoding)
    return s


def string_to_u_array(s: str) -> u_array:
    '''
    Convert a Python string to the engine character array representation
    '''
    is_debug = is_debug_build()
    encoding = 'utf-32le' if is_debug else 'utf-16le'

    python_bytes = s.encode(encoding=encoding)
    byte_count = len(python_bytes)

    native_bytes = new_byte_array(byte_count)
    for i in range(byte_count):
        byte_array_setitem(native_bytes, i, python_bytes[i])
    my_u_array = u_array(byte_count >> (1 + is_debug))
    my_u_array.set_bytes(native_bytes)

    #print("ARRAY size =",my_u_array.size(),"bytes =",my_u_array.size_in_bytes())
    #bb = my_u_array.get_bytes()
    #for n in range(my_u_array.size_in_bytes()):
    #    print("{:2} =".format(n), repr(byte_array_getitem(bb, n)))

    return my_u_array


# ---------------------------------------------------------------------------

def string_to_u_array_TEST(s: str) -> u_array:
    python_bytes = s.encode(encoding='utf-16le')
    byte_count = len(python_bytes)

    print(s)
    print(repr(python_bytes))
    print("LEN", len(s), byte_count)

    if is_debug_build():
        print("DEBUG")
        native_bytes = new_byte_array(byte_count*2)
        for i in range(0, byte_count, 2):
            #print(i, i*4)
            byte_array_setitem(native_bytes, i*2, python_bytes[i])
            byte_array_setitem(native_bytes, i*2+1, python_bytes[i+1])
            byte_array_setitem(native_bytes, i*2+2, 0)
            byte_array_setitem(native_bytes, i*2+3, 0)
        my_u_array = u_array(byte_count >> 1)
        my_u_array.set_bytes(native_bytes)

        print("ARRA size =", my_u_array.size(), "bytes =",
              my_u_array.size_in_bytes())
        bb = my_u_array.get_bytes()
        for n in range(my_u_array.size_in_bytes()):
            print("{:2} =".format(n), repr(byte_array_getitem(bb, n)))

        return my_u_array

    native_bytes = new_byte_array(byte_count)
    for i in range(byte_count):
        byte_array_setitem(native_bytes, i, python_bytes[i])
    my_u_array = u_array(byte_count >> 1)
    my_u_array.set_bytes(native_bytes)
    return my_u_array
