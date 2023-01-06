import lib

def bind(gen):
    gen.start('float_value')

    lib.bind_defaults(gen)  # bind default types (int, float, etc...)

    float_value = gen.begin_class('FloatValue')  # begin type definition
    gen.bind_constructor(float_value, ['?float value'])  # declare constructor

    gen.bind_method(float_value, 'Get', 'float', [])  # declare getter method
    gen.bind_method(float_value, 'Set', 'void', ['float value'])  # declare setter method

    gen.bind_arithmetic_ops_overloads(float_value, ['+'], [('FloatValue', ['const FloatValue &b'], [])])  # bind arithmetic operator

    gen.end_class(float_value)

    gen.finalize()