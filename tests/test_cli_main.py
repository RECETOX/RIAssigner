import os

import pytest
from click.testing import CliRunner

from RIAssigner.__main__ import main

here = os.path.abspath(os.path.dirname(__file__))
testdata_dir = os.path.join(here, 'data')


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def reference_msp():
    return os.path.join(testdata_dir, 'msp', 'Alkanes_20210325.msp')


@pytest.fixture
def query_csv():
    return os.path.join(testdata_dir, 'csv', 'aplcms_aligned_peaks.csv')


@pytest.fixture
def query_csv_with_ri_in_comment():
    return os.path.join(testdata_dir, 'ri_from_comment', 'nist_to_ri_2mols.csv')


def test_main_with_reference_and_method(runner, tmp_path, reference_msp, query_csv):
    output = str(tmp_path / "output.csv")
    result = runner.invoke(main, [
        '--reference', reference_msp, 'msp', 'min',
        '--query', query_csv, 'csv', 'min',
        '--method', 'kovats',
        '--output', output,
    ])
    assert result.exit_code == 0, result.output
    assert os.path.exists(output)


def test_main_with_ri_from_comment(runner, tmp_path, query_csv_with_ri_in_comment):
    output = str(tmp_path / "output.csv")
    # 'SemiStdNP' is the key used in comment fields to store semi-standard non-polar RI values
    result = runner.invoke(main, [
        '--query', query_csv_with_ri_in_comment, 'csv', 'seconds',
        '--ri_from_comment', 'SemiStdNP',
        '--output', output,
    ])
    assert result.exit_code == 0, result.output
    assert os.path.exists(output)


def test_main_missing_reference_and_method_raises_error(runner, tmp_path, query_csv):
    output = str(tmp_path / "output.csv")
    result = runner.invoke(main, [
        '--query', query_csv, 'csv', 'min',
        '--output', output,
    ])
    assert result.exit_code != 0
    assert "Either --ri_from_comment or both --reference and --method must be provided" in result.output


def test_main_missing_query_raises_error(runner, tmp_path):
    output = str(tmp_path / "output.csv")
    result = runner.invoke(main, [
        '--output', output,
    ])
    assert result.exit_code != 0
