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
        new_content = '# -*- coding: utf-8 -*-\n' + file.read()
        ast_object = ast.parse(new_content)
    CheckVisitor().visit(ast_object)
    Transformer().visit(ast_object)
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


class Transformer(ast.NodeTransformer):
    pass


class NotSupportedError(Exception):
    pass