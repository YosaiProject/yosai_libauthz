import os
from yosai.core import authz_abcs

from ._libauthz_native import ffi


class RustyPermissionVerifier:  # (authz_abcs.PermissionVerifier):
    def __init__(self):
        self.ffi = ffi
        self.lib = self.ffi.dlopen(os.path.join(os.path.dirname(__file__),
                                   '_libauthz.so'))

    def is_permitted_from_json(self, required_perm, assigned_perms):
        """
        :type required_perm: string

        :param assigned_perms: a json blob of assigned permission dicts
        :type assigned_perms: bytes
        """
        rp_keepalive = self.ffi.new("char[]", required_perm.encode('utf-8'))
        ap_keepalive = assigned_perms
        result = self.lib.is_permitted_from_json(rp_keepalive,
                                                 ap_keepalive,
                                                 len(ap_keepalive))
        if result < 0:
            msg = "Rust Library, libauthz, panicked!  Error: {}".format(result)
            raise ValueError(msg)
        return bool(result)

    def is_permitted_from_string(self, required_perm, assigned_perms):
        """
        :type required_perm: string

        :param assigned_perms: a list of wildcard_perm strings
        :type assigned_perms: list
        """
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
