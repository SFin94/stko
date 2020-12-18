import pytest
import os

import stk


@pytest.fixture
def benzene_build():
    """Benzene fixture with slightly distorted geometry."""
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