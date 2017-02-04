
#ifndef LIBAUTHZ_H_INCLUDED
#define LIBAUTHZ_H_INCLUDED

int is_permitted_from_string(const char *required_perm,
                             char **assigned_perms,
                             int assigned_perms_len);

int is_permitted_from_json(const char *required_perm,
                           char *assigned_perms,
                           int assigned_perms_len);

#endif
