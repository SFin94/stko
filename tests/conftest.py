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

