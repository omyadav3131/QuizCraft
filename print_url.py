import ast
if not hasattr(ast, 'Str'):
    # Polyfill ast.Str for Werkzeug 1.0.1 in Python 3.14
    class _Str(ast.AST):
        _fields = ('s',)
        def __init__(self, s, **kwargs):
            self.s = s
            super().__init__(**kwargs)
    ast.Str = _Str
    
    class _Num(ast.AST):
        _fields = ('n',)
        def __init__(self, n, **kwargs):
            self.n = n
            super().__init__(**kwargs)
    ast.Num = _Num
    
    class _NameConstant(ast.AST):
        _fields = ('value',)
        def __init__(self, value, **kwargs):
            self.value = value
            super().__init__(**kwargs)
    ast.NameConstant = _NameConstant

from app import create_app
app = create_app()
print(app.url_map)
