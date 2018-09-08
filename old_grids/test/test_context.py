# -*- coding: utf-8 -*-
# OLDGRIDS: Helpful Open-source Research TOol for N-fermion systems.
# Copyright (C) 2011-2017 The OLDGRIDS Development Team
#
# This file is part of OLDGRIDS.
#
# OLDGRIDS is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# OLDGRIDS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --


import os
import subprocess

from old_grids import context
from old_grids.test.common import in_horton_source_root


def test_context():
    fn = context.get_fn('basis/sto-3g.nwchem')
    assert os.path.isfile(fn)
    fns = context.glob('basis/*.nwchem')
    assert fn in fns


def test_data_files():
    # Find files in data that were not checked in.
    # This test only makes sense if ran inside the source tree. The purpose is
    # to detect mistakes in the development process.
    if context.data_dir == os.path.abspath('data/') and os.path.isdir('.git'):
        lines = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard',
                                         'data']).decode("utf-8").split('\n')
        for line in lines:
            line = line.strip()
            if len(line) != 0:
                raise ValueError('The following file is not checked in: %s' % line)


def test_shebang():
    # Make sure that all executable python modules, in the data and
    # scripts directories have a proper shebang line.
    def iter_py_files(root):
        for dn, subdns, fns in os.walk(root):
            for fn in fns:
                if fn.endswith('.py'):
                    yield os.path.join(dn, fn)

    # Collect all bad files
    bad = []

    # Loop over all py files in datadir:
    for fn_py in iter_py_files(context.data_dir):
        if os.access(fn_py, os.X_OK):
            with open(fn_py) as f:
                if next(f) != '#!/usr/bin/env python\n':
                    bad.append(fn_py)

    # Loop over all py files in scripts, if testing from the development root:
    if in_horton_source_root():
        for fn_py in iter_py_files('scripts'):
            assert os.access(fn_py, os.X_OK), 'Py Files in scripts/ must be executable.'
            with open(fn_py) as f:
                if next(f) != '#!/usr/bin/env python\n':
                    bad.append(fn_py)

    if len(bad) > 0:
        print('The following files have an incorrect shebang line:')
        for fn in bad:
            print(('   ', fn))
        raise AssertionError('Some Python scripts have an incorrect shebang line.')