import lang.rust

def bind_std(gen):
    class RustConstCharPtrConverter(lang.rust.RustTypeConverterCommon):
        def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
            super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
            self.rust_to_c_type = "*C.char"
            self.rust_type = "String", "Cow<str>", "&str", "OsString", "PathBuf"

        def get_type_glue(self, gen, module_name):
            return ''
        
        def get_type_api(self, module_name):
            return ''
        
        def to_c_call(self, in_var, out_var_p, is_pointer=False):
            if is_pointer:
                out = f"{out_var_p.replace('&', '_')}1 := CString(*{in_var})\n"
                out += f"{out_var_p.replace('&', '_')} := &{out_var_p.replace('&', '_')}1\n"
            else:
                out = f"{out_var_p.replace('&', '_')}, idFin{out_var_p.replace('&', '_')} := wrapString({in_var})\n"
                out += f"defer idFin{out_var_p.replace('&', '_')}()\n"
            return out
        
        def from_c_call(self, out_var, in_var, is_pointer=False):
            if is_pointer:
                return f"{out_var} = CString({in_var})\n"
            else:
                return f"{out_var} = CString(*{in_var})\n"
        
        def to_c_storage(self, in_var, out_var):
            return f"{out_var} = CString({in_var})\n"
        
        def from_c_storage(self, out_var, in_var):
            return f"{out_var} = CString({in_var})\n"
        
    
    class RustBasicTypeConverter(lang.rust.RustTypeConverterCommon):
        def __init__(self, type, c_type, rust_type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
            super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
            self.rust_to_c_type = c_type
            self.rust_type = rust_type
        
        def get_type_glue(self, gen, module_name):
            return ''
        
        def get_type_api(self, module_name):
            return ''
        
        #? Need to update these functions with the correct syntax for Rust
        def to_c_call(self, in_var, out_var_p, is_pointer=False):
            if is_pointer:
                return f"{out_var_p} = &{in_var}\n"
            else:
                return f"{out_var_p} = {in_var}\n"
        
        def from_c_call(self, out_var, in_var, is_pointer=False):
            return f"{out_var} = {in_var}\n"
        # end of update

    gen.bind_type("std::ffi::CString", RustConstCharPtrConverter)
    gen.bind_type("std::ffi::CStr", RustConstCharPtrConverter)

    gen.bind_type("std::os::raw::c_char", RustBasicTypeConverter, "C.char", "c_char")
    gen.bind_type("std::os::raw::c_uchar", RustBasicTypeConverter, "C.uchar", "c_uchar") # Unsigned char is not supported natively by Rust
    
    gen.bind_type("std::os::raw::c_short", RustBasicTypeConverter, "C.short", "c_short")
    gen.bind_type("std::os::raw::c_ushort", RustBasicTypeConverter, "C.ushort", "c_ushort")


    gen.bind_type("std::os::raw::c_int", RustBasicTypeConverter, "C.int", "c_int")
    gen.bind_type("std::os::raw::c_uint", RustBasicTypeConverter, "C.uint", "c_uint")
    gen.bind_type("std::os::raw::c_long", RustBasicTypeConverter, "C.long", "c_long")
    gen.bind_type("std::os::raw::c_ulong", RustBasicTypeConverter, "C.ulong", "c_ulong")
    gen.bind_type("std::os::raw::c_longlong", RustBasicTypeConverter, "C.longlong", "c_longlong")
    gen.bind_type("std::os::raw::c_ulonglong", RustBasicTypeConverter, "C.ulonglong", "c_ulonglong")

    gen.bind_type("std::os::raw::c_float", RustBasicTypeConverter, "C.float", "c_float")
    gen.bind_type("std::os::raw::c_double", RustBasicTypeConverter, "C.double", "c_double")

    gen.bind_type("std::os::raw::c_bool", RustBasicTypeConverter, "C.bool", "c_bool")

    gen.bind_type("std::os::raw::c_void", RustBasicTypeConverter, "C.void", "c_void")

    gen.bind_type("std::os::raw::c_schar", RustBasicTypeConverter, "C.schar", "c_schar")


    class RustBoolConverter(lang.rust.RustTypeConverterCommon):
        def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
            super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
            self.rust_to_c_type = "C.bool"
            self.rust_type = "bool"

        def get_type_glue(self, gen, module_name):
            return ''

        def get_type_api(self, module_name):
            return ''

        def to_c_call(self, in_var, out_var_p, is_pointer):
            if is_pointer:
                return f"{out_var_p} = &{in_var}\n"
            else:
                return f"{out_var_p} = {in_var}\n"

        def from_c_call(self, out_var, expr, ownership):
            return "bool (%s)" % (out_var)
    
    gen.bind_type(RustBoolConverter("bool")).nobind = True