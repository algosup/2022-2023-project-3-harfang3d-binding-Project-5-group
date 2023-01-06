import lang.rust

def bind_stl(gen):
    gen.add_include('vector', True)
    gen.add_include('string', True)