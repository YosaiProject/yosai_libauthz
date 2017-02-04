import os
from yosai.core import authz_abcs

from ._libauthz_native import ffi as _ffi


class RustyPermissionVerifier:  # (authz_abcs.PermissionVerifier):
    def __init__(self):
        self.lib = _ffi.dlopen(os.path.join(os.path.dirname(__file__),
                               '_libauthz.so'))

    def is_permitted_from_json(self, required_perm, serialized_perms):
        perms_buffer = serialized_perms.encode('utf-8')
        result = self.lib.is_permitted_from_json(required_perm.encode('utf-8'),
                                                 perms_buffer,
                                                 len(perms_buffer))
        if result == -1:
            raise ValueError("Rust Library, libauthz, panicked!")
        return bool(result)

    def is_permitted_from_string(self, required_perm, assigned_perms):
        encoded_perms = [x.encode('utf-8') for x in assigned_perms]
        result = self.lib.is_permitted_from_string(required_perm.encode('utf-8'),
                                                   encoded_perms,
                                                   len(encoded_perms))

        if result == -1:
            raise ValueError("Rust Library, libauthz, panicked!")
        return bool(result)
