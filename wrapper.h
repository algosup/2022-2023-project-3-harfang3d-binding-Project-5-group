#pragma once
#ifdef __cplusplus
extern "C" {
#endif
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <memory.h>
#include <string.h>
#include <stdlib.h>
#include "fabgen.h"

extern int  my_testreturn_int;();
extern float  my_testreturn_float;();
extern const char * my_testreturn_const_char_ptr;();
extern int * my_testreturn_int_by_pointer;();
extern int * my_testreturn_int_by_reference;();
extern int  my_testadd_int_by_value;(int  a; ,int  b;);
extern int  my_testadd_int_by_pointer;(int * a; ,int * b;);
extern int  my_testadd_int_by_reference;(int * a; ,int * b;);
#ifdef __cplusplus
}
#endif
