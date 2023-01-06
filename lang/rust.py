import gen

class RustTypeConverterCommon(gen.TypeConverter):
    pass

class RustClassTypeDefaultConverter(RustTypeConverterCommon):
    pass

class RustPtrTypeDefaultConverter(RustTypeConverterCommon):
    def get_type_glue(self, gen, module_name):
        return ''

class RustExternTypeConverter(RustTypeConverterCommon):
    pass

class RustGenerator(gen.FABGen):
    default_class_converter = RustClassTypeDefaultConverter
    default_ptr_converter = RustPtrTypeDefaultConverter
    default_extern_converter = RustExternTypeConverter

    def __init__(self):
        super().__init__()
        self.rust = ''
        self.crust_directives = ''

    def get_language(self):
        return "Rust"
    
    # def start(self, module_name):
    #     super().start(module_name)