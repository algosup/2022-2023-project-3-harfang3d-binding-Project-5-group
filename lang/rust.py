import gen

class RustTypeConverterCommon(gen.TypeConverter):
    pass

class RustClassTypeDefaultConverter(RustTypeConverterCommon):
    pass

class RustPtrTypeDefaultConverter(RustTypeConverterCommon):
    pass

class RustExternTypeConverter(RustTypeConverterCommon):
    pass

class RustGenerator(gen.FABGen):
    default_class_converter = RustClassTypeDefaultConverter
    default_ptr_converter = RustPtrTypeDefaultConverter
    default_extern_converter = RustExternTypeConverter

    def __init__(self):
        super().__init__()

        raise NotImplementedError("Rust generator is not implemented yet")

    def get_language(self):
        return "Rust"