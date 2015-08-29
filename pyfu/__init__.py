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
    CheckVisitor().visit(ast_object)
    code = compile(ast_object, path, 'exec')
    exec(code,  module.__dict__)


class CheckVisitor(ast.NodeVisitor):

    def visit_FunctionDef(self, node):
        pass

    def visit(self, node):
        allowed_node_classes = (ast.Module, ast.ClassDef, ast.FunctionDef, ast.Name, ast.Load, ast.Pass)
        if not isinstance(node, allowed_node_classes):
            raise NotSupportedError(node)
        return super(CheckVisitor, self).visit(node)


class NotSupportedError(Exception):
    pass