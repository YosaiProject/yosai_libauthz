import ctypes

lib_path = "../target/release/libauthz.so"

lib = ctypes.cdll.LoadLibrary(lib_path)


def is_permitted_from_json(required_perm, serialized_perms):
    perms_buffer = serialized_perms.encode('utf-8')
    result = lib.is_permitted_from_json(ctypes.c_char_p(required_perm),
                                        perms_buffer, len(perms_buffer))
    if result == -1:
        raise ValueError("Rust Library, libauthz, panicked!")
    return bool(result)


def is_permitted_from_str(required_perm, assigned_perms):
    perm_array = (ctypes.c_char_p * len(assigned_perms))(*assigned_perms)
    result = lib.is_permitted_from_str(ctypes.c_char_p(required_perm),
                                       perm_array, len(assigned_perms))

    if result == -1:
        raise ValueError("Rust Library, libauthz, panicked!")
    return bool(result)
