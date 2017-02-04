import os
from ._libauthz_native import ffi as _ffi

_lib = _ffi.dlopen(os.path.join(os.path.dirname(__file__), '_libauthz.so'))


lib = ctypes.cdll.LoadLibrary(lib_path)


def is_permitted_from_json(required_perm, serialized_perms):
    perms_buffer = serialized_perms.encode('utf-8')
    result = lib.is_permitted_from_json(required_perm, perms_buffer, len(perms_buffer))
    if result == -1:
        raise ValueError("Rust Library, libauthz, panicked!")
    return bool(result)


def is_permitted_from_str(required_perm, assigned_perms):
    result = lib.is_permitted_from_str(required_perm, assigned_perm, len(assigned_perms))

    if result == -1:
        raise ValueError("Rust Library, libauthz, panicked!")
    return bool(result)
