# -*- coding: utf8 -*-

from __future__ import unicode_literals


def magic(path, name):
    import sys
    import ast
    import types
    with open(path) as file:
        buf = file.read()
        print(buf)
        ast_object = ast.parse(buf)
    code = compile(ast_object, path, 'exec')
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(code,  module.__dict__)