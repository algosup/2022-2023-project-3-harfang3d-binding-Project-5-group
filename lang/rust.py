import gen 
import lib

import re


def route_lambda(name):
    return lambda args : "%s(%s);" % (name, ", ".join(args))


def clean_name(name):
    new_name = name[0].lower() + re.sub(r'([A-Z])', r'_\1', name[1:]).lower() # Convert to snake case 
    # The following line is a list of keywords in rust, the words after "abstract" are reserved to be used in the future
    if new_name in ["as", "break", "const", "continue", "crate", "else", "enum", "extern", "false", "fn", "for", "if", "impl", "in", "let", "loop", "match", "mod", "move", "mut", "pub", "ref", "return", "self", "Self", "static", "struct", "super", "trait", "true", "type", "unsafe", "use", "where", "while", "async", "await", "dyn", "abstract", "become", "box", "do", "final", "macro", "override", "priv", "typeof", "unsized", "virtual", "yield", "try", "'union", "static"]:
        new_name = new_name + "_"
    return new_name

def clean_name_with_type(name, type): 
    '''
    This function is used to clean the name of the function and the type of the function, to format everything

    However in rust, there is 2 keywords with a problem, "'union" and "Self" which is different from self, we need to handle both of them differently
    '''

    # method to let the function support the keywords
    new_name = ""
    if type == "Self":
        pass 
    elif type == "'union":
        pass
    elif type == "self":
        pass

    elif "_" in name:
        next_is_forced_uppercase = True 
        for c in name:
            if c == "_":
                next_is_forced_uppercase = True
            elif next_is_forced_uppercase:
                new_name += c.capitalize()
                next_is_forced_uppercase = False
            else:
                new_name += c
    else:
        first_letter_checked = False
        for c in name: 
            if c in ["&", "*"] or first_letter_checked:
                new_name += c
            elif not first_letter_checked:
                first_letter_checked = True 
                new_name += c.capitalize()
    return new_name.strip().replace("_", "").replace(":", "")

class RustTypeConverterCommon(gen.TypeConverter):
    def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
        super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
        self.base_type = type 
        self.rust_to_c_type = None 
        self.rust_type = None 

    def get_type_api(self, module_name):
        out = "// type API for %s\n" % self.base_type
        if self.c_storage_class:
            out += "struct %s;\n" % self.c_storage_class
        if self.c_storage_class:
            out += "void %s(int idx, void *obj, %s storage);\n" % (self.to_c_func, self.c_storage_class)
        else:
            out += "void %s(int idx, void *obj);\n" % self.to_c_func
        out += "int %s(void *obj, OwnershipPolicy);\n" % self.from_c_func
        out += "\n"
        return out 

    def to_c_call(self, in_var, out_var_p, is_pointer):
        return ""
    
    def from_c_call(self, out_var, expr, ownership):
        return "%s((void *)%s, %s);\n" % (self.from_c_func, expr, ownership)
    

class DummyTypeConverter(gen.TypeConverter):
    def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
        super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
    
    def get_type_api(self, module_name): 
        return ""

    def to_c_call(self, in_var, out_var_p, is_pointer):
        return ""
    
    def from_c_call(self, out_var, expr, ownership):
        return ""
    
    def check_call(self, in_var):
        return ""
    
    def get_type_glue(self, gen, module_name):
        return ""

class RustPtrTypeConverter(gen.TypeConverter):
    def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
        super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
    
    def get_type_api(self, module_name):
        return ""
    
    def to_c_call(self, in_var, out_var_p, is_pointer):
        return ""
    
    def from_c_call(self, out_var, expr, ownership):
        return ""

    def check_call(self, in_var):
        return ""
    
    def get_type_glue(self, gen, module_name):
        return ""


class RustClassTypeDefaultConverter(RustTypeConverterCommon):
    def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
        super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)

    def is_type_class(self):
        return True
    
    def get_type_api(self, module_name):
        return ""
    
    def to_c_call(self, in_var, out_var_p, is_pointer):
        out = f"let mut {out_var_p.replace('&', '_')} = {in_var}.h;\n"
        return out
    
    def from_c_call(self, out_var, expr, ownership):
        return ""
    
    def check_call(self, in_var):
        return ""
    
    def get_type_glue(self, gen, module_name):
        return ""

class RustExternTypeConverter(RustTypeConverterCommon):
    def __init__(self, type, to_c_storage_type, bound_name, module):
        super().__init__(type, to_c_storage_type, bound_name)
        self.module = module 
    
    def get_type_api(self, module_name):
        return ''
    
    def to_c_call(self, in_var, out_var_p):
        out = ''
        if self.c_storage_class:
            c_storage_var = 'storage_%s' % out_var_p.replace('&', '_')
            out += '%s %s;\n' % (self.c_storage_class, c_storage_var)
            out += '(*%s)(%s, (void *)%s, %s);\n' % (self.to_c_func, in_var, out_var_p, c_storage_var)
        else: 
            out += '(*%s)(%s, (void *)%s);\n' % (self.to_c_func, in_var, out_var_p)
        return out
    
    def from_c_call(self, out_var, expr, ownership):
        return "%s = (*%s)((void *)%s, %s);\n" % (out_var, self.from_c_func, expr, ownership)
    
    def check_call(self, in_var):
        return "(*%s)(%s)" % (self.check_func, in_var)
    
    def get_type_glue(self, gen, module_name):
        out = ''

class RustPtrTypeDefaultConverter(RustTypeConverterCommon):
    def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
        super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)
    
    def is_type_ptr(self):
        return True
    
    def get_type_api(self, module_name):
        return ""
    
    def to_c_call(self, in_var, out_var_p, is_pointer):
        out = f"let mut {out_var_p.replace('&', '_')} = {in_var}.h;\n"
        return out
    
    def from_c_call(self, out_var, expr, ownership):
        return ""
    
    def check_call(self, in_var):
        return ""
    
    def get_type_glue(self, gen, module_name):
        return ""


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
    
    def start(self, module_name):
        super().start(module_name)
