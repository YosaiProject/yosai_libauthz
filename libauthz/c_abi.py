import os
from yosai.core import authz_abcs

from ._libauthz_native import ffi


class RustyPermissionVerifier:  # (authz_abcs.PermissionVerifier):
    def __init__(self):
        self.ffi = ffi
        self.lib = self.ffi.dlopen(os.path.join(os.path.dirname(__file__),
                                   '_libauthz.so'))

    def is_permitted_from_json(self, required_perm, serialized_perms):
        rp_keepalive = self.ffi.new("char[]", required_perm.encode('utf-8'))

        perms_buffer = serialized_perms.encode('utf-8')
        result = self.lib.is_permitted_from_json(rp_keepalive,
                                                 perms_buffer,
                                                 len(perms_buffer))
        if result < 0:
            msg = "Rust Library, libauthz, panicked!  Error: {}".format(result)
            raise ValueError(msg)
        return bool(result)

    def is_permitted_from_string(self, required_perm, assigned_perms):
        rp_keepalive = self.ffi.new("char[]", required_perm.encode('utf-8'))

        ap_keepalive = [self.ffi.new("char[]", perm.encode('utf-8')) for perm
                        in assigned_perms]
        assigned_permissions = self.ffi.new("char *[]", ap_keepalive)

        result = self.lib.is_permitted_from_string(rp_keepalive,
                                                   assigned_permissions,
                                                   len(assigned_permissions))

        if result < 0:
            msg = "Rust Library, libauthz, panicked! Error: {}".format(result)
            raise ValueError(msg)
        return bool(result)
