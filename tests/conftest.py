import pytest
import os
import stk


@pytest.fixture
def benzene_build():
    """Benzene fixture with distorted geometry."""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    benzene = os.path.join(current_directory, "benzene.mol")
    mol = stk.BuildingBlock.init_from_file(benzene)

    return mol

@pytest.fixture
def benzene_unopt_build():
    """Benzene fixture with largely distorted geometry."""
    # Would be good to make this consistent with above.
    unopt_mol = stk.BuildingBlock(smiles='c1ccccc1')    
    new_pos_mat = unopt_mol.get_position_matrix()
    new_pos_mat[1] = [4, 4, 4]
    unopt_mol = unopt_mol.with_position_matrix(new_pos_mat)

    return unopt_mol

def pytest_addoption(parser):
    parser.addoption('--macromodel_path', default='')
    parser.addoption('--mopac_path', default='')
    parser.addoption('--xtb_path', default='')
    parser.addoption('--gulp_path', default='')

def pytest_generate_tests(metafunc):
    if 'macromodel_path' in metafunc.fixturenames:
        mm_path = metafunc.config.getoption('macromodel_path')
        metafunc.parametrize('macromodel_path', [mm_path])
    if 'mopac_path' in metafunc.fixturenames:
        mopac_path = metafunc.config.getoption('mopac_path')
        metafunc.parametrize('mopac_path', [mopac_path])
    if 'xtb_path' in metafunc.fixturenames:
        xtb_path = metafunc.config.getoption('xtb_path')
        metafunc.parametrize('xtb_path', [xtb_path])
    if 'gulp_path' in metafunc.fixturenames:
        gulp_path = metafunc.config.getoption('gulp_path')
        metafunc.parametrize('gulp_path', [gulp_path])
    # elif 'macromodel_path' in metafunc.fixturenames:
    #     macromodel_path = metafunc.config.getoption('macromodel_path')
    #     metafunc.parametrize('macromodel_path', [macromodel_path])
