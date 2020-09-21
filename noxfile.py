import os
from pathlib import Path

import nox


_HERE = Path(__file__).absolute().parent
_TEST_DIR = _HERE/'test'
_DOC_DIR = _HERE/'doc'
# Locally we have nox handle the different versions, but in each travis run there is only a single python which can always be found as just 'python'
_PY_VERSIONS = ['3.9', '3.8', '3.7', '3.6'] if not os.environ.get("TRAVIS_PYTHON_VERSION") else ['python']


@nox.session(python=_PY_VERSIONS, reuse_venv=True)
def test(session):
    session.install('.')
    session.install('-r', str(_TEST_DIR/'requirements.txt'))
    cov_rc_file_name = '.coverage_rc'  # The rcfile path is duplicated in .travis.yml
    session.run('pytest', '--capture=sys', '--cov', '--cov-report=term-missing', f'--cov-config={_TEST_DIR}/{cov_rc_file_name}', *session.posargs)


@nox.session(python=_PY_VERSIONS, reuse_venv=True)
def examples(session):
    session.install('-e', '.')
    session.run('python', '-m', 'compileall', str(_HERE/'examples/result.py'))
