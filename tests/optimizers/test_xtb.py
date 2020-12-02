import sys
import pytest
import stk

from stko import XTB, XTBCREST, XTBFF, XTBFFCREST
from stko import XTBOptimizerError, XTBConvergenceError, CRESTOptimizerError
from stko import CRESTNotStartedError, CRESTNotCompletedError, CRESTSettingConflictError

# Only run tests if xtb executable present.
xtb = pytest.mark.skipif(
    all('xtb_path' not in x for x in sys.argv),
    reason="Only run when explicitly asked."
)


@xtb
def test_no_neg_frequencies(xtb_path, tmpdir):
    """Test negative frequencies are correctly checked for."""
    # Create benzene molecule.
    benzene_unopt = stk.BuildingBlock(smiles='c1ccccc1')
    # Optimize molecule.    
    xtb_test = XTB(
        xtb_path=xtb_path,
        output_dir=tmpdir,
        unlimited_memory=True,
        max_runs=1,
        calculate_hessian=True
    )
    benzene_opt = xtb_test.optimize(benzene_unopt)
    output_file = tmpdir+'/optimization_1.output'

    # Test for no imgainary frequencies.
    assert xtb_test._has_neg_frequencies(output_file) is False

@xtb
def test_no_neg_frequencies(xtb_path, tmpdir):
    """Test negative frequencies are correctly checked for."""
    # Create benzene molecule that will not optimise to min.
    benzene_unopt = stk.BuildingBlock(smiles='c1ccccc1')    
    new_pos_mat = benzene_unopt.get_position_matrix()
    new_pos_mat[1] = [4, 4, 4]
    benzene_unopt = benzene_unopt.with_position_matrix(new_pos_mat)
    # Optimize molecule but with reduced number of cycles.    
    xtb_test = XTB(
        xtb_path=xtb_path,
        output_dir=tmpdir,
        unlimited_memory=True,
        max_runs=1,
        cycles=10,
        calculate_hessian=True
    )
    benzene_opt = xtb_test.optimize(benzene_unopt)
    output_file = tmpdir+'/optimization_1.output'

    # Test for no imgainary frequencies.
    assert xtb_test._has_neg_frequencies(output_file) is True

@xtb
def test_no_output_file(xtb_path):
    """Test correct error raised if no output file created."""   
    # Create XTB instance.
    xtb_test = XTB(
        xtb_path=xtb_path,
        unlimited_memory=True,
        max_runs=1,
        calculate_hessian=True
    )
    with pytest.raises(XTBOptimizerError):
        xtb_test._is_complete('fake_output_file')

@xtb
def test_not_converged(xtb_path, tmpdir):
    """Test correct error raised if no output file created."""   
    # Create benzene molecule that will not optimise to min.
    benzene_unopt = stk.BuildingBlock(smiles='c1ccccc1')    
    new_pos_mat = benzene_unopt.get_position_matrix()
    new_pos_mat[1] = [4, 4, 4]
    benzene_unopt = benzene_unopt.with_position_matrix(new_pos_mat)
    # Optimize molecule but with reduced number of cycles.    
    xtb_test = XTB(
        xtb_path=xtb_path,
        output_dir=tmpdir,
        unlimited_memory=True,
        max_runs=1,
        cycles=10,
        calculate_hessian=True
    )
    benzene_opt = xtb_test.optimize(benzene_unopt)
    output_file = tmpdir+'/optimization_1.output'
    
    with pytest.raises(XTBOptimizerError):
        xtb_test._is_complete('fake_output_file')
