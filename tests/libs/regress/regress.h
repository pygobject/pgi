#ifndef __GITESTTYPES_H__
#define __GITESTTYPES_H__

#ifndef _GI_DISABLE_CAIRO
#include <cairo-gobject.h>
#endif
#include <glib-object.h>
#include <gio/gio.h>
#include <time.h>

void regress_set_abort_on_error (gboolean abort_on_error);

/* basic types */
gboolean regress_test_boolean (gboolean in);
gboolean regress_test_boolean_true (gboolean in);
gboolean regress_test_boolean_false (gboolean in);
gint8 regress_test_int8 (gint8 in);
guint8 regress_test_uint8 (guint8 in);
gint16 regress_test_int16 (gint16 in);
guint16 regress_test_uint16 (guint16 in);
gint32 regress_test_int32 (gint32 in);
guint32 regress_test_uint32 (guint32 in);
gint64 regress_test_int64 (gint64 in);
guint64 regress_test_uint64 (guint64 in);
gshort regress_test_short (gshort in);
gushort regress_test_ushort (gushort in);
gint regress_test_int (gint in);
guint regress_test_uint (guint in);
glong regress_test_long (glong in);
gulong regress_test_ulong (gulong in);
gssize regress_test_ssize (gssize in);
gsize regress_test_size (gsize in);
gfloat regress_test_float (gfloat in);
gdouble regress_test_double (gdouble in);
gunichar regress_test_unichar (gunichar in);
time_t regress_test_timet (time_t in);
GType regress_test_gtype (GType in);

/* utf8 */
const char *regress_test_utf8_const_return (void);
char *regress_test_utf8_nonconst_return (void);
void regress_test_utf8_const_in (const char *in);
void regress_test_utf8_out (char **out);
void regress_test_utf8_inout (char **inout);
GSList *regress_test_filename_return (void);
void regress_test_utf8_null_in (char *in);
void regress_test_utf8_null_out (char **char_out);

/* in arguments after out arguments */
void regress_test_int_out_utf8 (int *length, const char *in);

/* multiple output arguments */
void regress_test_multi_double_args (gdouble in, gdouble *one, gdouble *two);
void regress_test_utf8_out_out (char **out0, char **out1);
char *regress_test_utf8_out_nonconst_return (char **out);

/* non-basic-types */
/* array */
gboolean regress_test_strv_in (char **arr);
int regress_test_array_int_in (int n_ints, int *ints);
void regress_test_array_int_out (int *n_ints, int **ints);
void regress_test_array_int_inout (int *n_ints, int **ints);
int regress_test_array_gint8_in (int n_ints, gint8 *ints);
int regress_test_array_gint16_in (int n_ints, gint16 *ints);
gint32 regress_test_array_gint32_in (int n_ints, gint32 *ints);
gint64 regress_test_array_gint64_in (int n_ints, gint64 *ints);
char *regress_test_array_gtype_in (int n_types, GType *types);
char **regress_test_strv_out_container (void);
char **regress_test_strv_out (void);
const char * const * regress_test_strv_out_c (void);
void   regress_test_strv_outarg (char ***retp);
int regress_test_array_fixed_size_int_in (int *ints);
void regress_test_array_fixed_size_int_out (int **ints);
int *regress_test_array_fixed_size_int_return (void);

/* transfer tests */
int *regress_test_array_int_full_out(int *len);
int *regress_test_array_int_none_out(int *len);
void regress_test_array_int_null_in (int *arr, int len);
void regress_test_array_int_null_out (int **arr, int *len);

/* interface */
/* GList */
const GList *regress_test_glist_nothing_return (void);
GList *regress_test_glist_nothing_return2 (void);
GList *regress_test_glist_container_return (void);
GList *regress_test_glist_everything_return (void);
void regress_test_glist_nothing_in (const GList *in);
void regress_test_glist_nothing_in2 (GList *in);
void regress_test_glist_null_in(GSList *in);
void regress_test_glist_null_out(GSList **out_list);

/* GSList */
const GSList *regress_test_gslist_nothing_return (void);
GSList *regress_test_gslist_nothing_return2 (void);
GSList *regress_test_gslist_container_return (void);
GSList *regress_test_gslist_everything_return (void);
void regress_test_gslist_nothing_in (const GSList *in);
void regress_test_gslist_nothing_in2 (GSList *in);
void regress_test_gslist_null_in(GSList *in);
void regress_test_gslist_null_out(GSList **out_list);

/* GHashTable */
const GHashTable *regress_test_ghash_null_return (void);
const GHashTable *regress_test_ghash_nothing_return (void);
GHashTable *regress_test_ghash_nothing_return2 (void);
GHashTable *regress_test_ghash_gvalue_return (void);
void regress_test_ghash_gvalue_in (GHashTable *hash);
GHashTable *regress_test_ghash_container_return (void);
GHashTable *regress_test_ghash_everything_return (void);
void regress_test_ghash_null_in (const GHashTable *in);
void regress_test_ghash_null_out (const GHashTable **out);
void regress_test_ghash_nothing_in (const GHashTable *in);
void regress_test_ghash_nothing_in2 (GHashTable *in);
GHashTable *regress_test_ghash_nested_everything_return (void);
GHashTable *regress_test_ghash_nested_everything_return2 (void);

/* GPtrArray */
GPtrArray *regress_test_garray_container_return (void);
GPtrArray *regress_test_garray_full_return (void);

/* error? */

/* closure */
int regress_test_closure (GClosure *closure);
int regress_test_closure_one_arg (GClosure *closure, int arg);
GVariant *regress_test_closure_variant (GClosure *closure, GVariant* arg);

/* value */
int regress_test_int_value_arg(const GValue *v);
const GValue *regress_test_value_return(int i);

/* foreign structs */
#ifndef _GI_DISABLE_CAIRO
cairo_t *regress_test_cairo_context_full_return (void);
void regress_test_cairo_context_none_in (cairo_t *context);

cairo_surface_t *regress_test_cairo_surface_none_return (void);
cairo_surface_t *regress_test_cairo_surface_full_return (void);
void regress_test_cairo_surface_none_in (cairo_surface_t *surface);
void regress_test_cairo_surface_full_out (cairo_surface_t **surface);
#endif

/* versioning (deprecated, since, stability) */
void regress_test_versioning (void);

GVariant *regress_test_gvariant_i (void);
GVariant *regress_test_gvariant_s (void);
GVariant *regress_test_gvariant_asv (void);
GVariant *regress_test_gvariant_v (void);
GVariant *regress_test_gvariant_as (void);

/* enums / flags */

#define NUM_REGRESS_FOO

/**
 * RegressTestEnum:
 * @REGRESS_TEST_VALUE1: value 1
 * @REGRESS_TEST_VALUE2: value 2
 *
 * By purpose, not all members have documentation
 */
typedef enum
{
  REGRESS_TEST_VALUE1,
  REGRESS_TEST_VALUE2,
  REGRESS_TEST_VALUE3 = -1,
  REGRESS_TEST_VALUE4 = '0'
} RegressTestEnum;

typedef enum
{
  REGRESS_TEST_UNSIGNED_VALUE1 = 1,
  REGRESS_TEST_UNSIGNED_VALUE2 = 0x80000000
} RegressTestEnumUnsigned;

typedef enum
{
  REGRESS_TEST_FLAG1 = 1 << 0,
  REGRESS_TEST_FLAG2 = 1 << 1,
  REGRESS_TEST_FLAG3 = 1 << 2,
} RegressTestFlags;

GType regress_test_enum_get_type (void) G_GNUC_CONST;
#define REGRESS_TEST_TYPE_ENUM (regress_test_enum_get_type ())
GType regress_test_enum_unsigned_get_type (void) G_GNUC_CONST;
#define REGRESS_TEST_TYPE_ENUM_UNSIGNED (regress_test_enum_unsigned_get_type ())
GType regress_test_flags_get_type (void) G_GNUC_CONST;
#define REGRESS_TEST_TYPE_FLAGS (regress_test_flags_get_type ())

typedef enum
{
  REGRESS_TEST_REFERENCE_0 = 2 + 2,
  REGRESS_TEST_REFERENCE_1 = 1 + 1,
  REGRESS_TEST_REFERENCE_2 = 6 * 9,
  REGRESS_TEST_REFERENCE_3 = REGRESS_TEST_REFERENCE_1 + REGRESS_TEST_REFERENCE_1,
  REGRESS_TEST_REFERENCE_4 = REGRESS_TEST_REFERENCE_2 * REGRESS_TEST_REFERENCE_3,
  REGRESS_TEST_REFERENCE_5 = ~REGRESS_TEST_REFERENCE_4,
} RegressTestReferenceEnum;

/* this is not registered with GType */
typedef enum
{
  REGRESS_TEST_EVALUE1,
  REGRESS_TEST_EVALUE2 = 42,
  REGRESS_TEST_EVALUE3 = '0'
} RegressTestEnumNoGEnum;

const gchar * regress_test_enum_param(RegressTestEnum e);
const gchar * regress_test_unsigned_enum_param(RegressTestEnumUnsigned e);

void regress_global_get_flags_out (RegressTestFlags *v);

/* error domains */

typedef enum
{
  REGRESS_TEST_ERROR_CODE1 = 1,
  REGRESS_TEST_ERROR_CODE2 = 2,
  REGRESS_TEST_ERROR_CODE3 = 3
} RegressTestError;

GType regress_test_error_get_type (void);
GQuark regress_test_error_quark (void);

/* Test weird names, with and without
   c_symbol_prefix given by a GType
*/
typedef enum
{
  REGRESS_TEST_ABC_ERROR_CODE1 = 1,
  REGRESS_TEST_ABC_ERROR_CODE2 = 2,
  REGRESS_TEST_ABC_ERROR_CODE3 = 3
} RegressTestABCError;

GType regress_test_abc_error_get_type (void);
GQuark regress_test_abc_error_quark (void);

typedef enum
{
  REGRESS_TEST_OTHER_ERROR_CODE1 = 1,
  REGRESS_TEST_OTHER_ERROR_CODE2 = 2,
  REGRESS_TEST_OTHER_ERROR_CODE3 = 3
} RegressTestOtherError;

/* This returns a GType for RegressTestOtherError.
   The difference is intentional, although it
   is mainly meant for capitalization problems.
*/
GType regress_test_unconventional_error_get_type (void);
GQuark regress_test_unconventional_error_quark (void);

typedef enum
{
  REGRESS_TEST_DEF_ERROR_CODE0 = 0,
  REGRESS_TEST_DEF_ERROR_CODE1 = 1,
  REGRESS_TEST_DEF_ERROR_CODE2 = 2
} RegressTestDEFError;

GQuark regress_test_def_error_quark (void);

/* the scanner used to have problem
   with two uppercase letter right after
   the identifier prefix, that's why
   we break the RegressTest convention */
typedef enum
{
  REGRESS_ATEST_ERROR_CODE0 = 0,
  REGRESS_ATEST_ERROR_CODE1 = 1,
  REGRESS_ATEST_ERROR_CODE2 = 2
} RegressATestError;

GQuark regress_atest_error_quark (void);


/* constants */

#define REGRESS_NEGATIVE_INT_CONSTANT -42
#define REGRESS_INT_CONSTANT 4422
#define REGRESS_DOUBLE_CONSTANT 44.22
#define REGRESS_STRING_CONSTANT "Some String"
#define REGRESS_Mixed_Case_Constant 4423
#define REGRESS_G_GINT64_CONSTANT (G_GINT64_CONSTANT (1000))
#define REGRESS_GUINT64_CONSTANT ((guint64) -1)

typedef guint64 RegressTestTypeGUInt64;
#define REGRESS_GUINT64_CONSTANTA ((RegressTestTypeGUInt64) -1)

/* structures */
typedef struct _RegressTestStructA RegressTestStructA;
typedef struct _RegressTestStructB RegressTestStructB;
typedef struct _RegressTestStructC RegressTestStructC;
typedef struct _RegressTestStructD RegressTestStructD;
typedef struct _RegressTestStructF RegressTestStructF;

struct _RegressTestStructA
{
  gint some_int;
  gint8 some_int8;
  gdouble some_double;
  RegressTestEnum some_enum;
};

void regress_test_struct_a_clone (RegressTestStructA *a,
				  RegressTestStructA *a_out);
void regress_test_struct_a_parse (RegressTestStructA *a_out, const gchar *string);

struct _RegressTestStructB
{
  gint8 some_int8;
  RegressTestStructA nested_a;
};

void regress_test_struct_b_clone (RegressTestStructB *b,
			  RegressTestStructB *b_out);

/* This one has a non-basic member */
struct _RegressTestStructC
{
  gint another_int;
  GObject *obj;
};

/* This one has annotated fields */
/**
 * RegressTestStructD:
 * @array1: (array zero-terminated=1):
 * @array2: (array zero-terminated=1) (element-type RegressTestObj):
 * @field: (type RegressTestObj):
 * @list: (element-type RegressTestObj):
 * @garray: (element-type RegressTestObj):
 * @ref_count:
 */
struct _RegressTestStructD
{
  RegressTestStructA **array1;
  gpointer            *array2;
  gpointer             field;
  GList               *list;
  GPtrArray           *garray;
};

/* This one has an array of anonymous unions, inspired by GValue */
struct RegressTestStructE
{
  GType some_type;
  union {
    gint	v_int;
    guint	v_uint;
    glong	v_long;
    gulong	v_ulong;
    gint64      v_int64;
    guint64     v_uint64;
    gfloat	v_float;
    gdouble	v_double;
    gpointer	v_pointer;
  } some_union[2];
};

/* This one has members with const or volatile modifiers. */
struct _RegressTestStructF
{
  volatile gint   ref_count;
  const gint     *data1;
  const gint     *const data2;
  const gint     *const *const data3;
  const gint    **const* data4;
  volatile gint  *const data5;
  const gint     *volatile data6;
};

/* plain-old-data boxed types */
typedef struct _RegressTestSimpleBoxedA RegressTestSimpleBoxedA;
typedef struct _RegressTestSimpleBoxedB RegressTestSimpleBoxedB;

struct _RegressTestSimpleBoxedA
{
  gint some_int;
  gint8 some_int8;
  gdouble some_double;
  RegressTestEnum some_enum;
};

/* Intentionally uses _get_gtype */
GType                   regress_test_simple_boxed_a_get_gtype     (void);
RegressTestSimpleBoxedA *regress_test_simple_boxed_a_copy         (RegressTestSimpleBoxedA *a);
gboolean                regress_test_simple_boxed_a_equals       (RegressTestSimpleBoxedA *a,
                                                          RegressTestSimpleBoxedA *other_a);
const RegressTestSimpleBoxedA *regress_test_simple_boxed_a_const_return (void);


struct _RegressTestSimpleBoxedB
{
  gint8 some_int8;
  RegressTestSimpleBoxedA nested_a;
};

GType             regress_test_simple_boxed_b_get_type (void);
RegressTestSimpleBoxedB *regress_test_simple_boxed_b_copy     (RegressTestSimpleBoxedB *b);

/* opaque boxed */
#define REGRESS_TEST_TYPE_BOXED (regress_test_boxed_get_type())

typedef struct _RegressTestBoxed RegressTestBoxed;
typedef struct _RegressTestBoxedPrivate RegressTestBoxedPrivate;

struct _RegressTestBoxed
{
  gint8 some_int8;
  RegressTestSimpleBoxedA nested_a;

  RegressTestBoxedPrivate *priv;
};

GType      regress_test_boxed_get_type (void);
RegressTestBoxed *regress_test_boxed_new      (void);
RegressTestBoxed *regress_test_boxed_new_alternative_constructor1  (int i);
RegressTestBoxed *regress_test_boxed_new_alternative_constructor2  (int i, int j);
RegressTestBoxed *regress_test_boxed_new_alternative_constructor3  (char *s);

RegressTestBoxed *regress_test_boxed_copy     (RegressTestBoxed *boxed);
gboolean   regress_test_boxed_equals   (RegressTestBoxed *boxed,
					RegressTestBoxed *other);

typedef struct _RegressTestBoxedB RegressTestBoxedB;

struct _RegressTestBoxedB
{
  gint8 some_int8;
  glong some_long;
};

GType regress_test_boxed_b_get_type (void);
RegressTestBoxedB *regress_test_boxed_b_new (gint8 some_int8, glong some_long);
RegressTestBoxedB *regress_test_boxed_b_copy (RegressTestBoxedB *boxed);

typedef struct _RegressTestBoxedC RegressTestBoxedC;

struct _RegressTestBoxedC
{
  guint refcount;
  guint another_thing;
};

GType regress_test_boxed_c_get_type (void);
RegressTestBoxedC *regress_test_boxed_c_new (void);

typedef struct _RegressTestBoxedD RegressTestBoxedD;

GType regress_test_boxed_d_get_type (void);

RegressTestBoxedD *regress_test_boxed_d_new (const char *a_string, int a_int);
RegressTestBoxedD *regress_test_boxed_d_copy (RegressTestBoxedD *boxed);
void regress_test_boxed_d_free (RegressTestBoxedD *boxed);

int regress_test_boxed_d_get_magic (RegressTestBoxedD *boxed);

/* gobject */
#define REGRESS_TEST_TYPE_OBJ              (regress_test_obj_get_type ())
#define REGRESS_TEST_OBJECT(object)        (G_TYPE_CHECK_INSTANCE_CAST ((object), REGRESS_TEST_TYPE_OBJ, RegressTestObj))
#define REGRESS_TEST_IS_OBJECT(object)     (G_TYPE_CHECK_INSTANCE_TYPE ((object), REGRESS_TEST_TYPE_OBJ))
#define REGRESS_TEST_OBJ_GET_CLASS(obj)    (G_TYPE_INSTANCE_GET_CLASS ((obj), REGRESS_TEST_TYPE_OBJ, RegressTestObjClass))

typedef struct _RegressTestObj          RegressTestObj;
typedef struct _RegressTestObjClass     RegressTestObjClass;

/**
 * RegressTestObj:
 * @bare: (allow-none):
 */
struct _RegressTestObj
{
  GObject parent_instance;

  GObject *bare;
  RegressTestBoxed *boxed;
  GHashTable *hash_table;
  GList *list;
  gint8 some_int8;
  float some_float;
  double some_double;
  char* string;
  GType gtype;
};

struct _RegressTestObjClass
{
  GObjectClass parent_class;

  int (*matrix) (RegressTestObj *obj, const char *somestr);

  /**
   * RegressTestObjClass::allow_none_vfunc:
   * @two: (allow-none): Another object
   */
  void (*allow_none_vfunc) (RegressTestObj *obj, RegressTestObj *two);

  guint test_signal;
  guint test_signal_with_static_scope_arg;

  /* Should be replaced with simple "gpointer" and not be callback */
  void (*_regress_reserved1) (void);
  void (*_regress_reserved2) (void);
};

GType      regress_test_obj_get_type (void);
RegressTestObj*   regress_test_obj_new (RegressTestObj *obj);
RegressTestObj*   regress_constructor (void);
RegressTestObj*   regress_test_obj_new_from_file (const char *x, GError **error);
void       regress_test_obj_set_bare (RegressTestObj *obj, GObject *bare);
void       regress_test_obj_emit_sig_with_obj (RegressTestObj *obj);
void       regress_test_obj_emit_sig_with_foreign_struct (RegressTestObj *obj);
void       regress_test_obj_emit_sig_with_int64 (RegressTestObj *obj);
void       regress_test_obj_emit_sig_with_uint64 (RegressTestObj *obj);
int        regress_test_obj_instance_method (RegressTestObj *obj);
double     regress_test_obj_static_method (int x);
void       regress_forced_method (RegressTestObj *obj);

void regress_test_array_fixed_out_objects (RegressTestObj ***objs);

void regress_test_obj_torture_signature_0 (RegressTestObj    *obj,
                                   int        x,
                                   double     *y,
                                   int        *z,
                                   const char *foo,
                                   int        *q,
                                   guint       m);
gboolean regress_test_obj_torture_signature_1 (RegressTestObj    *obj,
                                       int        x,
                                       double     *y,
                                       int        *z,
                                       const char *foo,
                                       int        *q,
                                       guint       m,
                                       GError    **error);

gboolean regress_test_obj_skip_return_val (RegressTestObj *obj,
                                           gint            a,
                                           gint           *out_b,
                                           gdouble         c,
                                           gint           *inout_d,
                                           gint           *out_sum,
                                           gint            num1,
                                           gint            num2,
                                           GError        **error);

gboolean regress_test_obj_skip_return_val_no_out (RegressTestObj *obj,
                                                  gint            a,
                                                  GError        **error);

gboolean regress_test_obj_skip_param (RegressTestObj *obj,
                                      gint            a,
                                      gint           *out_b,
                                      gdouble         c,
                                      gint           *inout_d,
                                      gint           *out_sum,
                                      gint            num1,
                                      gint            num2,
                                      GError        **error);

gboolean regress_test_obj_skip_out_param (RegressTestObj *obj,
                                          gint            a,
                                          gint           *out_b,
                                          gdouble         c,
                                          gint           *inout_d,
                                          gint           *out_sum,
                                          gint            num1,
                                          gint            num2,
                                          GError        **error);

gboolean regress_test_obj_skip_inout_param (RegressTestObj *obj,
                                            gint            a,
                                            gint           *out_b,
                                            gdouble         c,
                                            gint           *inout_d,
                                            gint           *out_sum,
                                            gint            num1,
                                            gint            num2,
                                            GError        **error);

/* virtual */
int        regress_test_obj_do_matrix (RegressTestObj *obj, const char *somestr);

void regress_func_obj_null_in (RegressTestObj *obj);
void regress_test_obj_null_out (RegressTestObj **obj);

/* inheritance */
#define REGRESS_TEST_TYPE_SUB_OBJ           (regress_test_sub_obj_get_type ())
#define REGRESS_TEST_SUB_OBJECT(object)     (G_TYPE_CHECK_INSTANCE_CAST ((object), REGRESS_TEST_TYPE_SUB_OBJ, RegressTestSubObj))
#define REGRESS_TEST_IS_SUB_OBJECT(object)  (G_TYPE_CHECK_INSTANCE_TYPE ((object), REGRESS_TEST_TYPE_SUB_OBJ))
#define REGRESS_TEST_SUB_OBJ_GET_CLASS(obj) (G_TYPE_INSTANCE_GET_CLASS ((obj), REGRESS_TEST_TYPE_SUB_OBJ, RegressTestSubObjClass))

typedef struct _RegressTestSubObj         RegressTestSubObj;
typedef struct _RegressTestSubObjClass    RegressTestSubObjClass;

struct _RegressTestSubObj
{
  RegressTestObj parent_instance;
};

struct _RegressTestSubObjClass
{
  RegressTestObjClass parent_class;
};

GType       regress_test_sub_obj_get_type (void);
RegressTestObj* regress_test_sub_obj_new (void);
void        regress_test_sub_obj_unset_bare (RegressTestSubObj *obj);
int         regress_test_sub_obj_instance_method (RegressTestSubObj *obj);

/* fundamental object */
#define REGRESS_TEST_TYPE_FUNDAMENTAL_OBJECT            (regress_test_fundamental_object_get_type())
#define REGRESS_TEST_IS_FUNDAMENTAL_OBJECT(obj)         (G_TYPE_CHECK_INSTANCE_TYPE ((obj), REGRESS_TEST_TYPE_FUNDAMENTAL_OBJECT))
#define REGRESS_TEST_IS_FUNDAMENTAL_OBJECT_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE ((klass), REGRESS_TEST_TYPE_FUNDAMENTAL_OBJECT))
#define REGRESS_TEST_FUNDAMENTAL_OBJECT_GET_CLASS(obj)  (G_TYPE_INSTANCE_GET_CLASS ((obj), REGRESS_TEST_TYPE_FUNDAMENTAL_OBJECT, RegressTestFundamentalObjectClass))
#define REGRESS_TEST_FUNDAMENTAL_OBJECT(obj)            (G_TYPE_CHECK_INSTANCE_CAST ((obj), REGRESS_TEST_TYPE_FUNDAMENTAL_OBJECT, RegressTestFundamentalObject))
#define REGRESS_TEST_FUNDAMENTAL_OBJECT_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST ((klass), REGRESS_TEST_TYPE_FUNDAMENTAL_OBJECT, RegressTestFundamentalObjectClass))
#define REGRESS_TEST_FUNDAMENTAL_OBJECT_CAST(obj)       ((RegressTestFundamentalObject*)(obj))

typedef struct _RegressTestFundamentalObject RegressTestFundamentalObject;
typedef struct _RegressTestFundamentalObjectClass RegressTestFundamentalObjectClass;
/**
 * RegressTestFundamentalObjectCopyFunction:
 *
 * Returns: (transfer full):
 */
typedef RegressTestFundamentalObject * (*RegressTestFundamentalObjectCopyFunction) (const RegressTestFundamentalObject *obj);
typedef void (*RegressTestFundamentalObjectFinalizeFunction) (RegressTestFundamentalObject *obj);


struct _RegressTestFundamentalObject {
  GTypeInstance instance;
  gint refcount;
  guint flags;
};

struct _RegressTestFundamentalObjectClass {
  GTypeClass type_class;

  RegressTestFundamentalObjectCopyFunction copy;
  RegressTestFundamentalObjectFinalizeFunction finalize;
};

GType 		       regress_test_fundamental_object_get_type (void);
RegressTestFundamentalObject* regress_test_fundamental_object_ref      (RegressTestFundamentalObject *fundamental_object);
void 		       regress_test_fundamental_object_unref 	(RegressTestFundamentalObject *fundamental_object);

#define REGRESS_TEST_VALUE_HOLDS_FUNDAMENTAL_OBJECT(value)  (G_VALUE_HOLDS(value, REGRESS_TEST_TYPE_FUNDAMENTAL_OBJECT))

void 		       regress_test_value_set_fundamental_object (GValue *value, RegressTestFundamentalObject *fundamental_object);
RegressTestFundamentalObject* regress_test_value_get_fundamental_object (const GValue *value);

typedef struct _RegressTestFundamentalSubObject RegressTestFundamentalSubObject;
typedef struct _RegressTestFundamentalSubObjectClass RegressTestFundamentalSubObjectClass;

struct _RegressTestFundamentalSubObject
{
  RegressTestFundamentalObject fundamental_object;
  char *data;
};

struct _RegressTestFundamentalSubObjectClass {
  RegressTestFundamentalObjectClass fundamental_object_class;
};

GType regress_test_fundamental_sub_object_get_type(void);

RegressTestFundamentalSubObject *
regress_test_fundamental_sub_object_new (const char *data);

/* callback */
typedef void (*RegressTestSimpleCallback) (void);
typedef int (*RegressTestCallback) (void);
typedef int (*RegressTestCallbackUserData) (gpointer user_data);
/**
 * RegressTestCallbackHashtable:
 * @data: (element-type utf8 gint): a hash table; will be modified
 */
typedef void (*RegressTestCallbackHashtable) (GHashTable *data);
typedef void (*RegressTestCallbackGError) (const GError *error);
/**
 * RegressTestCallbackOwnedGError:
 * @error: (transfer full): GError instance; must be freed by the callback
 */
typedef void (*RegressTestCallbackOwnedGError) (GError *error);
/**
 * RegressTestCallbackFull:
 * @foo: the investment rate
 * @bar: how much money
 * @path: (type filename): Path to file
 */
typedef int (*RegressTestCallbackFull) (int foo, double bar, char *path);
/**
 * RegressTestCallbackArray:
 * @one: (array length=one_length):
 * @one_length:
 * @two: (array length=two_length) (element-type utf8):
 * @two_length:
 */
typedef int (*RegressTestCallbackArray) (int *one, gsize one_length, const char** two, int two_length);

void regress_test_simple_callback (RegressTestSimpleCallback callback);
int regress_test_callback (RegressTestCallback callback);
int regress_test_multi_callback (RegressTestCallback callback);
int regress_test_array_callback (RegressTestCallbackArray callback);
int regress_test_callback_user_data (RegressTestCallbackUserData callback,
                             gpointer user_data);
int regress_test_callback_destroy_notify (RegressTestCallbackUserData callback,
                                  gpointer user_data,
                                  GDestroyNotify notify);
int regress_test_callback_destroy_notify_no_user_data (RegressTestCallbackUserData callback,
                                  GDestroyNotify notify);
int regress_test_callback_thaw_notifications (void);

void regress_test_callback_async (RegressTestCallbackUserData callback, gpointer user_data);
int regress_test_callback_thaw_async (void);

void regress_test_async_ready_callback (GAsyncReadyCallback callback);

void regress_test_obj_instance_method_callback (RegressTestObj *obj, RegressTestCallback callback);
void regress_test_obj_static_method_callback (RegressTestCallback callback);
RegressTestObj *regress_test_obj_new_callback (RegressTestCallbackUserData callback,
                                gpointer user_data,
                                GDestroyNotify notify);
void regress_test_hash_table_callback (GHashTable *data, RegressTestCallbackHashtable callback);
void regress_test_gerror_callback (RegressTestCallbackGError callback);
void regress_test_null_gerror_callback (RegressTestCallbackGError callback);
void regress_test_owned_gerror_callback (RegressTestCallbackOwnedGError callback);

void regress_test_skip_unannotated_callback (RegressTestCallback callback);

typedef struct _RegressTestInterface RegressTestInterface;

/* interface */
#define REGRESS_TEST_TYPE_INTERFACE              (regress_test_interface_get_type ())
#define REGRESS_TEST_INTERFACE(object)           (G_TYPE_CHECK_INSTANCE_CAST ((object), REGRESS_TEST_TYPE_INTERFACE, RegressTestInterface))
#define REGRESS_TEST_IS_INTERFACE(object)        (G_TYPE_CHECK_INSTANCE_TYPE ((object), REGRESS_TEST_TYPE_INTERFACE))
#define REGRESS_TEST_INTERFACE_GET_IFACE(obj)    (G_TYPE_INSTANCE_GET_INTERFACE ((obj), REGRESS_TEST_TYPE_INTERFACE, RegressTestInterfaceIface))

typedef struct _RegressTestInterfaceIface RegressTestInterfaceIface;

struct _RegressTestInterfaceIface {
    GTypeInterface base_iface;
};

GType regress_test_interface_get_type (void) G_GNUC_CONST;

/* gobject with non-standard prefix */
#define REGRESS_TEST_TYPE_WI_802_1X              (regress_test_wi_802_1x_get_type ())
#define REGRESS_TEST_WI_802_1X(object)        (G_TYPE_CHECK_INSTANCE_CAST ((object), REGRESS_TEST_TYPE_WI_802_1X, RegressTestWi8021x))
#define REGRESS_TEST_IS_WI_802_1X(object)     (G_TYPE_CHECK_INSTANCE_TYPE ((object), REGRESS_TEST_TYPE_WI_802_1X))
#define REGRESS_TEST_WI_802_1X_GET_CLASS(obj)    (G_TYPE_INSTANCE_GET_CLASS ((obj), REGRESS_TEST_TYPE_WI_802_1X, RegressTestWi8021xClass))

typedef struct
{
  GObject parent_instance;

  gboolean testbool;
} RegressTestWi8021x;

typedef struct
{
  GObjectClass parent_class;
} RegressTestWi8021xClass;

GType        regress_test_wi_802_1x_get_type (void);
RegressTestWi8021x* regress_test_wi_802_1x_new (void);
gboolean     regress_test_wi_802_1x_get_testbool (RegressTestWi8021x *obj);
void         regress_test_wi_802_1x_set_testbool (RegressTestWi8021x *obj, gboolean v);
int          regress_test_wi_802_1x_static_method (int x);

/* floating gobject */
#define REGRESS_TEST_TYPE_FLOATING           (regress_test_floating_get_type ())
#define REGRESS_TEST_FLOATING(object)        (G_TYPE_CHECK_INSTANCE_CAST ((object), REGRESS_TEST_TYPE_FLOATING, RegressTestFloating))
#define REGRESS_TEST_IS_FLOATING(object)     (G_TYPE_CHECK_INSTANCE_TYPE ((object), REGRESS_TEST_TYPE_FLOATING))
#define REGRESS_TEST_FLOATING_GET_CLASS(obj) (G_TYPE_INSTANCE_GET_CLASS ((obj), REGRESS_TEST_TYPE_FLOATING, RegressTestFloatingClass))

typedef struct
{
  GInitiallyUnowned parent_instance;
} RegressTestFloating;

typedef struct
{
  GInitiallyUnownedClass parent_class;
} RegressTestFloatingClass;

GType        regress_test_floating_get_type (void);
RegressTestFloating* regress_test_floating_new (void);

/* Function signature torture tests */
void regress_test_torture_signature_0 (int        x,
                               double     *y,
                               int        *z,
                               const char *foo,
                               int        *q,
                               guint       m);
gboolean regress_test_torture_signature_1 (int        x,
                                   double     *y,
                                   int        *z,
                                   const char *foo,
                                   int        *q,
                                   guint       m,
                                   GError    **error);
void regress_test_torture_signature_2 (int                  x,
				       RegressTestCallbackUserData  callback,
				       gpointer              user_data,
				       GDestroyNotify        notify,
				       double               *y,
				       int                  *z,
				       const char           *foo,
				       int                  *q,
				       guint                 m);

GValue *regress_test_date_in_gvalue (void);
GValue *regress_test_strv_in_gvalue (void);

GObject * _regress_this_is_a_private_symbol (void);

void regress_test_multiline_doc_comments (void);
void regress_test_nested_parameter (int a);

/**
 * RegressSkippedStructure: (skip)
 *
 * This should be skipped, and moreover, all function which
 * use it should be.
 */
typedef struct
{
  int x;
  double v;
} RegressSkippedStructure;

void regress_random_function_with_skipped_structure (int x,
						     RegressSkippedStructure *foo,
						     double v);

/**
 * RegressIntset:
 *
 * Like telepathy-glib's TpIntset.
 *
 */
typedef struct _RegressIntset RegressIntset;

/**
 * RegressIntSet: (skip)
 *
 * Compatibility typedef, like telepathy-glib's TpIntSet
 *
 */
typedef RegressIntset RegressIntSet;

/**
 * RegressPtrArrayAlias:
 *
 * Typedef'd GPtrArray for some reason
 */
typedef GPtrArray RegressPtrArrayAlias;

void regress_introspectable_via_alias (RegressPtrArrayAlias *data);

/**
 * RegressVaListAlias:
 *
 * Typedef'd va_list for additional reasons
 */
typedef va_list RegressVaListAlias;

void regress_not_introspectable_via_alias (RegressVaListAlias ok);

/**
 * RegressAliasedTestBoxed:
 *
 * Typedef TestBoxed to test caller-allocates correctness
 */
typedef RegressTestBoxed RegressAliasedTestBoxed;

void regress_aliased_caller_alloc (RegressAliasedTestBoxed *boxed);

/* private testing */

typedef struct {
  gint this_is_public_before;
  /* < private > */
  gint this_is_private;
  /* < public > */
  gint this_is_public_after;
} RegressTestPrivateStruct;

typedef enum {
  REGRESS_TEST_PUBLIC_ENUM_BEFORE = 1 << 0,
  /* <private> */
  REGRESS_TEST_PRIVATE_ENUM       = 1 << 1,
  /* <public> */
  REGRESS_TEST_PUBLIC_ENUM_AFTER  = 1 << 2,
} RegressTestPrivateEnum;

typedef struct {
  gint just_int;
  gint array[10];
} RegressTestStructFixedArray;

void regress_test_struct_fixed_array_frob (RegressTestStructFixedArray *str);

#define REGRESS_UTF8_CONSTANT "const \xe2\x99\xa5 utf8"

#ifdef __GNUC__
#define REGRESS_TEST_GNUC_EXTENSION_STMT(foo) (G_GNUC_EXTENSION ({ int x[10]; x[5] = 42; x[5]; }))
#endif

/* https://bugzilla.gnome.org/show_bug.cgi?id=662888 */
#define REGRESS_LONG_STRING_CONSTANT \
	"TYPE,VALUE,ENCODING,CHARSET,LANGUAGE,DOM,INTL,POSTAL,PARCEL," \
	"HOME,WORK,PREF,VOICE,FAX,MSG,CELL,PAGER,BBS,MODEM,CAR,ISDN,VIDEO," \
	"AOL,APPLELINK,ATTMAIL,CIS,EWORLD,INTERNET,IBMMAIL,MCIMAIL," \
	"POWERSHARE,PRODIGY,TLX,X400,GIF,CGM,WMF,BMP,MET,PMB,DIB,PICT,TIFF," \
	"PDF,PS,JPEG,QTIME,MPEG,MPEG2,AVI,WAVE,AIFF,PCM,X509,PGP"

void regress_has_parameter_named_attrs (int        foo,
                                        gpointer   attributes);

typedef struct {
  int dummy;
  struct {
    const char *name;
    guint x;
  } attributes[32];

  double dummy2;
} RegressLikeGnomeKeyringPasswordSchema;

/* Ensure we ignore symbols that start with _; in particular we don't
 * want to issue a namespace warning.
 */
#define _DONTSCANTHIS 1

/* https://bugzilla.gnome.org/show_bug.cgi?id=685022 */
#define REGRESS_MININT64 ((gint64) G_GINT64_CONSTANT(0x8000000000000000))
#define REGRESS_MAXUINT64 (G_GINT64_CONSTANT(0xffffffffffffffffU))

#endif /* __GITESTTYPES_H__ */
