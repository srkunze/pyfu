# -*- coding: utf8 -*-
import codecs
import sys
import ast
import types


def magic(path, name):
    module = types.ModuleType(name)
    module.__file__ = path
    module.__name__ = name
    sys.modules[name] = module
    with codecs.open(path, 'r', 'utf-8') as file:
        #TODO: find a better way to remove multiple 'coding: pyfu'
        file.readline()
        new_content = b'# -*- coding: utf-8 -*-\n' + file.read()
        module_ast = ast.parse(new_content)
    CheckVisitor().visit(module_ast)
    transform(module_ast)
    code = compile(module_ast, path, 'exec')
    exec(code,  module.__dict__)


def transform(module_ast):
    name_dict = {}
    collect_names(name_dict, module_ast)

    #TODO: functions and methods are all fine
    #TODO: collect them and create them first
    funcs = {}
    CollectFunctionsVisitor(function_dict=funcs).visit(module_ast)
    #TODO: collect metaclasses and create them second in the correct order
    #TODO: collect classes
    pass


def collect_names(name_dict, node):
    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, (ast.ClassDef, ast.FunctionDef)):
                    name_dict[item.name] = {}
                if isinstance(item, ast.ClassDef):
                    collect_names(name_dict[item.name], item)


class CheckVisitor(ast.NodeVisitor):

    def visit_FunctionDef(self, node):
        pass

    def visit(self, node):
        allowed_node_classes = (ast.Module, ast.ClassDef, ast.FunctionDef, ast.Name, ast.Load, ast.Pass)
        if not isinstance(node, allowed_node_classes):
            raise NotSupportedError(node)
        return super(CheckVisitor, self).visit(node)


class CollectFunctionsVisitor(ast.NodeVisitor):

    def __init__(self, function_dict):
        self.function_dict = function_dict

    def visit(self, node):
        if isinstance(node, ast.FunctionDef):
            self.function_dict[node.name] = node
            return
        return super(CollectFunctionsVisitor, self).visit(node)


class NotSupportedError(Exception):
    pass












