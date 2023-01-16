import gen
import lib

import re


def route_lambda(name):
    return lambda args: "%s(%s);" % (name, ", ".join(args))


def clean_name(name):
    new_name = name[0].lower() + re.sub(r'([A-Z])', r'_\1',
                                        name[1:]).lower()  # Convert to snake case
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
        super().__init__(type, to_c_storage_type, bound_name,
                         from_c_storage_type, needs_c_storage_class)
        self.base_type = type
        self.rust_to_c_type = None
        self.rust_type = None

    def get_type_api(self, module_name):
        out = "// type API for %s\n" % self.base_type
        if self.c_storage_class:
            out += "struct %s;\n" % self.c_storage_class
        if self.c_storage_class:
            out += "void %s(int idx, void *obj, %s storage);\n" % (
                self.to_c_func, self.c_storage_class)
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
        super().__init__(type, to_c_storage_type, bound_name,
                         from_c_storage_type, needs_c_storage_class)

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
        super().__init__(type, to_c_storage_type, bound_name,
                         from_c_storage_type, needs_c_storage_class)

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
        super().__init__(type, to_c_storage_type, bound_name,
                         from_c_storage_type, needs_c_storage_class)

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
            out += '(*%s)(%s, (void *)%s, %s);\n' % (self.to_c_func,
                                                     in_var, out_var_p, c_storage_var)
        else:
            out += '(*%s)(%s, (void *)%s);\n' % (self.to_c_func,
                                                 in_var, out_var_p)
        return out

    def from_c_call(self, out_var, expr, ownership):
        return "%s = (*%s)((void *)%s, %s);\n" % (out_var, self.from_c_func, expr, ownership)

    def check_call(self, in_var):
        return "(*%s)(%s)" % (self.check_func, in_var)

    def get_type_glue(self, gen, module_name):
        out = '//extern API for %s\n' % self.ctype
        if self.c_storage_class:
            out += "struct %s;\n" % self.c_storage_class
        out += "void %s(int idx, void *obj, %s storage);\n" % (self.to_c_func,
                                                               self.c_storage_class)
        out += "void *%s(void *obj, OwnershipPolicy);\n" % self.from_c_func
        out += "int %s(void *obj);\n" % self.check_func
        out += '\n'
        return out


class RustGenerator(gen.FABGen):
    default_ptr_converter = RustPtrTypeConverter
    default_class_converter = RustClassTypeDefaultConverter
    default_extern_converter = RustExternTypeConverter

    def __init__(self):
        super().__init__()
        self.check_self_type_in_ops = True
        self.rust = ''
        self.crust_directives = ''

    def get_language(self):
        return "Rust"

    def output_includes(self):
        pass

    def start(self, module_name):
        super().start(module_name)

        self._source += self.get_binding_api_declaration(module_name)

    def set_compilation_directives(self, directives):
        self.crust_directives = directives

    def set_error(self, type, reason):
        return ""

    def get_self(self, ctx):
        return ""

    def get_var(self, i, ctx):
        return ""

    def open_proxy(self, name, max_arg_count, ctx):
        return ""

    def _proto_call(self, self_conv, proto, expr_eval, ctx, fixed_arg_count=None):
        return ""

    def _bind_proxy(self, name, self_conv, protos, desc, expr_eval, ctx, fixed_arg_count=None):
        return ""

    def close_proxy(self, ctx):
        return ""

    def proxy_call_error(self, msg, ctx):
        return ""

    def return_void_from_c(self):
        return ""

    def rval_from_nullptr(self, out_var):
        return ""

    def rval_from_c_ptr(self, conv, out_var, expr, ownership):
        return ""

    def commit_from_c_vars(self, rvals, ctx="default"):
        return ""

    def rbind_function(self, name, rval, args, internal=False):
        return ""

    def get_binding_api_declaration(self):
        type_info_name = gen.apply_api_prefix("type_info")

        out = '''\
struct %s {
    uint32_T type_tag;
    const char *c_type;
    const char *bound name;

    bool (*check)(void* p);
    void (*to_c)(void *p, void *out);
    int (*from_c)(void *obj, OwnershipPolicy policy);
};\n

''' % type_info_name

        out += "//return a type info from its type tag\n"
        out += "%s *%s(u_t type tag);\nnin" % (type_info_name,
                                               gen.apply_api_prefix("get_bound_type_info"))

        out += "//return a type info from its type name\n"
        out += "%s *%s(const char *type);\n" % (type_info_name,
                                                gen.apply_api_prefix("get_c_type_info"))

        out += "// return the typetag of a userdata object, null ptr if not a FABGen object\n"
        out += "uint32_t %s(void* p); \n\n" % gen.apply_api_prefix(
            "get_wrapped_object_type_tag")

    def output_binding_api(self):
        type_info_name = gen.apply_api_prefix("type_info")
        self._source += '''
    %s *%s(const char *name) {
        return nullptr;
    }\n\n''' % (
            type_info_name, gen.apply_api_prefix("get_type_info"))

        self._source += '''\
    uint32_t %s (void* p) {
        return 0;
        //auto o =  cast_to_wrapped_Object_safe(L, idx);
        //return o ? o->type_tag : 0;
    }\n\n''' % gen.apply_api_prefix("get_wrapped_object_type_tag")

    def get_output(self):
        return {"wrapper.cpp": self.rust_c, "wrapper.h": self.rust_h, "bind.rs": self.rust_bind, "translate_file.json": self.rust_translate_file}

    def _get_type(self, name):
        for type in self._bound_types:
            if type:
                return type
        return None

    def _get_conv(self, conv_name):
        if conv_name in self._FABGen_type_convs:
            return self.get_conv(conv_name)
        return None

    def _get_conv_from_bound_name(self, bound_name):
        for name, conv in self._FABGen__type_convs.items():
            if conv.bound_name == bound_name:
                return conv
        return None

    def __get_is_type_class_or_pointer_with_class(self, conv):
        if conv.is_type_class() or \
                (isinstance(conv, RustPtrTypeConverter) and self._get_conv(str(conv.ctype.scoped_typename)) is None):
            return True
        return False

    def __get_stars(self, val, start_stars=0, add_stars_for_ref=True):
        stars = "*" * start_stars
        if "carg" in val and hasattr(val["carg"].ctype, "ref"):
            stars += "*" * (len(val["carg"].ctype.ref) if add_stars_for_ref else val["carg"].ctype.ref.count('*'))
        elif "storage_ctype" in val and hasattr(val["storage_ctype"], "ref"):
            star += "*" * (len(val["storage_ctype"].ref) if add_stars_for_ref else val["storage_ctype"].ref.count('*'))
        elif hasattr(val["conv"].ctype, "ref"):
            stars += "*" * (len(val["conv"].ctype.ref) if add_stars_for_ref else val["conv"].ctype.ref.count('*'))
        return stars

    def __arg_from_cpp_to_c(self, val, retval_name, just_copy):
        src = ""
               # type class, not a pointer
        if val['conv'] is not None and val['conv'].is_type_class() and \
                not val['conv'].ctype.is_pointer() and ('storage_ctype' not in val or not hasattr(val['storage_ctype'], 'ref') or not any(s in val['storage_ctype'].ref for s in ["&", "*"])):
                               # special shared ptr
            if 'proxy' in val['conv']._features:
                src += f"	if(!{retval_name})\n" \
                    "		return nullptr;\n"

                src += "	auto " + \
                    val['conv']._features['proxy'].wrap(
                        "ret", "retPointer")
                               # special std::future
            elif val["conv"] is not None and "std::future" in str(val["conv"].ctype):
                src += f"	auto retPointer = new std::future<int>(std::move({retval_name}));\n"
            else:
                                   # class, not pointer, but static
                if just_copy:
                    src += f"	auto retPointer = {retval_name};\n"
                else:
                    src += f"	auto retPointer = new {val['conv'].ctype}({retval_name});\n"
            retval_name = f"({(self._name)}{(val['conv'].bound_name)})(retPointer)"
        else:
                   # special std::string (convert to const char*)
            if val["conv"] is not None and "std::string" in str(val["conv"].ctype):
                stars = self.__get_stars(val)
                if len(stars) > 0:  # rarely use but just in case
                    retval_name = f"new const char*(&(*{retval_name}->begin()))"
                else:
                    retval_name = f"{retval_name}.c_str()"
            else:
                retval_name = f"{retval_name}"

                # cast it
                # if it's an enum
        if val["conv"].bound_name in self._enums.keys():
            enum_conv = self._get_conv_from_bound_name(val['conv'].bound_name)
            if enum_conv is not None and hasattr(enum_conv, "base_type") and enum_conv.base_type is not None:
                arg_bound_name = str(enum_conv.base_type)
            else:
                arg_bound_name = "int"
            retval_name = f"({arg_bound_name}){retval_name}"
               # cast it, if it's a const
        elif 'storage_ctype' in val and val["storage_ctype"].const or \
        'carg' in val and val["carg"].ctype.const:
            arg_bound_name = self.__get_arg_bound_name_to_c(val)
            retval_name = f"({arg_bound_name}){retval_name}"

        return src, retval_name

    def __arg_from_c_to_cpp(self, val, retval_name, add_star=True):
        src = ""
		# check if there is special slice to convert
        if isinstance(val["conv"], lib.go.stl.GoSliceToStdVectorConverter):
			# special if string or const char*
            if "GoStringConverter" in str(val["conv"].T_conv): # or \
				# "GoConstCharPtrConverter" in str(val["conv"].T_conv):
                src += f"std::vector<{val['conv'].T_conv.ctype}> {retval_name};\n"\
                    f"for(int i_counter_c=0; i_counter_c < {retval_name}ToCSize; ++i_counter_c)\n"\
					f"	{retval_name}.push_back(std::string({retval_name}ToCBuf[i_counter_c]));\n"
			# slice from class
            elif self.__get_is_type_class_or_pointer_with_class(val["conv"].T_conv):
                src += f"std::vector<{val['conv'].T_conv.ctype}> {retval_name};\n"\
					f"for(int i_counter_c=0; i_counter_c < {retval_name}ToCSize; ++i_counter_c)\n"\
					f"	{retval_name}.push_back(*(({val['conv'].T_conv.ctype}**){retval_name}ToCBuf)[i_counter_c]);\n"
            else:
                src += f"std::vector<{val['conv'].T_conv.ctype}> {retval_name}(({val['conv'].T_conv.ctype}*){retval_name}ToCBuf, ({val['conv'].T_conv.ctype}*){retval_name}ToCBuf + {retval_name}ToCSize);\n"

        retval = ""
		# very special case, std::string &
        if "GoStringConverter" in str(val["conv"]) and \
			"carg" in val and hasattr(val["carg"].ctype, "ref") and any(s in val["carg"].ctype.ref for s in ["&"]) and \
			not val["carg"].ctype.const:
            src += f"std::string {retval_name}_cpp(*{retval_name});\n"
            retval += f"{retval_name}_cpp"
		# std::function
        elif "GoStdFunctionConverter" in str(val["conv"]):
            func_name = val["conv"].base_type.replace("std::function<", "")[:-1]
            first_parenthesis = func_name.find("(")
            retval += f"({func_name[:first_parenthesis]}(*){func_name[first_parenthesis:]}){retval_name}"
		# classe or pointer on class
        else:
            if self.__get_is_type_class_or_pointer_with_class(val["conv"]):
                stars = self.__get_stars(val, add_start_for_ref=False)
				# for type pointer, there is a * in the ctype, so remove one
                if isinstance(val['conv'], RustPtrTypeConverter):
                    stars = stars[1:]
				
				# if it's not a pointer, add a star anyway because we use pointer to use in go
                if (not val["conv"].ctype.is_pointer() and ("carg" not in val or ("carg" in val and not val["carg"].ctype.is_pointer()))):
                    stars += "*"
                    if add_star:
                        retval += "*"

                retval += f"({val['conv'].ctype}{stars}){retval_name}"

            elif "carg" in val and hasattr(val["carg"].ctype, "ref") and any(s in val["carg"].ctype.ref for s in ["&"]) and not val["carg"].ctype.const:
				# add cast and *
                retval = f"({val['carg'].ctype})(*{retval_name})"
			# cast, if it's an enum
            elif val["conv"].bound_name in self._enums.keys():
                retval = f"({val['conv'].ctype}){retval_name}"
            else:
                retval = retval_name

        return src, retval

    def __arg_from_c_to_rust(self, val, retval_name, non_owning=False):

        rval_ownership = self._FABGen__ctype_to_ownership_policy(val["conv"].ctype)

        src = ""
        # check if pointer 
        if ('carg' in val and (val['carg'].ctype.is_pointer() or (hasattr(val)['carg'].ctype, 'ref') and any (s in val['carg'].ctype.ref for s in ["&", "*"]))) or \
            ('carg' not in val and 'storage_ctype' in val and (val['storage_ctype'].is_pointer() or (hasattr(val['storage_ctype'], 'ref' and any(s in val['storage_ctype'].ref for s in ["&", "*"]))))) or \
            ('carg' not in val and 'storage_ctype' not in val and val['conv'].ctype.is_pointer()):
            is_pointer = True 
        else:
            is_pointer = False
        
        # check if ref 
        if ('carg' in val and (hasattr(val['carg'].ctype, 'ref') and any (s in val['carg'].ctype.ref for s in ["&"]))) or \
            ('carg' not in val and 'storage_ctype' in val and (hasattr(val['storage_ctype'], 'ref') and any (s in val['storage_ctype'].ref for s in ["&"]))):
            is_ref = True
        else:
            is_ref = False
        

        if not is_pointer:
            if val['conv'].bound_name in self._enums.keys():
                retval_name = f"{val['conv'].bound_name}({retval_name})"
            else:
                conversation_ret = val['conv'].from_c_call(retval_name, "","")
                if conversation_ret != "":
                    retval_name = conversation_ret
                
                if val["conv"].is_type_class():
                    retval_boundname = val["conv"].bound_name
                    retval_boundname = clean_name_with_type(retval_boundname)

                    src += f"   let {retval_name}_rust = {retval_boundname}::from_c({retval_name});\n"
                    

                    if rval_ownership != "NonOwning" and not is_ref and not non_owning:
                        src += f"  " #TODO ff
