/* -*- mode: C; c-file-style: "gnu"; indent-tabs-mode: nil; -*-
 * vim: tabstop=4 shiftwidth=4 expandtab
 */

#include <glib-object.h>

#ifndef __GI_MARSHALLING_TESTS_H__
#define __GI_MARSHALLING_TESTS_H__

typedef struct _GIMarshallingTestsSimpleStruct GIMarshallingTestsSimpleStruct;
typedef struct _GIMarshallingTestsBoxedStruct GIMarshallingTestsBoxedStruct;

/* Constants */

#define GI_MARSHALLING_TESTS_CONSTANT_NUMBER 42
#define GI_MARSHALLING_TESTS_CONSTANT_UTF8   "const \xe2\x99\xa5 utf8"


/* Booleans */

gboolean gi_marshalling_tests_boolean_return_true (void);
gboolean gi_marshalling_tests_boolean_return_false (void);

void gi_marshalling_tests_boolean_in_true (gboolean v);
void gi_marshalling_tests_boolean_in_false (gboolean v);

void gi_marshalling_tests_boolean_out_true (gboolean *v);
void gi_marshalling_tests_boolean_out_false (gboolean *v);

void gi_marshalling_tests_boolean_inout_true_false (gboolean *v);
void gi_marshalling_tests_boolean_inout_false_true (gboolean *v);


/* Integers */

gint8 gi_marshalling_tests_int8_return_max (void);
gint8 gi_marshalling_tests_int8_return_min (void);

void gi_marshalling_tests_int8_in_max (gint8 v);
void gi_marshalling_tests_int8_in_min (gint8 v);

void gi_marshalling_tests_int8_out_max (gint8 *v);
void gi_marshalling_tests_int8_out_min (gint8 *v);

void gi_marshalling_tests_int8_inout_max_min (gint8 *v);
void gi_marshalling_tests_int8_inout_min_max (gint8 *v);


guint8 gi_marshalling_tests_uint8_return (void);

void gi_marshalling_tests_uint8_in (guint8 v);

void gi_marshalling_tests_uint8_out (guint8 *v);
void gi_marshalling_tests_uint8_inout (guint8 *v);


gint16 gi_marshalling_tests_int16_return_max (void);
gint16 gi_marshalling_tests_int16_return_min (void);

void gi_marshalling_tests_int16_in_max (gint16 v);
void gi_marshalling_tests_int16_in_min (gint16 v);

void gi_marshalling_tests_int16_out_max (gint16 *v);
void gi_marshalling_tests_int16_out_min (gint16 *v);

void gi_marshalling_tests_int16_inout_max_min (gint16 *v);
void gi_marshalling_tests_int16_inout_min_max (gint16 *v);


guint16 gi_marshalling_tests_uint16_return (void);

void gi_marshalling_tests_uint16_in (guint16 v);

void gi_marshalling_tests_uint16_out (guint16 *v);
void gi_marshalling_tests_uint16_inout (guint16 *v);


gint32 gi_marshalling_tests_int32_return_max (void);
gint32 gi_marshalling_tests_int32_return_min (void);

void gi_marshalling_tests_int32_in_max (gint32 v);
void gi_marshalling_tests_int32_in_min (gint32 v);

void gi_marshalling_tests_int32_out_max (gint32 *v);
void gi_marshalling_tests_int32_out_min (gint32 *v);

void gi_marshalling_tests_int32_inout_max_min (gint32 *v);
void gi_marshalling_tests_int32_inout_min_max (gint32 *v);


guint32 gi_marshalling_tests_uint32_return (void);

void gi_marshalling_tests_uint32_in (guint32 v);

void gi_marshalling_tests_uint32_out (guint32 *v);
void gi_marshalling_tests_uint32_inout (guint32 *v);


gint64 gi_marshalling_tests_int64_return_max (void);
gint64 gi_marshalling_tests_int64_return_min (void);

void gi_marshalling_tests_int64_in_max (gint64 v);
void gi_marshalling_tests_int64_in_min (gint64 v);

void gi_marshalling_tests_int64_out_max (gint64 *v);
void gi_marshalling_tests_int64_out_min (gint64 *v);

void gi_marshalling_tests_int64_inout_max_min (gint64 *v);
void gi_marshalling_tests_int64_inout_min_max (gint64 *v);


guint64 gi_marshalling_tests_uint64_return (void);

void gi_marshalling_tests_uint64_in (guint64 v);

void gi_marshalling_tests_uint64_out (guint64 *v);
void gi_marshalling_tests_uint64_inout (guint64 *v);


gshort gi_marshalling_tests_short_return_max (void);
gshort gi_marshalling_tests_short_return_min (void);

void gi_marshalling_tests_short_in_max (gshort short_);
void gi_marshalling_tests_short_in_min (gshort short_);

void gi_marshalling_tests_short_out_max (gshort *short_);
void gi_marshalling_tests_short_out_min (gshort *short_);

void gi_marshalling_tests_short_inout_max_min (gshort *short_);
void gi_marshalling_tests_short_inout_min_max (gshort *short_);


gushort gi_marshalling_tests_ushort_return (void);

void gi_marshalling_tests_ushort_in (gushort ushort_);

void gi_marshalling_tests_ushort_out (gushort *ushort_);
void gi_marshalling_tests_ushort_inout (gushort *ushort_);


gint gi_marshalling_tests_int_return_max (void);
gint gi_marshalling_tests_int_return_min (void);

void gi_marshalling_tests_int_in_max (gint int_);
void gi_marshalling_tests_int_in_min (gint int_);

void gi_marshalling_tests_int_out_max (gint *int_);
void gi_marshalling_tests_int_out_min (gint *int_);

void gi_marshalling_tests_int_inout_max_min (gint *int_);
void gi_marshalling_tests_int_inout_min_max (gint *int_);


guint gi_marshalling_tests_uint_return (void);

void gi_marshalling_tests_uint_in (guint uint_);

void gi_marshalling_tests_uint_out (guint *uint_);
void gi_marshalling_tests_uint_inout (guint *uint_);


glong gi_marshalling_tests_long_return_max (void);
glong gi_marshalling_tests_long_return_min (void);

void gi_marshalling_tests_long_in_max (glong long_);
void gi_marshalling_tests_long_in_min (glong long_);

void gi_marshalling_tests_long_out_max (glong *long_);
void gi_marshalling_tests_long_out_min (glong *long_);

void gi_marshalling_tests_long_inout_max_min (glong *long_);
void gi_marshalling_tests_long_inout_min_max (glong *long_);


gulong gi_marshalling_tests_ulong_return (void);

void gi_marshalling_tests_ulong_in (gulong ulong_);

void gi_marshalling_tests_ulong_out (gulong *ulong_);
void gi_marshalling_tests_ulong_inout (gulong *ulong_);


gssize gi_marshalling_tests_ssize_return_max (void);
gssize gi_marshalling_tests_ssize_return_min (void);

void gi_marshalling_tests_ssize_in_max (gssize ssize);
void gi_marshalling_tests_ssize_in_min (gssize ssize);

void gi_marshalling_tests_ssize_out_max (gssize *ssize);
void gi_marshalling_tests_ssize_out_min (gssize *ssize);

void gi_marshalling_tests_ssize_inout_max_min (gssize *ssize);
void gi_marshalling_tests_ssize_inout_min_max (gssize *ssize);


gsize gi_marshalling_tests_size_return (void);

void gi_marshalling_tests_size_in (gsize size);

void gi_marshalling_tests_size_out (gsize *size);
void gi_marshalling_tests_size_inout (gsize *size);


/* Floating-point */

gfloat gi_marshalling_tests_float_return (void);

void gi_marshalling_tests_float_in (gfloat v);

void gi_marshalling_tests_float_out (gfloat *v);

void gi_marshalling_tests_float_inout (gfloat *v);


gdouble gi_marshalling_tests_double_return (void);

void gi_marshalling_tests_double_in (gdouble v);

void gi_marshalling_tests_double_out (gdouble *v);

void gi_marshalling_tests_double_inout (gdouble *v);


/* Timestamps */

time_t gi_marshalling_tests_time_t_return (void);

void gi_marshalling_tests_time_t_in (time_t v);

void gi_marshalling_tests_time_t_out (time_t *v);

void gi_marshalling_tests_time_t_inout (time_t *v);


/* GType */

GType gi_marshalling_tests_gtype_return (void);

GType gi_marshalling_tests_gtype_string_return (void);

void gi_marshalling_tests_gtype_in (GType gtype);

void gi_marshalling_tests_gtype_string_in (GType gtype);

void gi_marshalling_tests_gtype_out (GType *gtype);

void gi_marshalling_tests_gtype_string_out (GType *gtype);

void gi_marshalling_tests_gtype_inout (GType *gtype);


/* UTF-8 */

const gchar *gi_marshalling_tests_utf8_none_return (void);
gchar *gi_marshalling_tests_utf8_full_return (void);

void gi_marshalling_tests_utf8_none_in (const gchar *utf8);
void gi_marshalling_tests_utf8_full_in (gchar *utf8);

void gi_marshalling_tests_utf8_none_out (gchar **utf8);
void gi_marshalling_tests_utf8_full_out (gchar **utf8);

void gi_marshalling_tests_utf8_dangling_out (gchar **utf8);

void gi_marshalling_tests_utf8_none_inout (gchar **utf8);
void gi_marshalling_tests_utf8_full_inout (gchar **utf8);

GSList *gi_marshalling_tests_filename_list_return (void);

void gi_marshalling_tests_utf8_as_uint8array_in (const guint8 *array,
                                                 gsize         len);


/* Enum */

typedef enum
{
  GI_MARSHALLING_TESTS_ENUM_VALUE1,
  GI_MARSHALLING_TESTS_ENUM_VALUE2,
  GI_MARSHALLING_TESTS_ENUM_VALUE3 = 42
} GIMarshallingTestsEnum;

typedef enum
{
  GI_MARSHALLING_TESTS_SECOND_ENUM_SECONDVALUE1,
  GI_MARSHALLING_TESTS_SECOND_ENUM_SECONDVALUE2,
} GIMarshallingTestsSecondEnum;

GIMarshallingTestsEnum gi_marshalling_tests_enum_returnv (void);

void gi_marshalling_tests_enum_in (GIMarshallingTestsEnum v);

void gi_marshalling_tests_enum_out (GIMarshallingTestsEnum *v);

void gi_marshalling_tests_enum_inout (GIMarshallingTestsEnum *v);


/* GEnum */

typedef enum
{
  GI_MARSHALLING_TESTS_GENUM_VALUE1,
  GI_MARSHALLING_TESTS_GENUM_VALUE2,
  GI_MARSHALLING_TESTS_GENUM_VALUE3 = 42
} GIMarshallingTestsGEnum;

GType gi_marshalling_tests_genum_get_type (void) G_GNUC_CONST;
#define GI_MARSHALLING_TESTS_TYPE_GENUM (gi_marshalling_tests_genum_get_type ())

GIMarshallingTestsGEnum gi_marshalling_tests_genum_returnv (void);

void gi_marshalling_tests_genum_in (GIMarshallingTestsGEnum v);

void gi_marshalling_tests_genum_out (GIMarshallingTestsGEnum *v);

void gi_marshalling_tests_genum_inout (GIMarshallingTestsGEnum *v);


/* GFlags */

typedef enum
{
  GI_MARSHALLING_TESTS_FLAGS_VALUE1 = 1 << 0,
  GI_MARSHALLING_TESTS_FLAGS_VALUE2 = 1 << 1,
  GI_MARSHALLING_TESTS_FLAGS_VALUE3 = 1 << 2,
  GI_MARSHALLING_TESTS_FLAGS_MASK = GI_MARSHALLING_TESTS_FLAGS_VALUE1 |
                                    GI_MARSHALLING_TESTS_FLAGS_VALUE2,
  GI_MARSHALLING_TESTS_FLAGS_MASK2 = GI_MARSHALLING_TESTS_FLAGS_MASK
} GIMarshallingTestsFlags;

GType gi_marshalling_tests_flags_get_type (void) G_GNUC_CONST;
#define GI_MARSHALLING_TESTS_TYPE_FLAGS (gi_marshalling_tests_flags_get_type ())

GIMarshallingTestsFlags gi_marshalling_tests_flags_returnv (void);

void gi_marshalling_tests_flags_in (GIMarshallingTestsFlags v);
void gi_marshalling_tests_flags_in_zero (GIMarshallingTestsFlags v);

void gi_marshalling_tests_flags_out (GIMarshallingTestsFlags *v);

void gi_marshalling_tests_flags_inout (GIMarshallingTestsFlags *v);

/* Flags with no GType */

typedef enum
{
  GI_MARSHALLING_TESTS_NO_TYPE_FLAGS_VALUE1 = 1 << 0,
  GI_MARSHALLING_TESTS_NO_TYPE_FLAGS_VALUE2 = 1 << 1,
  GI_MARSHALLING_TESTS_NO_TYPE_FLAGS_VALUE3 = 1 << 2,
  GI_MARSHALLING_TESTS_NO_TYPE_FLAGS_MASK = GI_MARSHALLING_TESTS_NO_TYPE_FLAGS_VALUE1 |
                                            GI_MARSHALLING_TESTS_NO_TYPE_FLAGS_VALUE2,
  GI_MARSHALLING_TESTS_NO_TYPE_FLAGS_MASK2 = GI_MARSHALLING_TESTS_FLAGS_MASK
} GIMarshallingTestsNoTypeFlags;

GIMarshallingTestsNoTypeFlags gi_marshalling_tests_no_type_flags_returnv (void);

void gi_marshalling_tests_no_type_flags_in (GIMarshallingTestsNoTypeFlags v);
void gi_marshalling_tests_no_type_flags_in_zero (GIMarshallingTestsNoTypeFlags v);

void gi_marshalling_tests_no_type_flags_out (GIMarshallingTestsNoTypeFlags *v);

void gi_marshalling_tests_no_type_flags_inout (GIMarshallingTestsNoTypeFlags *v);

/* Arrays */

gboolean gi_marshalling_tests_init_function (gint *n_args, char ***argv);

/* Fixed-size */
const gint *gi_marshalling_tests_array_fixed_int_return (void);
const gshort *gi_marshalling_tests_array_fixed_short_return (void);

void gi_marshalling_tests_array_fixed_int_in (const gint *ints);
void gi_marshalling_tests_array_fixed_short_in (const gshort *shorts);

void gi_marshalling_tests_array_fixed_out (gint **ints);

void gi_marshalling_tests_array_fixed_out_struct (GIMarshallingTestsSimpleStruct **structs);

void gi_marshalling_tests_array_fixed_inout (gint **ints);

/* Variable-size */

const gint *gi_marshalling_tests_array_return (gint *length);
const gint *gi_marshalling_tests_array_return_etc (gint first, gint *length, gint last, gint *sum);

void gi_marshalling_tests_array_in (const gint *ints, gint length);
void gi_marshalling_tests_array_in_len_before (gint length, const gint *ints);
void gi_marshalling_tests_array_in_len_zero_terminated (const gint *ints, gint length);
void gi_marshalling_tests_array_string_in (const gchar **strings, gint length);
void gi_marshalling_tests_array_uint8_in (const guint8 *chars, gint length);
void gi_marshalling_tests_array_struct_in (GIMarshallingTestsBoxedStruct **structs, gint length);
void gi_marshalling_tests_array_struct_value_in (GIMarshallingTestsBoxedStruct *structs, gint length);
void gi_marshalling_tests_array_struct_take_in (GIMarshallingTestsBoxedStruct **structs, gint length);
void gi_marshalling_tests_array_simple_struct_in (GIMarshallingTestsSimpleStruct *structs, gint length);
void gi_marshalling_tests_multi_array_key_value_in (gint length, const gchar **keys, const GValue *values);
void gi_marshalling_tests_array_enum_in (GIMarshallingTestsEnum *_enum, gint length);
void gi_marshalling_tests_array_in_guint64_len (const gint *ints, guint64 length);
void gi_marshalling_tests_array_in_guint8_len (const gint *ints, guint8 length);

void gi_marshalling_tests_array_out (gint **ints, gint *length);
void gi_marshalling_tests_array_out_etc (gint first, gint **ints, gint *length, gint last, gint *sum);

void gi_marshalling_tests_array_inout (gint **ints, gint *length);
void gi_marshalling_tests_array_inout_etc (gint first, gint **ints, gint *length, gint last, gint *sum);

void gi_marshalling_tests_array_in_nonzero_nonlen (gint first, const guint8 *chars);

/* Zero-terminated */

gchar **gi_marshalling_tests_array_zero_terminated_return (void);
gchar **gi_marshalling_tests_array_zero_terminated_return_null (void);
GIMarshallingTestsBoxedStruct **gi_marshalling_tests_array_zero_terminated_return_struct (void);

void gi_marshalling_tests_array_zero_terminated_in (gchar **utf8s);

void gi_marshalling_tests_array_zero_terminated_out (gchar ***utf8s);

void gi_marshalling_tests_array_zero_terminated_inout (gchar ***utf8s);

GVariant **gi_marshalling_tests_array_gvariant_none_in (GVariant **variants);

GVariant **gi_marshalling_tests_array_gvariant_container_in (GVariant **variants);

GVariant **gi_marshalling_tests_array_gvariant_full_in (GVariant **variants);


/* GArray */

GArray *gi_marshalling_tests_garray_int_none_return (void);
GArray *gi_marshalling_tests_garray_uint64_none_return (void);
GArray *gi_marshalling_tests_garray_utf8_none_return (void);
GArray *gi_marshalling_tests_garray_utf8_container_return (void);
GArray *gi_marshalling_tests_garray_utf8_full_return (void);

void gi_marshalling_tests_garray_int_none_in (GArray *array_);
void gi_marshalling_tests_garray_uint64_none_in (GArray *array_);
void gi_marshalling_tests_garray_utf8_none_in (GArray *array_);

void gi_marshalling_tests_garray_utf8_none_out (GArray **array_);
void gi_marshalling_tests_garray_utf8_container_out (GArray **array_);
void gi_marshalling_tests_garray_utf8_full_out (GArray **array_);
void gi_marshalling_tests_garray_utf8_full_out_caller_allocated (GArray *array_);

void gi_marshalling_tests_garray_utf8_none_inout (GArray **array_);
void gi_marshalling_tests_garray_utf8_container_inout (GArray **array_);
void gi_marshalling_tests_garray_utf8_full_inout (GArray **array_);

/* GPtrArray */
GPtrArray *gi_marshalling_tests_gptrarray_utf8_none_return (void);
GPtrArray *gi_marshalling_tests_gptrarray_utf8_container_return (void);
GPtrArray *gi_marshalling_tests_gptrarray_utf8_full_return (void);

void gi_marshalling_tests_gptrarray_utf8_none_in (GPtrArray *parray_);

void gi_marshalling_tests_gptrarray_utf8_none_out (GPtrArray **parray_);
void gi_marshalling_tests_gptrarray_utf8_container_out (GPtrArray **parray_);
void gi_marshalling_tests_gptrarray_utf8_full_out (GPtrArray **parray_);

void gi_marshalling_tests_gptrarray_utf8_none_inout (GPtrArray **parray_);
void gi_marshalling_tests_gptrarray_utf8_container_inout (GPtrArray **parray_);
void gi_marshalling_tests_gptrarray_utf8_full_inout (GPtrArray **parray_);

/* GByteArray */

GByteArray *gi_marshalling_tests_bytearray_full_return (void);
void gi_marshalling_tests_bytearray_none_in (GByteArray* v);

/* GBytes */

GBytes *gi_marshalling_tests_gbytes_full_return (void);
void gi_marshalling_tests_gbytes_none_in (GBytes* v);

/* GStrv */

GStrv gi_marshalling_tests_gstrv_return (void);
void gi_marshalling_tests_gstrv_in (GStrv g_strv);
void gi_marshalling_tests_gstrv_out (GStrv *g_strv);
void gi_marshalling_tests_gstrv_inout (GStrv *g_strv);

/* GList */

GList *gi_marshalling_tests_glist_int_none_return (void);
GList *gi_marshalling_tests_glist_uint32_none_return (void);
GList *gi_marshalling_tests_glist_utf8_none_return (void);
GList *gi_marshalling_tests_glist_utf8_container_return (void);
GList *gi_marshalling_tests_glist_utf8_full_return (void);

void gi_marshalling_tests_glist_int_none_in (GList *list);
void gi_marshalling_tests_glist_uint32_none_in (GList *list);
void gi_marshalling_tests_glist_utf8_none_in (GList *list);

void gi_marshalling_tests_glist_utf8_none_out (GList **list);
void gi_marshalling_tests_glist_utf8_container_out (GList **list);
void gi_marshalling_tests_glist_utf8_full_out (GList **list);

void gi_marshalling_tests_glist_utf8_none_inout (GList **list);
void gi_marshalling_tests_glist_utf8_container_inout (GList **list);
void gi_marshalling_tests_glist_utf8_full_inout (GList **list);


/* GSList */

GSList *gi_marshalling_tests_gslist_int_none_return (void);
GSList *gi_marshalling_tests_gslist_utf8_none_return (void);
GSList *gi_marshalling_tests_gslist_utf8_container_return (void);
GSList *gi_marshalling_tests_gslist_utf8_full_return (void);

void gi_marshalling_tests_gslist_int_none_in (GSList *list);
void gi_marshalling_tests_gslist_utf8_none_in (GSList *list);

void gi_marshalling_tests_gslist_utf8_none_out (GSList **list);
void gi_marshalling_tests_gslist_utf8_container_out (GSList **list);
void gi_marshalling_tests_gslist_utf8_full_out (GSList **list);

void gi_marshalling_tests_gslist_utf8_none_inout (GSList **list);
void gi_marshalling_tests_gslist_utf8_container_inout (GSList **list);
void gi_marshalling_tests_gslist_utf8_full_inout (GSList **list);


/* GHashTable */

GHashTable *gi_marshalling_tests_ghashtable_int_none_return (void);
GHashTable *gi_marshalling_tests_ghashtable_utf8_none_return (void);
GHashTable *gi_marshalling_tests_ghashtable_utf8_container_return (void);
GHashTable *gi_marshalling_tests_ghashtable_utf8_full_return (void);

void gi_marshalling_tests_ghashtable_int_none_in (GHashTable *hash_table);
void gi_marshalling_tests_ghashtable_utf8_none_in (GHashTable *hash_table);
void gi_marshalling_tests_ghashtable_utf8_container_in (GHashTable *hash_table);
void gi_marshalling_tests_ghashtable_utf8_full_in (GHashTable *hash_table);

void gi_marshalling_tests_ghashtable_utf8_none_out (GHashTable **hash_table);
void gi_marshalling_tests_ghashtable_utf8_container_out (GHashTable **hash_table);
void gi_marshalling_tests_ghashtable_utf8_full_out (GHashTable **hash_table);

void gi_marshalling_tests_ghashtable_utf8_none_inout (GHashTable **hash_table);
void gi_marshalling_tests_ghashtable_utf8_container_inout (GHashTable **hash_table);
void gi_marshalling_tests_ghashtable_utf8_full_inout (GHashTable **hash_table);


/* GValue */

GValue *gi_marshalling_tests_gvalue_return (void);

void gi_marshalling_tests_gvalue_in (GValue *value);
void gi_marshalling_tests_gvalue_int64_in (GValue *value);
void gi_marshalling_tests_gvalue_in_with_type (GValue *value, GType type);

void gi_marshalling_tests_gvalue_in_enum (GValue *value);

void gi_marshalling_tests_gvalue_out (GValue **value);
void gi_marshalling_tests_gvalue_int64_out (GValue **value);
void gi_marshalling_tests_gvalue_out_caller_allocates (GValue *value);

void gi_marshalling_tests_gvalue_inout (GValue **value);

void gi_marshalling_tests_gvalue_flat_array (guint         n_values,
                                             const GValue *values);

GValue *gi_marshalling_tests_return_gvalue_flat_array (void);

GValue *gi_marshalling_tests_gvalue_flat_array_round_trip (const GValue one,
                                                           const GValue two,
                                                           const GValue three);

/* GClosure */

void gi_marshalling_tests_gclosure_in (GClosure *closure);
GClosure *gi_marshalling_tests_gclosure_return (void);

/* Callback return values */

/**
 * GIMarshallingTestsCallbackReturnValueOnly:
 */
typedef glong (* GIMarshallingTestsCallbackReturnValueOnly) (void);

glong gi_marshalling_tests_callback_return_value_only (GIMarshallingTestsCallbackReturnValueOnly callback);

/**
 * GIMarshallingTestsCallbackOneOutParameter:
 * @a: (out):
 */
typedef void (* GIMarshallingTestsCallbackOneOutParameter) (gfloat *a);

void gi_marshalling_tests_callback_one_out_parameter (GIMarshallingTestsCallbackOneOutParameter  callback,
                                                      gfloat                                    *a);

/**
 * GIMarshallingTestsCallbackMultipleOutParameters:
 * @a: (out):
 * @b: (out):
 */
typedef void (* GIMarshallingTestsCallbackMultipleOutParameters) (gfloat *a, gfloat *b);

void gi_marshalling_tests_callback_multiple_out_parameters (GIMarshallingTestsCallbackMultipleOutParameters  callback,
                                                            gfloat                                          *a,
                                                            gfloat                                          *b);

/**
 * GIMarshallingTestsCallbackReturnValueAndOneOutParameter:
 * @a: (out):
 */
typedef glong (* GIMarshallingTestsCallbackReturnValueAndOneOutParameter) (glong *a);

glong gi_marshalling_tests_callback_return_value_and_one_out_parameter (GIMarshallingTestsCallbackReturnValueAndOneOutParameter  callback,
                                                                        glong                                                   *a);

/**
 * GIMarshallingTestsCallbackReturnValueAndMultipleOutParameters:
 * @a: (out):
 * @b: (out):
 */
typedef glong (* GIMarshallingTestsCallbackReturnValueAndMultipleOutParameters) (glong *a, glong *b);

glong gi_marshalling_tests_callback_return_value_and_multiple_out_parameters (GIMarshallingTestsCallbackReturnValueAndMultipleOutParameters  callback,
                                                                              glong                                                         *a,
                                                                              glong                                                         *b);

/* Pointer */

gpointer gi_marshalling_tests_pointer_in_return (gpointer pointer);

/* Structure */

struct _GIMarshallingTestsSimpleStruct {
    glong long_;
    gint8 int8;
};

typedef struct {
    GIMarshallingTestsSimpleStruct simple_struct;
} GIMarshallingTestsNestedStruct;

typedef struct {
    GIMarshallingTestsNestedStruct *pointer;
} GIMarshallingTestsNotSimpleStruct;


GIMarshallingTestsSimpleStruct *gi_marshalling_tests_simple_struct_returnv (void);

void gi_marshalling_tests_simple_struct_inv (GIMarshallingTestsSimpleStruct *struct_);

void gi_marshalling_tests_simple_struct_method (GIMarshallingTestsSimpleStruct *struct_);


typedef struct {
    glong long_;
} GIMarshallingTestsPointerStruct;

GType gi_marshalling_tests_pointer_struct_get_type (void) G_GNUC_CONST;

GIMarshallingTestsPointerStruct *gi_marshalling_tests_pointer_struct_returnv (void);

void gi_marshalling_tests_pointer_struct_inv (GIMarshallingTestsPointerStruct *struct_);

struct _GIMarshallingTestsBoxedStruct {
    glong long_;
    gchar *string_;
    GStrv g_strv;
};

GType gi_marshalling_tests_boxed_struct_get_type (void) G_GNUC_CONST;

GIMarshallingTestsBoxedStruct *gi_marshalling_tests_boxed_struct_new (void);

GIMarshallingTestsBoxedStruct *gi_marshalling_tests_boxed_struct_returnv (void);

void gi_marshalling_tests_boxed_struct_inv (GIMarshallingTestsBoxedStruct *struct_);

void gi_marshalling_tests_boxed_struct_out (GIMarshallingTestsBoxedStruct **struct_);

void gi_marshalling_tests_boxed_struct_inout (GIMarshallingTestsBoxedStruct **struct_);

typedef union {
    glong long_;
} GIMarshallingTestsUnion;

GType gi_marshalling_tests_union_get_type (void) G_GNUC_CONST;

GIMarshallingTestsUnion *gi_marshalling_tests_union_returnv (void);

void gi_marshalling_tests_union_inv (GIMarshallingTestsUnion *union_);

void gi_marshalling_tests_union_out (GIMarshallingTestsUnion **union_);

void gi_marshalling_tests_union_inout (GIMarshallingTestsUnion **union_);

void gi_marshalling_tests_union_method (GIMarshallingTestsUnion *union_);

 /* Object */

#define GI_MARSHALLING_TESTS_TYPE_OBJECT             (gi_marshalling_tests_object_get_type ())
#define GI_MARSHALLING_TESTS_OBJECT(obj)             (G_TYPE_CHECK_INSTANCE_CAST ((obj), GI_MARSHALLING_TESTS_TYPE_OBJECT, GIMarshallingTestsObject))
#define GI_MARSHALLING_TESTS_OBJECT_CLASS(klass)     (G_TYPE_CHECK_CLASS_CAST ((klass), GI_MARSHALLING_TESTS_TYPE_OBJECT, GIMarshallingTestsObjectClass))
#define GI_MARSHALLING_TESTS_IS_OBJECT(obj)          (G_TYPE_CHECK_INSTANCE_TYPE ((obj), GI_MARSHALLING_TESTS_TYPE_OBJECT))
#define GI_MARSHALLING_TESTS_IS_OBJECT_CLASS(klass)  (G_TYPE_CHECK_CLASS_TYPE ((klass), GI_MARSHALLING_TESTS_TYPE_OBJECT))
#define GI_MARSHALLING_TESTS_OBJECT_GET_CLASS(obj)   (G_TYPE_INSTANCE_GET_CLASS ((obj), GI_MARSHALLING_TESTS_TYPE_OBJECT, GIMarshallingTestsObjectClass))

typedef struct _GIMarshallingTestsObjectClass GIMarshallingTestsObjectClass;
typedef struct _GIMarshallingTestsObject GIMarshallingTestsObject;

typedef int (* GIMarshallingTestsCallbackIntInt) (int val, void *user_data);

struct _GIMarshallingTestsObjectClass
{
	GObjectClass parent_class;

    /**
     * GIMarshallingTestsObjectClass::method_int8_in:
     * @in: (in):
     */
    void (* method_int8_in) (GIMarshallingTestsObject *self, gint8 in);

    /**
     * GIMarshallingTestsObjectClass::method_int8_out:
     * @out: (out):
     */
    void (* method_int8_out) (GIMarshallingTestsObject *self, gint8 *out);

    /**
     * GIMarshallingTestsObjectClass::method_int8_arg_and_out_caller:
     * @out: (out caller-allocates):
     */
    void (* method_int8_arg_and_out_caller) (GIMarshallingTestsObject *self, gint8 arg, gint8 *out);

    /**
     * GIMarshallingTestsObjectClass::method_int8_arg_and_out_callee:
     * @out: (out):
     */
    void (* method_int8_arg_and_out_callee) (GIMarshallingTestsObject *self, gint8 arg, gint8 **out);

    /**
     * GIMarshallingTestsObjectClass::method_str_arg_out_ret:
     * @out: (out caller-allocates):
     *
     * Returns: (transfer none)
     */
    const gchar* (* method_str_arg_out_ret) (GIMarshallingTestsObject *self, const gchar* arg, guint *out);

    /**
     * GIMarshallingTestsObjectClass::method_with_default_implementation:
     * @in: (in):
     */
    void (* method_with_default_implementation) (GIMarshallingTestsObject *self, gint8 in);

    /**
     * GIMarshallingTestsObjectClass::method_deep_hierarchy:
     * @in: (in):
     */
    void (* method_deep_hierarchy) (GIMarshallingTestsObject *self, gint8 in);

    void (* vfunc_with_callback) (GIMarshallingTestsObject *self,
                                  GIMarshallingTestsCallbackIntInt callback,
                                  void *callback_data);

    /**
     * GIMarshallingTestsObjectClass::vfunc_return_value_only:
     */
    glong (* vfunc_return_value_only) (GIMarshallingTestsObject *self);

    /**
     * GIMarshallingTestsObjectClass::vfunc_one_out_parameter:
     * @a: (out):
     */
    void  (* vfunc_one_out_parameter) (GIMarshallingTestsObject *self, gfloat *a);

    /**
     * GIMarshallingTestsObjectClass::vfunc_multiple_out_parameters:
     * @a: (out):
     * @b: (out):
     */
    void  (* vfunc_multiple_out_parameters) (GIMarshallingTestsObject *self, gfloat *a, gfloat *b);

    /**
     * GIMarshallingTestsObjectClass::vfunc_caller_allocated_out_parameter:
     * @a: (out):
     */
    void  (* vfunc_caller_allocated_out_parameter) (GIMarshallingTestsObject *self, GValue *a);

    /**
     * GIMarshallingTestsObjectClass::vfunc_array_out_parameter:
     * @a: (out) (array zero-terminated=1):
     */
    void  (* vfunc_array_out_parameter) (GIMarshallingTestsObject *self, gfloat **a);

    /**
     * GIMarshallingTestsObjectClass::vfunc_return_value_and_one_out_parameter:
     * @a: (out):
     */
    glong (* vfunc_return_value_and_one_out_parameter) (GIMarshallingTestsObject *self, glong *a);

    /**
     * GIMarshallingTestsObjectClass::vfunc_return_value_and_multiple_out_parameters:
     * @a: (out):
     * @b: (out):
     */
    glong (* vfunc_return_value_and_multiple_out_parameters) (GIMarshallingTestsObject *self, glong *a, glong *b);

    /**
     * GIMarshallingTestsObjectClass::vfunc_meth_with_err:
     * @x:
     * @error: A #GError
     */
    gboolean (*vfunc_meth_with_err) (GIMarshallingTestsObject *object, gint x, GError **error);


    /**
     * GIMarshallingTestsObjectClass::vfunc_return_object_transfer_none:
     *
     * Returns: (transfer none)
     */
    GObject* (* vfunc_return_object_transfer_none) (GIMarshallingTestsObject *self);

    /**
     * GIMarshallingTestsObjectClass::vfunc_return_object_transfer_full:
     *
     * Returns: (transfer full)
     */
    GObject* (* vfunc_return_object_transfer_full) (GIMarshallingTestsObject *self);

    /**
     * GIMarshallingTestsObjectClass::vfunc_out_object_transfer_none:
     * @object: (out) (transfer none):
     */
    void (* vfunc_out_object_transfer_none) (GIMarshallingTestsObject *self, GObject **object);

    /**
     * GIMarshallingTestsObjectClass::vfunc_out_object_transfer_full:
     * @object: (out) (transfer full):
     */
    void (* vfunc_out_object_transfer_full) (GIMarshallingTestsObject *self, GObject **object);

    /**
     * GIMarshallingTestsObjectClass::vfunc_in_object_transfer_none:
     * @object: (in) (transfer none):
     */
    void (* vfunc_in_object_transfer_none) (GIMarshallingTestsObject *self, GObject *object);

    /**
     * GIMarshallingTestsObjectClass::vfunc_in_object_transfer_full:
     * @object: (in) (transfer full):
     */
    void (* vfunc_in_object_transfer_full) (GIMarshallingTestsObject *self, GObject *object);


};

struct _GIMarshallingTestsObject
{
	GObject parent_instance;

    gint int_;
};

GType gi_marshalling_tests_object_get_type (void) G_GNUC_CONST;
void gi_marshalling_tests_object_static_method (void);
void gi_marshalling_tests_object_method (GIMarshallingTestsObject *object);
void gi_marshalling_tests_object_overridden_method (GIMarshallingTestsObject *object);
GIMarshallingTestsObject *gi_marshalling_tests_object_new (gint int_);

void gi_marshalling_tests_object_method_array_in (GIMarshallingTestsObject *object, const gint *ints, gint length);
void gi_marshalling_tests_object_method_array_out (GIMarshallingTestsObject *object, gint **ints, gint *length);
void gi_marshalling_tests_object_method_array_inout (GIMarshallingTestsObject *object, gint **ints, gint *length);
const gint *gi_marshalling_tests_object_method_array_return (GIMarshallingTestsObject *object, gint *length);

void gi_marshalling_tests_object_method_int8_in (GIMarshallingTestsObject *object, gint8 in);
void gi_marshalling_tests_object_method_int8_out (GIMarshallingTestsObject *object, gint8 *out);
void gi_marshalling_tests_object_method_int8_arg_and_out_caller (GIMarshallingTestsObject *object, gint8 arg, gint8 *out);
void gi_marshalling_tests_object_method_int8_arg_and_out_callee (GIMarshallingTestsObject *object, gint8 arg, gint8 **out);
const gchar* gi_marshalling_tests_object_method_str_arg_out_ret (GIMarshallingTestsObject *object, const gchar* arg, guint *out);
void gi_marshalling_tests_object_method_with_default_implementation (GIMarshallingTestsObject *object, gint8 in);
void gi_marshalling_tests_object_method_variant_array_in (GIMarshallingTestsObject *object, GVariant **in, gsize n_in);

glong gi_marshalling_tests_object_vfunc_return_value_only (GIMarshallingTestsObject *self);
void gi_marshalling_tests_object_vfunc_one_out_parameter (GIMarshallingTestsObject *self, gfloat *a);
void gi_marshalling_tests_object_vfunc_multiple_out_parameters (GIMarshallingTestsObject *self, gfloat *a, gfloat *b);
void gi_marshalling_tests_object_vfunc_caller_allocated_out_parameter (GIMarshallingTestsObject *self, GValue *a);
void gi_marshalling_tests_object_vfunc_array_out_parameter (GIMarshallingTestsObject *self, gfloat **a);
glong gi_marshalling_tests_object_vfunc_return_value_and_one_out_parameter (GIMarshallingTestsObject *self, glong *a);
glong gi_marshalling_tests_object_vfunc_return_value_and_multiple_out_parameters (GIMarshallingTestsObject *self, glong *a, glong *b);
gboolean gi_marshalling_tests_object_vfunc_meth_with_error (GIMarshallingTestsObject *object, gint x, GError **error);

void gi_marshalling_tests_object_get_ref_info_for_vfunc_return_object_transfer_none (GIMarshallingTestsObject *self, guint *ref_count, gboolean *is_floating);
void gi_marshalling_tests_object_get_ref_info_for_vfunc_return_object_transfer_full (GIMarshallingTestsObject *self, guint *ref_count, gboolean *is_floating);
void gi_marshalling_tests_object_get_ref_info_for_vfunc_out_object_transfer_none (GIMarshallingTestsObject *self, guint *ref_count, gboolean *is_floating);
void gi_marshalling_tests_object_get_ref_info_for_vfunc_out_object_transfer_full (GIMarshallingTestsObject *self, guint *ref_count, gboolean *is_floating);
void gi_marshalling_tests_object_get_ref_info_for_vfunc_in_object_transfer_none (GIMarshallingTestsObject *self, GType type, guint *ref_count, gboolean *is_floating);
void gi_marshalling_tests_object_get_ref_info_for_vfunc_in_object_transfer_full (GIMarshallingTestsObject *self, GType type, guint *ref_count, gboolean *is_floating);

GIMarshallingTestsObject *gi_marshalling_tests_object_none_return (void);
GIMarshallingTestsObject *gi_marshalling_tests_object_full_return (void);

void gi_marshalling_tests_object_none_in (GIMarshallingTestsObject *object);
void gi_marshalling_tests_object_full_in (GIMarshallingTestsObject *object);

void gi_marshalling_tests_object_none_out (GIMarshallingTestsObject **object);
void gi_marshalling_tests_object_full_out (GIMarshallingTestsObject **object);

void gi_marshalling_tests_object_none_inout (GIMarshallingTestsObject **object);
void gi_marshalling_tests_object_full_inout (GIMarshallingTestsObject **object);
void gi_marshalling_tests_object_inout_same (GIMarshallingTestsObject **object);

void gi_marshalling_tests_object_int8_in (GIMarshallingTestsObject *object, gint8 in);
void gi_marshalling_tests_object_int8_out (GIMarshallingTestsObject *object, gint8 *out);

void gi_marshalling_tests_object_vfunc_with_callback (GIMarshallingTestsObject *object,
                                                      GIMarshallingTestsCallbackIntInt callback,
                                                      void *callback_data);
void gi_marshalling_tests_object_call_vfunc_with_callback (GIMarshallingTestsObject *object);

#define GI_MARSHALLING_TESTS_TYPE_SUB_OBJECT             (gi_marshalling_tests_sub_object_get_type ())
#define GI_MARSHALLING_TESTS_SUB_OBJECT(obj)             (G_TYPE_CHECK_INSTANCE_CAST ((obj), GI_MARSHALLING_TESTS_TYPE_SUB_OBJECT, GIMarshallingTestsSubObject))
#define GI_MARSHALLING_TESTS_SUB_OBJECT_CLASS(klass)     (G_TYPE_CHECK_CLASS_CAST ((klass), GI_MARSHALLING_TESTS_TYPE_SUB_OBJECT, GIMarshallingTestsSubObjectClass))
#define GI_MARSHALLING_TESTS_IS_SUB_OBJECT(obj)          (G_TYPE_CHECK_INSTANCE_TYPE ((obj), GI_MARSHALLING_TESTS_TYPE_SUB_OBJECT))
#define GI_MARSHALLING_TESTS_IS_SUB_OBJECT_CLASS(klass)  (G_TYPE_CHECK_CLASS_TYPE ((klass), GI_MARSHALLING_TESTS_TYPE_SUB_OBJECT))
#define GI_MARSHALLING_TESTS_SUB_OBJECT_GET_CLASS(obj)   (G_TYPE_INSTANCE_GET_CLASS ((obj), GI_MARSHALLING_TESTS_TYPE_SUB_OBJECT, GIMarshallingTestsSubObjectClass))

typedef struct _GIMarshallingTestsSubObjectClass GIMarshallingTestsSubObjectClass;
typedef struct _GIMarshallingTestsSubObject GIMarshallingTestsSubObject;

struct _GIMarshallingTestsSubObjectClass
{
	GIMarshallingTestsObjectClass parent_class;
};

struct _GIMarshallingTestsSubObject
{
	GIMarshallingTestsObject parent_instance;
};

GType gi_marshalling_tests_sub_object_get_type (void) G_GNUC_CONST;

void gi_marshalling_tests_sub_object_sub_method (GIMarshallingTestsSubObject *object);
void gi_marshalling_tests_sub_object_overwritten_method (GIMarshallingTestsSubObject *object);

#define GI_MARSHALLING_TESTS_TYPE_SUB_SUB_OBJECT             (gi_marshalling_tests_sub_sub_object_get_type ())
#define GI_MARSHALLING_TESTS_SUB_SUB_OBJECT(obj)             (G_TYPE_CHECK_INSTANCE_CAST ((obj), GI_MARSHALLING_TESTS_TYPE_SUB_SUB_OBJECT, GIMarshallingTestsSubSubObject))
#define GI_MARSHALLING_TESTS_SUB_SUB_OBJECT_CLASS(klass)     (G_TYPE_CHECK_CLASS_CAST ((klass), GI_MARSHALLING_TESTS_TYPE_SUB_SUB_OBJECT, GIMarshallingTestsSubSubObjectClass))
#define GI_MARSHALLING_TESTS_IS_SUB_SUB_OBJECT(obj)          (G_TYPE_CHECK_INSTANCE_TYPE ((obj), GI_MARSHALLING_TESTS_TYPE_SUB_SUB_OBJECT))
#define GI_MARSHALLING_TESTS_IS_SUB_SUB_OBJECT_CLASS(klass)  (G_TYPE_CHECK_CLASS_TYPE ((klass), GI_MARSHALLING_TESTS_TYPE_SUB_SUB_OBJECT))
#define GI_MARSHALLING_TESTS_SUB_SUB_OBJECT_GET_CLASS(obj)   (G_TYPE_INSTANCE_GET_CLASS ((obj), GI_MARSHALLING_TESTS_TYPE_SUB_SUB_OBJECT, GIMarshallingTestsSubSubObjectClass))

typedef struct _GIMarshallingTestsSubSubObjectClass GIMarshallingTestsSubSubObjectClass;
typedef struct _GIMarshallingTestsSubSubObject GIMarshallingTestsSubSubObject;

struct _GIMarshallingTestsSubSubObjectClass
{
	GIMarshallingTestsSubObjectClass parent_class;
};

struct _GIMarshallingTestsSubSubObject
{
	GIMarshallingTestsSubObject parent_instance;
};

GType gi_marshalling_tests_sub_sub_object_get_type (void) G_GNUC_CONST;

/* Interfaces */

#define GI_MARSHALLING_TESTS_TYPE_INTERFACE              (gi_marshalling_tests_interface_get_type ())
#define GI_MARSHALLING_TESTS_INTERFACE(object)           (G_TYPE_CHECK_INSTANCE_CAST ((object), GI_MARSHALLING_TESTS_TYPE_INTERFACE, GIMarshallingTestsInterface))
#define GI_MARSHALLING_TESTS_IS_INTERFACE(object)        (G_TYPE_CHECK_INSTANCE_TYPE ((object), GI_MARSHALLING_TESTS_TYPE_INTERFACE))
#define GI_MARSHALLING_TESTS_INTERFACE_GET_IFACE(obj)    (G_TYPE_INSTANCE_GET_INTERFACE ((obj), GI_MARSHALLING_TESTS_TYPE_INTERFACE, GIMarshallingTestsInterfaceIface))

typedef struct _GIMarshallingTestsInterface GIMarshallingTestsInterface;
typedef struct _GIMarshallingTestsInterfaceIface GIMarshallingTestsInterfaceIface;

struct _GIMarshallingTestsInterfaceIface {
    GTypeInterface base_iface;

    /**
     * GIMarshallingTestsInterfaceIface::test_int8_in:
     * @in: (in):
     */
    void (* test_int8_in) (GIMarshallingTestsInterface *self, gint8 in);
};

GType gi_marshalling_tests_interface_get_type (void) G_GNUC_CONST;

void gi_marshalling_tests_interface_test_int8_in (GIMarshallingTestsInterface *self, gint8 in);

void gi_marshalling_tests_test_interface_test_int8_in (GIMarshallingTestsInterface *test_iface, gint8 in);

/* GIMarshallingTestsInterface2 allows us testing vfunc clashes when a class'
   vfunc implementation ambiguously relates to its prototype */

#define GI_MARSHALLING_TESTS_TYPE_INTERFACE2              (gi_marshalling_tests_interface2_get_type ())
#define GI_MARSHALLING_TESTS_INTERFACE2(object)           (G_TYPE_CHECK_INSTANCE_CAST ((object), GI_MARSHALLING_TESTS_TYPE_INTERFACE2, GIMarshallingTestsInterface2))
#define GI_MARSHALLING_TESTS_IS_INTERFACE2(object)        (G_TYPE_CHECK_INSTANCE_TYPE ((object), GI_MARSHALLING_TESTS_TYPE_INTERFACE2))
#define GI_MARSHALLING_TESTS_INTERFACE2_GET_IFACE(obj)    (G_TYPE_INSTANCE_GET_INTERFACE ((obj), GI_MARSHALLING_TESTS_TYPE_INTERFACE2, GIMarshallingTestsInterface2Iface))

typedef struct _GIMarshallingTestsInterface2 GIMarshallingTestsInterface2;
typedef struct _GIMarshallingTestsInterface2Iface GIMarshallingTestsInterface2Iface;

struct _GIMarshallingTestsInterface2Iface {
    GTypeInterface base_iface;

    /**
     * GIMarshallingTestsInterface2Iface::test_int8_in:
     * @in: (in):
     */
    void (* test_int8_in) (GIMarshallingTestsInterface2 *self, gint8 in);
};

GType gi_marshalling_tests_interface2_get_type (void) G_GNUC_CONST;

/* GIMarshallingTestsInterface3 tests passing arrays of variants from C to @lang */

#define GI_MARSHALLING_TESTS_TYPE_INTERFACE3              (gi_marshalling_tests_interface3_get_type ())
#define GI_MARSHALLING_TESTS_INTERFACE3(object)           (G_TYPE_CHECK_INSTANCE_CAST ((object), GI_MARSHALLING_TESTS_TYPE_INTERFACE3, GIMarshallingTestsInterface3))
#define GI_MARSHALLING_TESTS_IS_INTERFACE3(object)        (G_TYPE_CHECK_INSTANCE_TYPE ((object), GI_MARSHALLING_TESTS_TYPE_INTERFACE3))
#define GI_MARSHALLING_TESTS_INTERFACE3_GET_IFACE(obj)    (G_TYPE_INSTANCE_GET_INTERFACE ((obj), GI_MARSHALLING_TESTS_TYPE_INTERFACE3, GIMarshallingTestsInterface3Iface))

typedef struct _GIMarshallingTestsInterface3 GIMarshallingTestsInterface3;
typedef struct _GIMarshallingTestsInterface3Iface GIMarshallingTestsInterface3Iface;

struct _GIMarshallingTestsInterface3Iface {
    GTypeInterface base_iface;

    /**
     * GIMarshallingTestsInterface3::test_variant_array_in:
     * @in: (in) (array length=n_in):
     */
    void (* test_variant_array_in) (GIMarshallingTestsInterface3 *self, GVariant **in, gsize n_in);
};

GType gi_marshalling_tests_interface3_get_type (void) G_GNUC_CONST;

void gi_marshalling_tests_interface3_test_variant_array_in (GIMarshallingTestsInterface3 *self, GVariant **in, gsize n_in);

/* Multiple output arguments */

void gi_marshalling_tests_int_out_out (gint *int0, gint *int1);
void gi_marshalling_tests_int_three_in_three_out(gint a, gint b, gint c,
                                                 gint *out0, gint *out1, gint *out2);
gint gi_marshalling_tests_int_return_out (gint *int_);


/* GError */

#define GI_MARSHALLING_TESTS_CONSTANT_GERROR_DOMAIN "gi-marshalling-tests-gerror-domain"
#define GI_MARSHALLING_TESTS_CONSTANT_GERROR_CODE 5
#define GI_MARSHALLING_TESTS_CONSTANT_GERROR_MESSAGE "gi-marshalling-tests-gerror-message"
#define GI_MARSHALLING_TESTS_CONSTANT_GERROR_DEBUG_MESSAGE "we got an error, life is shit"

void gi_marshalling_tests_gerror(GError **error);
void gi_marshalling_tests_gerror_array_in(gint *in_ints, GError **error);
void gi_marshalling_tests_gerror_out(GError **error, gchar **debug);
void gi_marshalling_tests_gerror_out_transfer_none(GError **err, const gchar **debug);
GError *gi_marshalling_tests_gerror_return(void);

/* GParamSpec */
void gi_marshalling_tests_param_spec_in_bool(const GParamSpec *param);
GParamSpec *gi_marshalling_tests_param_spec_return (void);
void gi_marshalling_tests_param_spec_out(GParamSpec **param);

/* Overrides */

#define GI_MARSHALLING_TESTS_OVERRIDES_CONSTANT 42


typedef struct {
    glong long_;
} GIMarshallingTestsOverridesStruct;

GType gi_marshalling_tests_overrides_struct_get_type (void) G_GNUC_CONST;

GIMarshallingTestsOverridesStruct *gi_marshalling_tests_overrides_struct_new (void);

glong gi_marshalling_tests_overrides_struct_method (GIMarshallingTestsOverridesStruct *struct_);

GIMarshallingTestsOverridesStruct *gi_marshalling_tests_overrides_struct_returnv (void);


#define GI_MARSHALLING_TESTS_TYPE_OVERRIDES_OBJECT             (gi_marshalling_tests_overrides_object_get_type ())
#define GI_MARSHALLING_TESTS_OVERRIDES_OBJECT(obj)             (G_TYPE_CHECK_INSTANCE_CAST ((obj), GI_MARSHALLING_TESTS_TYPE_OVERRIDES_OBJECT, GIMarshallingTestsOverridesObject))
#define GI_MARSHALLING_TESTS_OVERRIDES_OBJECT_CLASS(klass)     (G_TYPE_CHECK_CLASS_CAST ((klass), GI_MARSHALLING_TESTS_TYPE_OVERRIDES_OBJECT, GIMarshallingTestsOverridesObjectClass))
#define GI_MARSHALLING_TESTS_IS_OVERRIDES_OBJECT(obj)          (G_TYPE_CHECK_INSTANCE_TYPE ((obj), GI_MARSHALLING_TESTS_TYPE_OVERRIDES_OBJECT))
#define GI_MARSHALLING_TESTS_IS_OVERRIDES_OBJECT_CLASS(klass)  (G_TYPE_CHECK_CLASS_TYPE ((klass), GI_MARSHALLING_TESTS_TYPE_OVERRIDES_OBJECT))
#define GI_MARSHALLING_TESTS_OVERRIDES_OBJECT_GET_CLASS(obj)   (G_TYPE_INSTANCE_GET_CLASS ((obj), GI_MARSHALLING_TESTS_TYPE_OVERRIDES_OBJECT, GIMarshallingTestsOverridesObjectClass))

typedef struct _GIMarshallingTestsOverridesObjectClass GIMarshallingTestsOverridesObjectClass;
typedef struct _GIMarshallingTestsOverridesObject GIMarshallingTestsOverridesObject;

struct _GIMarshallingTestsOverridesObjectClass
{
    GObjectClass parent_class;
};

struct _GIMarshallingTestsOverridesObject
{
    GObject parent_instance;

    glong long_;
};

GType gi_marshalling_tests_overrides_object_get_type (void) G_GNUC_CONST;

GIMarshallingTestsOverridesObject *gi_marshalling_tests_overrides_object_new (void);

glong gi_marshalling_tests_overrides_object_method (GIMarshallingTestsOverridesObject *object);

GIMarshallingTestsOverridesObject *gi_marshalling_tests_overrides_object_returnv (void);

/* Properties Object */

#define GI_MARSHALLING_TESTS_TYPE_PROPERTIES_OBJECT (gi_marshalling_tests_properties_object_get_type ())
#define GI_MARSHALLING_TESTS_PROPERTIES_OBJECT(obj) (G_TYPE_CHECK_INSTANCE_CAST ((obj), GI_MARSHALLING_TESTS_TYPE_PROPERTIES_OBJECT, GIMarshallingTestsPropertiesObject))
#define GI_MARSHALLING_TESTS_PROPERTIES_OBJECT_CLASS(klass) (G_TYPE_CHECK_CLASS_CAST ((klass), GI_MARSHALLING_TESTS_TYPE_PROPERTIES_OBJECT, GIMarshallingTestsPropertiesObjectClass))
#define GI_MARSHALLING_TESTS_IS_PROPERTIES_OBJECT(obj) (G_TYPE_CHECK_INSTANCE_TYPE ((obj), GI_MARSHALLING_TESTS_TYPE_PROPERTIES_OBJECT))
#define GI_MARSHALLING_TESTS_IS_PROPERTIES_OBJECT_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE ((klass), GI_MARSHALLING_TESTS_TYPE_PROPERTIES_OBJECT))
#define GI_MARSHALLING_TESTS_PROPERTIES_OBJECT_GET_CLASS(obj) (G_TYPE_INSTANCE_GET_CLASS ((obj), GI_MARSHALLING_TESTS_TYPE_PROPERTIES_OBJECT, GIMarshallingTestsPropertiesObjectClass))

typedef struct _GIMarshallingTestsPropertiesObject GIMarshallingTestsPropertiesObject;
typedef struct _GIMarshallingTestsPropertiesObjectClass GIMarshallingTestsPropertiesObjectClass;

struct _GIMarshallingTestsPropertiesObject {
    GObject parent_instance;

    gboolean some_boolean;
    gchar some_char;
    guchar some_uchar;
    gint some_int;
    guint some_uint;
    glong some_long;
    gulong some_ulong;
    gint64 some_int64;
    guint64 some_uint64;
    gfloat some_float;
    gdouble some_double;
    gchar **some_strv;
    GIMarshallingTestsBoxedStruct* some_boxed_struct;
    GList* some_boxed_glist;
    GVariant *some_variant;
    GObject *some_object;
};

struct _GIMarshallingTestsPropertiesObjectClass {
    GObjectClass parent_class;
};

GType gi_marshalling_tests_properties_object_get_type (void) G_GNUC_CONST;

GIMarshallingTestsPropertiesObject *gi_marshalling_tests_properties_object_new (void);

#endif /* _GI_MARSHALLING_TESTS_H_ */
