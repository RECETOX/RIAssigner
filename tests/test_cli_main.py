import os

import pytest
from click.testing import CliRunner

from RIAssigner.__main__ import compute, main, ri_from_comment

here = os.path.abspath(os.path.dirname(__file__))
testdata_dir = os.path.join(here, "data")


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def reference_msp():
    return os.path.join(testdata_dir, "msp", "Alkanes_20210325.msp")


@pytest.fixture
def query_csv():
    return os.path.join(testdata_dir, "csv", "aplcms_aligned_peaks.csv")


@pytest.fixture
def query_csv_with_ri_in_comment():
    return os.path.join(testdata_dir, "ri_from_comment", "nist_to_ri_2mols.csv")


def test_compute_command(runner, tmp_path, reference_msp, query_csv):
    output = str(tmp_path / "output.csv")
    result = runner.invoke(
        compute,
        [
            "--reference",
            reference_msp,
            "msp",
            "min",
            "--query",
            query_csv,
            "csv",
            "min",
            "--method",
            "kovats",
            "--output",
            output,
        ],
    )
    assert result.exit_code == 0, result.output
    assert os.path.exists(output)


def test_compute_missing_reference_raises_error(runner, tmp_path, query_csv):
    output = str(tmp_path / "output.csv")
    result = runner.invoke(
        compute,
        [
            "--query",
            query_csv,
            "csv",
            "min",
            "--method",
            "kovats",
            "--output",
            output,
        ],
    )
    assert result.exit_code != 0
    assert "reference" in result.output


def test_compute_missing_method_raises_error(
    runner, tmp_path, reference_msp, query_csv
):
    output = str(tmp_path / "output.csv")
    result = runner.invoke(
        compute,
        [
            "--reference",
            reference_msp,
            "msp",
            "min",
            "--query",
            query_csv,
            "csv",
            "min",
            "--output",
            output,
        ],
    )
    assert result.exit_code != 0
    assert "method" in result.output


def test_ri_from_comment_command(runner, tmp_path, query_csv_with_ri_in_comment):
    output = str(tmp_path / "output.csv")
    # 'SemiStdNP' is the key used in comment fields to store semi-standard non-polar RI values
    result = runner.invoke(
        ri_from_comment,
        [
            "--query",
            query_csv_with_ri_in_comment,
            "csv",
            "seconds",
            "--ri-source",
            "SemiStdNP",
            "--output",
            output,
        ],
    )
    assert result.exit_code == 0, result.output
    assert os.path.exists(output)


def test_ri_from_comment_missing_query_raises_error(runner, tmp_path):
    output = str(tmp_path / "output.csv")
    result = runner.invoke(
        ri_from_comment,
        [
            "--ri-source",
            "SemiStdNP",
            "--output",
            output,
        ],
    )
    assert result.exit_code != 0
    assert "query" in result.output


def test_main_group_lists_subcommands(runner):
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "compute" in result.output
    assert "ri-from-comment" in result.output
