from RIAssigner.data import MatchMSData, PandasData


def load_data(filename, filetype, rt_unit):
    """Load data from file and create a Data instance.

    Parameters
    ----------
    filename : str
        Path to the data file.
    filetype : str
        Type of the data file. Supported types are 'msp', 'csv', 'tsv', 'tabular', 'parquet'.
    rt_unit : str
        Retention time unit.

    Returns
    -------
    Data
        Data instance.
    """
    if filetype == "msp":
        return MatchMSData(filename, filetype, rt_unit)
    elif filetype in ["csv", "tsv", "tabular", "parquet"]:
        return PandasData(filename, filetype, rt_unit)
    else:
        raise ValueError(f"Unsupported file type: {filetype}. Supported types are 'msp', 'csv', 'tsv', 'tabular' and 'parquet'.")
