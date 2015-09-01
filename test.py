# -*- coding: pyfu -*-

class B(A):

    class Meta:
        def xxx(self):
            pass

    def a(self):
        pass


class A(object):

    def b(self):
        pass


def a(n=10):
    for i in range(n):
        print(i)
