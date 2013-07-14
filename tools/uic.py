#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the BipComposer project.
# Copyright (C) 2013 Morwenn
# Contact: Morwenn <morwenn29@hotmail.fr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA

import logging
import os
from distutils.cmd import Command
from distutils.core import DistutilsOptionError


# Ugly hacks with global variables
read_resources = True
import_module = ''

class CompileUI(Command):
    """Build PySide (.ui) files and resources."""

    description = "build PySide Qt GUIs (.ui)."

    user_options = [
        ('no-read-resources', 'R', 'Whether to take in account the .qrc files'),
        ('import-module=', 'r', 'Additional module to import'),
        ('input-dir=', 'i', 'Input directory path where to search \'.ui\' files.'),
        ('output-dir=', 'o', 'Output directory path for the generated UI files.'),
        ('indent=', 'I', 'set indent width to N spaces, tab if N is 0 (default: 4)'),
        ('i18n-module', 'm', 'specify from which module the \'_()\' function '
                             'should be imported. Ex: mymodule.i18n'),
        ('ui-execute', 'x', 'generate extra code to test and display the class'),
        ('from-imports', 'F', 'generate imports relative to \'.\'')
    ]
    boolean_options = ['from-imports', 'ui-execute', 'no-read-resources']

    def initialize_options(self):
        self.no_read_resources = False
        self.input_dir = None
        self.output_dir = None
        self.indent = 4
        self.i18n_module = None
        self.ui_execute = False
        self.from_imports = False
        self.import_module = ''

    def finalize_options(self):
        if self.input_dir is None:
            self.input_dir = '.'
        if self.output_dir is None:
            self.output_dir = '.'
        global read_resources
        read_resources = not self.no_read_resources
        global import_module
        import_module = self.import_module

    def run(self):
        for filename in os.listdir(self.input_dir):
            fpath = os.path.join(self.input_dir, filename)
            if not os.path.isfile(fpath):
                continue
            elif not filename.endswith('.ui'):
                continue
            self.compile_ui(fpath)


    def compile_ui(self, ui_file, py_file=None):
        """Compile the .ui files to python modules."""
        self._wrapuic(i18n_module=self.i18n_module)
        if py_file is None:
            py_file = os.path.join(
                self.output_dir,
                os.path.basename(ui_file).replace('.ui', '_ui.py')
            )

        fi = open(ui_file, 'r')
        fo = open(py_file, 'wt')
        try:
            from pysideuic import compileUi
            compileUi(fi, fo, execute=self.ui_execute, indent=self.indent,
                      from_imports=self.from_imports)
            logging.info("Compiled %s into %s", ui_file, py_file)
        except ImportError:
            logging.warn("You need to have pyside-tools installed in order to "
                     "compile .ui files.")
        except Exception as err:
            logging.warn("Failed to generate %r from %r: %s", py_file, ui_file, err)
            if not os.path.exists(py_file) or not not open(py_file).read():
                raise SystemExit(1)
            return
        finally:
            fi.close()
            fo.close()

    _wrappeduic = False
    @classmethod
    def _wrapuic(cls, i18n_module=None):
        """Wrap uic to use gettext's _() in place of tr()"""
        if cls._wrappeduic:
            return

        try:
            from pysideuic.Compiler import compiler, qtproxies, indenter

            class _UICompiler(compiler.UICompiler):
                """Specialised compiler for qt .ui files."""
                def createToplevelWidget(self, classname, widgetname):
                    o = indenter.getIndenter()
                    o.level = 0
                    if i18n_module:
                        o.write('from %s import _' % i18n_module)
                    return super().createToplevelWidget(
                        classname, widgetname
                    )
                def readResources(self, elem):
                    if read_resources:
                        super().readResources(elem)
                    if import_module:
                        self.resources.append(import_module)
            compiler.UICompiler = _UICompiler

            class _i18n_string(qtproxies.i18n_string):
                """Provide a translated text."""
                def __str__(self):
                    return "_('%s')" % self.string

            qtproxies.i18n_string = _i18n_string

            cls._wrappeduic = True
        except ImportError:
            logging.warn("You need to have pyside-tools installed in order to "
                         "compile .ui files.")


# If main, run the compiler
if __name__ == '__main__':

    from distutils.core import setup

    setup(
        cmdclass = { 'build' : CompileUI }
    )
