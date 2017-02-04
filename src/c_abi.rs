use std::slice;
use std::ffi::CStr;
use std::panic;
use std::str;
use libc::{size_t, c_char, c_int};

use authz::{is_permitted_from_str, is_permitted_from_perm, perms_from_buffer, Permission};


#[no_mangle]
pub unsafe extern "C" fn is_permitted_from_string(required_perm: *const c_char,
                                                  assigned_perms: *const *const c_char,
                                                  assigned_perms_len: size_t)
                                                  -> c_int {

    let res = panic::catch_unwind(|| {
        // unsafe is on by default
        let ffi_required_permission = CStr::from_ptr(required_perm);
        let required_permission = match ffi_required_permission.to_str() {
            Ok(s) => s,
            Err(_) => return -1,
        };
        // unsafe is on by default:
        let perms = slice::from_raw_parts(assigned_perms, assigned_perms_len as usize);
        let assigned_permissions = perms.iter()
            .map(|&p| CStr::from_ptr(p))
            .map(|cs| cs.to_bytes())
            .map(|bs| str::from_utf8(bs).unwrap_or_else(|_| ""));

        is_permitted_from_str(required_permission, assigned_permissions)
    });

    match res {
        Ok(rc) => rc,
        Err(_) => -2,
    }
}


#[no_mangle]
pub unsafe extern "C" fn is_permitted_from_json(required_perm: *const c_char,
                                                assigned_perms: *const u8,
                                                assigned_perms_len: size_t)
                                                -> c_int {
    let res = panic::catch_unwind(|| {
        let ffi_required_permission = CStr::from_ptr(required_perm); // unsafe is on by default
        let required = match ffi_required_permission.to_str() {
            Ok(s) => s,
            Err(_) => return -3,
        };

        // unsafe is on by default:
        let serialized_perms = slice::from_raw_parts(assigned_perms, assigned_perms_len as usize);

        // using _ for the error lets the compiler figure out what error type it is:
        let deserialized: Result<Vec<Permission>, _> = perms_from_buffer(serialized_perms);
        let assigned = match deserialized {
            Ok(x) => x,
            Err(e) => {
                println!("{:?}", e);
                return -4;
            }
        };

        is_permitted_from_perm(&required, assigned)
    });
    match res {
        Ok(rc) => rc,
        Err(_) => -5,
    }
}
