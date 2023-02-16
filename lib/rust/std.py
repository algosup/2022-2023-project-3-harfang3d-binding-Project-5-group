import lang.rust

def bind_std(gen):
    class RustConstCharPtrConverter(lang.rust.RustTypeConverterCommon):
        def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
            super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
            self.rust_to_c_type = "*C.char"
            self.rust_type = "String"#, "Cow<str>", "&str", "OsString", "PathBuf"

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

    gen.bind_type(RustConstCharPtrConverter("const char *"))

    class RustBasicTypeConverter(lang.rust.RustTypeConverterCommon):
        def __init__(self,
            type: str,                  # C++ type
            c_type: str,                # C type
            rust_type: str,             # Rust type
            to_c_storage_type=None,
            bound_name=None,
            from_c_storage_type=None,
            needs_c_storage_class=False
        ):
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

    gen.bind_type(RustBasicTypeConverter("char", "C.char", "i8"))

    gen.bind_type(RustBasicTypeConverter("unsigned char", "C.uchar", "u8"))
    gen.bind_type(RustBasicTypeConverter("int8t_t", "C.short", "i8"))
    gen.bind_type(RustBasicTypeConverter("uint8_t", "C.uchar", "u8"))

    gen.bind_type(RustBasicTypeConverter("short", "C.short", "i16"))
    gen.bind_type(RustBasicTypeConverter("int16_t", "C.ushort", "i16"))
    gen.bind_type(RustBasicTypeConverter("char16_t", "C.ushort", "i16"))
    
    gen.bind_type(RustBasicTypeConverter("uint16_t", "C.ushort", "u16"))
    gen.bind_type(RustBasicTypeConverter("unsigned short", "C.ushort ", "uint16"))

    gen.bind_type(RustBasicTypeConverter("int32", "C.int32_t", "i32"))
    gen.bind_type(RustBasicTypeConverter("int", "C.int32_t", "i32"))
    gen.bind_type(RustBasicTypeConverter("int32_t", "C.int32_t", "i32"))
    gen.bind_type(RustBasicTypeConverter("char32_t", "C.int32_t", "i32"))
    gen.bind_type(RustBasicTypeConverter("size_t", "C.size_t", "i32"))

    gen.bind_type(RustBasicTypeConverter("uint32_t", "C.uint32_t", "u32"))
    gen.bind_type(RustBasicTypeConverter("unsigned int32_t", "C.uint32_t", "u32"))
    gen.bind_type(RustBasicTypeConverter("unsigned int", "C.uint32_t", "u32"))

    gen.bind_type(RustBasicTypeConverter("int64_t", "C.int64_t", "i64"))
    gen.bind_type(RustBasicTypeConverter("long", "C.int64_t", "i64"))

    gen.bind_type(RustBasicTypeConverter("float32", "C.float", "f32"))
    gen.bind_type(RustBasicTypeConverter("float", "C.float", "f32"))

    gen.bind_type(RustBasicTypeConverter("intptr_t", "C.intptr_t", "*i32")) # ! <--- Could change in the future

    gen.bind_type(RustBasicTypeConverter("unsigned long", "C.uint64_t", "u64"))
    gen.bind_type(RustBasicTypeConverter("uint64_t", "C.uint64_t ", "u64"))
    gen.bind_type(RustBasicTypeConverter("double", "C.double", "f64"))


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