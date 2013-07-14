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

import argparse
import fileinput
import os
import shutil
import subprocess
import sys


def make_pot(output=None):
    """
    Search all the calls to the function _()
    and create the template .pot file.
    """
    # Directory where to look for the Python files
    input_dir = os.path.join('.', 'bipcomposer')
    input_dir = os.path.abspath(input_dir)
    
    # Output file
    if not output:
        output = os.path.join('.', 'bipcomposer',
                              'locale', 'bipcomposer.pot')
    output = os.path.abspath(output)
    
    input_files = []
    # Recursively find all the .py files in the project
    for root, dirs, files in os.walk(input_dir):
        for f in files:
            if f.endswith('.py'):
                f = os.path.join(root, f)
                input_files.append(f)
    
    if not input_files:
        print("There are no files to translate.")
        sys.exit(1)
    
    # xgettext is a standard Unix tool.
    # If the platform is Windows, the embedded xgettext.exe
    # will be used instead
    if os.name == 'nt':
        util = os.path.join('tools', 'win32', 'xgettext.exe')
    else:
        util = 'xgettext'
        
    args = [util, '-o', output] + input_files
    subprocess.call(args)
    
    # Change CHARSET to UTF-8
    for line in fileinput.input(output, inplace=1):
        if 'CHARSET' in line:
            line = line.replace('CHARSET', 'UTF-8')
        print(line, end='')


def make_po(input_file=None, locale_dir=None):
    """
    Search for the template .pot file and create
    the .po files for the given languages.
    """
    # Root directory for the locale files
    if not locale_dir:
        locale_dir = os.path.join('.', 'bipcomposer', 'locale')
    locale_dir = os.path.abspath(locale_dir)
    
    # Template .pot file
    if not input_file:
        input_file = os.path.join(locale_dir, 'bipcomposer.pot')
    # Name of the file, without its path or extension
    input_fname = os.path.splitext(os.path.split(input_file)[1])[0]

    # msgmerge is a standard Unix tool.
    # If the platform is Windows, the embedded msgmerge.exe
    # will be used instead
    if os.name == 'nt':
        util = os.path.join('tools', 'win32', 'msgmerge.exe')
    else:
        util = 'msgmerge'

    # Recursively find all the .py files in the project
    for root, dirs, files in os.walk(locale_dir):
        if os.path.split(root)[1] == 'LC_MESSAGES':
            fout = os.path.join(root, input_fname + '.po')
            if not os.path.exists(fout):
                # Copy the .pot file if there is not
                # any corresponding .po file
                shutil.copyfile(input_file, fout)
            else:
                # Merge the .pot and .po files
                args = [util, '--no-wrap', '-U', fout, input_file]
                subprocess.call(args)


def make_locale(locale_dir=None):
    """
    Create the locale files .pot and .po files for
    the whole project.
    """
    try:
        make_pot()
    except:
        sys.exit(1)
    make_po(locale_dir)


def make_mo(locale_dir=None):
    """
    Compile the .po files to compiled binary .mo
    files.
    """
    # Root directory for the locale files
    if not locale_dir:
        locale_dir = os.path.join('.', 'bipcomposer', 'locale')
    locale_dir = os.path.abspath(locale_dir)

    # msgfmt is a standard Unix tool.
    # If the platform is Windows, the embedded msgfmt.exe
    # will be used instead
    if os.name == 'nt':
        util = os.path.join('tools', 'win32', 'msgfmt.exe')
    else:
        util = 'msgfmt'

    # Recursively find all the .py files in the project
    for root, dirs, files in os.walk(locale_dir):
        for f in files:
            if f.endswith('.po'):
                fname = os.path.splitext(f)[0]
                mo_file = os.path.join(root, fname + '.mo')

                # Turns .po files into .mo files
                # thanks to msgfmt
                args = [util, '-o', mo_file, os.path.join(root, f)]
                subprocess.call(args)


def make_icons(icons_dir=None):
    """
    Create a .qrc with all the icons in the icons_dir
    directory then embed them in a Python file.
    This function requires pyside-rcc, embedded with PySide.
    """
    # Root directory for the icons
    if not icons_dir:
        icons_dir = os.path.join('.', 'bipcomposer', 'icons')

    # Recursively find all the .png files in the icons directory
    icons = []
    for root, dirs, files in os.walk(icons_dir):
        for f in files:
            if f.endswith('.png'):
                fname = os.path.join('icons', f)
                icons.append(fname)

    # Create a Qt resource file (.qrc)
    qrc_file = os.path.join('bipcomposer', 'icons.qrc')
    with open(qrc_file, 'w') as f:
        f.write('<!DOCTYPE RCC><RCC version="1.0">\n'
                '<qresource>\n')
        for ic in icons:
            f.write('<file>%s</file>\n' % ic)
        f.write('</qresource>\n'
                '</RCC>\n')

    # Compile the resource file in a Python file
    output_file = os.path.join('bipcomposer', 'icons', '__init__.py')
    args = ['pyside-rcc', '-py3', '-o', output_file, qrc_file]
    subprocess.call(args)


def make_doc(target):
    """
    Forward the documentation creation to the Sphinx
    documentation builder which should be in the
    directory doc.
    """
    os.chdir('doc')
    args = ['make', target]
    subprocess.call(args)


def make_exe():
    """
    Call python setup.py build to generate the
    stand-alone executable.
    """
    if not os.path.exists(os.path.join('.', 'setup.py')):
        print("Can not find file ./setup.py")
        sys.exit(1)
    args = ['python', 'setup.py', 'build']
    subprocess.call(args)


def make_installer():
    """
    Call python setup.py build to generate the
    installer (Windows only).
    """
    if not os.path.exists(os.path.join('.', 'setup.py')):
        print("Can not find file ./setup.py")
        sys.exit(1)
    if os.name != "nt":
        print("The installer generation only works with Window")
        sys.exit(1)
    args = ['python', 'setup.py', 'bdist_msi']
    subprocess.call(args)


def make_gui(input_dir=None, output_dir=None, icons=None):
    """
    Call the script that can compile the .ui files to .py files
    while generating gettext-compatible translation functions.
    """
    # Generate the .py files
    gen_dir = os.path.join('bipcomposer', 'gui', 'generated')
    if not input_dir:
        input_dir = gen_dir
    if not output_dir:
        output_dir = gen_dir
    if not icons:
        icons = os.path.join('bipcomposer', 'icons.qrc')
    util = os.path.join('tools', 'uic.py')
    args = ['python', util, 'build',
            '-i', input_dir,
            '-o', output_dir,
            '-r', 'bipcomposer.icons',
            '-R']
    subprocess.call(args)

    # Generate the __init__.py file
    init_file = os.path.join(input_dir, '__init__.py')
    with open(init_file, 'w') as f:
        # Write the shebang and the encoding note
        f.write("#!/usr/bin/env python\n"
                "# -*- coding: utf-8 -*-\n"
                "\n")

        elems = []
        for fname in os.listdir(input_dir):
            if fname.endswith('.py') and fname != '__init__.py':
                fname = fname.split('.')[0]
                tmp = 'Ui_' + fname[:-3]
                # Write the import directives
                f.write("from .%(file)s import %(name)s\n" % {
                    "file" : fname,
                    "name" : tmp
                })
                elems.append(tmp)

        # Fill the variable __all__
        f.write("\n\n"
                "__all__ = [")
        for elem in elems:
            f.write("'%s', " % elem)
        f.write("]\n")



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Generate files for BipComposer')
    subparsers = parser.add_subparsers()
    
    # Create subparsers
    parser_pot = subparsers.add_parser('pot', help='Generate the template .pot file',
                                       description='Generate the template .pot file')
    parser_po = subparsers.add_parser('po', help='Create or merge the traduction .po files',
                                      description='Create or merge the traduction .po files')
    parser_locale = subparsers.add_parser('locale', help='Generate the locale files',
                                          description='Generate the locale files')
    parser_mo = subparsers.add_parser('mo', help='Compile the .po to .mo binary files',
                                      description='Compile the .po to .mo binary files')
    parser_icons = subparsers.add_parser('icons', help='Compile the icon files',
                                         description='Compile the icon files')
    parser_doc = subparsers.add_parser('doc', help='Generate the developer documentation',
                                       description='Generate the developer documentation')
    parser_exe = subparsers.add_parser('exe', help='Generate the executable',
                                       description='Generate the executable')
    parser_installer = subparsers.add_parser('installer', help='Generate the installer (Windows only)',
                                       description='Generate the intaller')
    parser_gui = subparsers.add_parser('gui', help='Compile the .ui files to .py files',
                                       description='Compile the .ui files to .py files')

    # Configure pot parsing
    parser_pot.add_argument('-o', '--output',
                            help='write output to specified file')
    parser_pot.set_defaults(func=make_pot)

    # Configure po parsing
    parser_po.add_argument('-i', '--input-file',
                           help='Template file to merge to the .po files')
    parser_po.add_argument('-d', '--locale-dir',
                           help='specify the root of the locale directory')
    parser_po.set_defaults(func=make_po)

    # Configure locale parsing
    parser_locale.add_argument('-d', '--locale-dir',
                               help='specify the root of the locale directory')
    parser_locale.set_defaults(func=make_locale)

    # Configure mo parsing
    parser_mo.add_argument('-d', '--locale-dir',
                           help='specify the root of the locale directory')
    parser_mo.set_defaults(func=make_mo)

    # Configure the icons compilation
    parser_icons.add_argument('-d', '--icons-dir',
                               help='specify the icons directory')
    parser_icons.set_defaults(func=make_icons)

    # Configure the documentation parsing
    parser_doc.add_argument('target',
                            help='Target to build. See Sphinx documentation.')
    parser_doc.set_defaults(func=make_doc)
    
    # Configure the program generation
    parser_exe.set_defaults(func=make_exe)

    # Configure the installer generation
    parser_installer.set_defaults(func=make_installer)
    
    # Configure the gui files generation
    parser_gui.set_defaults(func=make_gui)
    parser_gui.add_argument('-i', '--input-dir',
                            help='directory where are stored the .ui files')
    parser_gui.add_argument('-o', '--output-dir',
                            help='Directory where will be generated the .py files.')
    parser_gui.add_argument('-ic', '--icons',
                            help='.qrc files describing the icons.')    
    
    if len(sys.argv) == 1:
        # If no arguments are given, print help
        parser.print_help()
    else:
        # Invoque the required function with the given args
        args = parser.parse_args()
        func = args.func
        delattr(args, 'func')
        func(**vars(args))


    