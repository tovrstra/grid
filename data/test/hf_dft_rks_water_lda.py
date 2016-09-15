# -*- coding: utf-8 -*-
# HORTON: Helpful Open-source Research TOol for N-fermion systems.
# Copyright (C) 2011-2016 The HORTON Development Team
#
# This file is part of HORTON.
#
# HORTON is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# HORTON is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --


import sys

from numpy import array, allclose
from nose.plugins.attrib import attr

from horton.context import context


@attr('regression_check')
def test_regression():
    ref_result_kin = 75.86640559819817
    ref_result_hartree = 46.821024094028125
    ref_result_energy = -75.84048710792095
    ref_result_grid = -8.779892993965897
    ref_result_exp_alpha = array([-18.58231551,  -0.89645667,  -0.47394633,  -0.29939112,
        -0.22841871,   0.0452818 ,   0.12825414,   0.76332828,
         0.80243536,   0.83062215,   0.86461713,   1.00423662,
         1.31602462,   1.67066462,   1.67676588,   1.71875151,
         2.2334736 ,   2.52029455])
    ref_result_nn = 9.1571750364299866
    ref_result_ne = -198.90519884261133

    thresholds = {'ref_result_kin': 1e-08, 'ref_result_energy': 1e-08, 'ref_result_grid': 1e-08, 'ref_result_ne': 1e-08, 'ref_result_exp_alpha': 1e-08, 'ref_result_nn': 1e-08, 'ref_result_hartree': 1e-08}

    test_path = context.get_fn("examples/hf_dft/rks_water_lda.py")

    l = {}
    m = locals()
    with open(test_path) as fh:
        exec fh in l

    for k,v in thresholds.items():
        var_name = k.split("ref_")[1]
        assert allclose(l[var_name], m[k], v), (var_name, m[k] - l[var_name])

if __name__ == "__main__":
    test_regression()
