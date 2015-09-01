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
        new_content = b'# -*- coding: utf-8 -*-\n' + file.read()
        module_ast = ast.parse(new_content)
    CheckVisitor().visit(module_ast)
    transform(module_ast)
    code = compile(module_ast, path, 'exec')
    exec(code,  module.__dict__)


class CheckVisitor(ast.NodeVisitor):

    def visit_FunctionDef(self, node):
        pass

    def visit(self, node):
        allowed_node_classes = (ast.Module, ast.ClassDef, ast.FunctionDef, ast.Name, ast.Load, ast.Pass)
        if not isinstance(node, allowed_node_classes):
            raise NotSupportedError(node)
        return super(CheckVisitor, self).visit(node)


def transform(module_ast):
    dependency_graph = DependencyGraph(module_ast)
    dependency_graph.linearized
    #TODO: generate an AST that implements the linearized dependency graph


class DependencyGraph(dict):

    def __init__(self, ast_node):
        self.ast_node = ast_node
        self._build(ast_node, [])

    def _build(self, node, ns):
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.FunctionDef):
                        depends_on = {'.'.join(ns)} if ns else set()
                        for decorator in item.decorator_list:
                            CollectNamesVisitor(depends_on).visit(decorator)
                        self['.'.join(ns + [item.name])] = {
                            'node': item,
                            'depends_on': depends_on,
                        }
                    if isinstance(item, ast.ClassDef):
                        depends_on = {'.'.join(ns)} if ns else set()
                        for decorator in item.decorator_list:
                            CollectNamesVisitor(depends_on).visit(decorator)
                        depends_on.update({base.id for base in item.bases})
                        self['.'.join(ns + [item.name])] = {
                            'node': item,
                            'depends_on': depends_on,
                        }
                        self._build(item, ns + [item.name])

    @property
    def linearized(self):
        builtins = set(__builtins__.keys())
        satisfied = [name for name, name_data in self.items() if not name_data['depends_on']]
        satisfied_set = set(satisfied)
        unsatisfied = set(self.keys()) - set(satisfied)

        while unsatisfied:
            found_one = False
            for name in unsatisfied:
                if not (self[name]['depends_on'] - satisfied_set - builtins):
                    found_one = True
                    satisfied.append(name)
                    satisfied_set.add(name)
                    unsatisfied.remove(name)
                    break
            if not found_one:
                raise UnsatisfiableDependenciesError(self, unsatisfied)

        return satisfied


class CollectNamesVisitor(ast.NodeVisitor):

    def __init__(self, names):
        self.names = names

    def visit_Name(self, node):
        self.names.add(node.id)

    def visit(self, node):
        node_classes_to_visit = (ast.Module, ast.ClassDef, ast.Name, ast.Load, ast.Call)
        if isinstance(node, node_classes_to_visit):
            super(CollectNamesVisitor, self).visit(node)
        return self


class NotSupportedError(Exception):
    pass


class UnsatisfiableDependenciesError(Exception):
    pass
