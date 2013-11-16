# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import sys
import string
import collections

from pgi import _compat


class CodeBlock(object):
    """A piece of code with global dependencies"""

    INDENTATION = 4

    def __init__(self, line=None):
        super(CodeBlock, self).__init__()
        self._lines = []
        self._deps = {}
        if line:
            self.write_line(line)

    def get_dependencies(self):
        return self._deps

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

        for name, obj in _compat.iteritems(self._deps):
            block.add_dependency(name, obj)

    def write_line(self, line, level=0):
        """Append a new line"""

        self._lines.append((line, level))

    def write_lines(self, lines, level=0):
        """Append multiple new lines"""

        for line in lines:
            self.write_line(line, level)

    def compile(self, **kwargs):
        """Execute the python code and returns the global dict.
        kwargs can contain extra dependencies that get only used
        at compile time.
        """

        code = compile(str(self), "<string>", "exec")
        global_dict = dict(self._deps)
        global_dict.update(kwargs)
        _compat.exec_(code, global_dict)
        return global_dict

    def pprint(self, file_=sys.stdout):
        """Print the code block to stdout.
        Does syntax highlighting if possible.
        """

        code = []
        if self._deps:
            code.append("# dependencies:")
        for k, v in _compat.iteritems(self._deps):
            code.append("#   %s: %r" % (k, v))
        code.append(str(self))
        code = "\n".join(code)

        if file_.isatty():
            try:
                from pygments import highlight
                from pygments.lexers import PythonLexer
                from pygments.formatters import TerminalFormatter
            except ImportError:
                pass
            else:
                formatter = TerminalFormatter(bg="dark")
                lexer = PythonLexer()
                file_.write(highlight(code, lexer, formatter))
                return
        file_.write(code)

    def __str__(self):
        lines = []

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

    parse("$foo = $foo + $bar", bar="1")
    ("t1 = t1 + 1", {'foo': 't1', 'bar': '1'})
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

        # if there is a single variable and the to be inserted object
        # is a code block, insert the block with the current indentation level
        if line.startswith("$") and line.count("$") == 1:
            name = line[1:]
            if name in kwargs and isinstance(kwargs[name], CodeBlock):
                kwargs[name].write_into(block, level)
                continue

        block.write_line(string.Template(line).substitute(defdict), level)
    return block, dict(defdict)


def parse_with_objects(code, var, **kwargs):
    """Parse code and include non string/codeblock kwargs as
    dependencies.
    """

    deps = {}
    for key, value in kwargs.items():
        if not isinstance(value, (basestring, CodeBlock)):
            new_var = var()
            deps[new_var] = value
            kwargs[key] = new_var

    block, var = parse_code(code, var, **kwargs)
    for key, dep in deps.iteritems():
        block.add_dependency(key, dep)

    return block, var
