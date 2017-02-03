
#ifndef LIBAUTHZ_H_INCLUDED
#define LIBAUTHZ_H_INCLUDED

int is_permitted_from_string(char *required_perm,
                             char **assigned_perms,
                             unsigned int assigned_perms_len);

int is_permitted_from_json(char *required_perm,
                           const char *assigned_perms,
                           unsigned int assigned_perms_len);

#endif
