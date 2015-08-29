# -*- coding: utf8 -*-
import sys
import ast
import types


def magic(path, name):
    module = types.ModuleType(name)
    module.__file__ = path
    module.__name__ = name
    sys.modules[name] = module
    with open(path) as file:
        #TODO: find a better way to remove multiple 'coding: pyfu'
        file.readline()
        ast_object = ast.parse(file.read())
    code = compile(ast_object, path, 'exec')
    exec(code,  module.__dict__)