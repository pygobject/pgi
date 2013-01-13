# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import sys
import string
import collections


class CodeBlock(object):
    """A piece of code with global dependencies"""

    INDENTATION = 4

    def __init__(self):
        super(CodeBlock, self).__init__()
        self._lines = []
        self._deps = {}

    def add_dependency(self, name, obj):
        """Add a code dependency so it gets inserted into globals"""

        if name in self._deps:
            if self._deps[name] is obj:
                return
            raise ValueError("There exists a different dep with the same name")
        self._deps[name] = obj

    def write_into(self, block, level=0):
        """Append this block to another one, passing all dependencies"""

        for line, l in self._lines:
            block.write_line(line, level + l)

        for name, obj in self._deps.iteritems():
            block.add_dependency(name, obj)

    def write_line(self, line, level=0):
        """Append a new line"""

        self._lines.append((line, level))

    def write_lines(self, lines, level=0):
        """Append multiple new lines"""

        for line in lines:
            self.write_line(line, level)

    def compile(self):
        """Execute the python code and returns the global dict"""

        code = compile(str(self), "<string>", "exec")
        global_dict = dict(self._deps)
        exec code in global_dict
        return global_dict

    def pprint(self):
        """Print the code block to stdout.
        Does syntax highlighting if possible.
        """

        code = str(self)
        if sys.stdout.isatty():
            try:
                from pygments import highlight
                from pygments.lexers import PythonLexer
                from pygments.formatters import TerminalFormatter
            except ImportError:
                pass
            else:
                formatter = TerminalFormatter(bg="dark")
                lexer = PythonLexer()
                print highlight(code, lexer, formatter).strip()
                return
        print code

    def __str__(self):
        lines = []
        if self._deps:
            lines.append("# dependencies: %s" % ", ".join(self._deps.keys()))
        else:
            lines.append("# no dependencies")

        for line, level in self._lines:
            lines.append(" " * self.INDENTATION * level + line)
        return "\n".join(lines)

    def __repr__(self):
        name = self.__class__.__name__
        deps = ",".join(self._deps.keys())
        return "<%s lines=%d, deps=%r>" % (name, len(self._deps), deps)


def parse_code(code, var_factory, **kwargs):
    """Parse a piece of text and substitude $var by either unique
    variable names or by the given kwargs mapping. Use $$ to escape $.

    Returns a CodeBlock and the resulting variable mapping.

    >>> parse("$foo = $foo + $bar", bar="1")
    >>> ("t1 = t1 + 1", {'foo': 't1', 'bar': '1'})
    """

    block = CodeBlock()
    defdict = collections.defaultdict(var_factory)
    defdict.update(kwargs)

    indent = -1
    code = code.strip()
    for line in code.splitlines():
        length = len(line)
        line = line.lstrip()
        spaces = length - len(line)
        if spaces:
            if indent < 0:
                indent = spaces
                level = 1
            else:
                level = spaces / indent
        else:
            level = 0

        block.write_line(string.Template(line).substitute(defdict), level)
    return block, dict(defdict)


class CodeGenerator(object):
    """Helper class that holds a variable factory"""

    def __init__(self, variable_factory):
        super(CodeGenerator, self).__init__()
        self._factory = variable_factory

    def var(self):
        """Generate a new variable name"""

        return self._factory()

    def parse(self, code, **kwargs):
        """Parse code: see parse_code()"""

        return parse_code(code, self._factory, **kwargs)
