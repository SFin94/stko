"""Module of tests for XTB Optimizers."""
import sys
import pytest
import stk
import os
from os.path import join

from stko import XTB, XTBCREST, XTBFF, XTBFFCREST
from stko import XTBOptimizerError, XTBConvergenceError, CRESTOptimizerError
from stko import CRESTNotStartedError, CRESTNotCompletedError, CRESTSettingConflictError
from.utilities import compare_benzenes

odir = 'xtb_tests_output'
if not os.path.exists(odir):
    os.mkdir(odir)

# Only run tests if xtb executable present.
xtb = pytest.mark.skipif(
    all('xtb_path' not in x for x in sys.argv),
    reason="Only run when explicitly asked."
)

@xtb
def test_optimizer(xtb_path, benzene_build, tmpdir):
    xtb_test_optimizer = XTB(
        xtb_path=xtb_path,
        output_dir=join(odir, 'test_optimizer1'),
        unlimited_memory=True,
        max_runs=1,
        calculate_hessian=True
    )
    opt_benzene = xtb_test_optimizer(benzene_build)
    compare_benzenes(
        initial_molecule=benzene_build,
        optimized_molecule=opt_benzene,
    )

@xtb
def test_no_neg_frequencies(xtb_path, tmpdir):
    """Test negative frequencies are correctly checked for."""
    # Optimize molecule.    
    xtb_test_optimizer = XTB(
        xtb_path=xtb_path,
        output_dir=tmpdir,
        unlimited_memory=True,
        max_runs=1,
        calculate_hessian=True
    )
    opt_benzene = xtb_test_optimizer(benzene_build)
    output_file = tmpdir+'/optimization_1.output'

    # Test for no imgainary frequencies.
    assert xtb_test_optimizer._has_neg_frequencies(output_file) is False

@xtb
def test_neg_frequencies(xtb_path, tmpdir):
    """Test negative frequencies are correctly checked for."""
    # Optimize molecule but with reduced number of cycles.    
    xtb_test_optimizer = XTB(
        xtb_path=xtb_path,
        output_dir=tmpdir,
        unlimited_memory=True,
        max_runs=1,
        cycles=10,
        calculate_hessian=True
    )
    benzene_unopt = xtb_test_optimizer.optimize(benzene_unopt_build)
    output_file = tmpdir+'/optimization_1.output'

    # Test for no imgainary frequencies.
    assert xtb_test_optimizer._has_neg_frequencies(output_file) is True

@xtb
def test_no_output_file(xtb_path):
    """Test correct error raised if no output file created."""   
    # Create XTB instance.
    xtb_test_optimizer = XTB(
        xtb_path=xtb_path,
        unlimited_memory=True,
        max_runs=1,
        calculate_hessian=True
    )
    with pytest.raises(XTBOptimizerError):
        xtb_test_optimizer._is_complete('dummy_output_file')

