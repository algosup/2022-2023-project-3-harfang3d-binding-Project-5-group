import lang.rust

def bind_std(gen):
    class RustBasicTypeConverter(lang.rust.RustTypeConverterCommon):
        def __init__(self, 
            type,
            c_type,
            rust_type,
            to_c_storage_type = None,
            bound_name = None,
            from_c_storage_type = None,
            needs_c_storage_class = False,
        ):
            super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
            self.rust_to_c_type = c_type
            self.rust_type = rust_type

        def get_type_glue(self, gen, module_name):
            return ''

    gen.bind_type(RustBasicTypeConverter("int", "C.int32_t", "i32"))