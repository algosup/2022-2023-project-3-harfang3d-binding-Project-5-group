import lib

def bind(gen):
    gen.start('my_test')

    lib.bind_defaults(gen)

    # inject test code in the wrapper
    gen.insert_code('''\
    // basic interoperability
    int return_int() { return 8; }
    float return_float() { return 8.f; }
    const char *return_const_char_ptr() { return "const char * -> string"; }

    static int static_int = 9;

    int *return_int_by_pointer() { return &static_int; }
    int &return_int_by_reference() { return static_int; }

    // argument passing
    int add_int_by_value(int a, int b) { return a + b; }
    int add_int_by_pointer(int *a, int *b) { return *a + *b; }
    int add_int_by_reference(int &a, int &b) { return a + b; }
    \n''', True, False)

    gen.add_include('string', True)

    gen.bind_function('return_int', 'int', [])
    gen.bind_function('return_float', 'float', [])
    gen.bind_function('return_const_char_ptr', 'const char *', [])

    gen.bind_function('return_int_by_pointer', 'int*', [])
    gen.bind_function('return_int_by_reference', 'int&', [])

    gen.bind_function('add_int_by_value', 'int', ['int a', 'int b'])
    gen.bind_function('add_int_by_pointer', 'int', ['int *a', 'int *b'])
    gen.bind_function('add_int_by_reference', 'int', ['int &a', 'int &b'])

    gen.finalize()