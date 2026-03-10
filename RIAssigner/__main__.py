import click

from RIAssigner.cli import create_method, load_data


@click.group()
def main():
    """Command line interface for the RIAssigner library."""
    pass


@main.command()
@click.option('--reference',
              required=True,
              type=(str, str, str),
              help="""Reference dataset containing retention times and indices.
              Path to msp, csv, tsv/tabular or parquet file, filetype and retention time unit.""")
@click.option('--query',
              required=True,
              type=(str, str, str),
              help="""Query dataset for which to compute retention indices.
              Path to msp, csv, tsv/tabular or parquet file, filetype and retention time unit.""")
@click.option('--method',
              required=True,
              type=click.Choice(['kovats', 'cubicspline']),
              help="Computation method for RI.")
@click.option('--output',
              required=True,
              type=str,
              help="Output filename.")
def compute(reference, query, method, output):
    """Compute retention indices for a query dataset using a reference dataset."""
    query_data = load_data(*query)
    reference_data = load_data(*reference)
    method_instance = create_method(method)
    retention_indices = method_instance.compute(query_data, reference_data)
    query_data.retention_indices = retention_indices
    query_data.write(output)


@main.command('ri-from-comment')
@click.option('--query',
              required=True,
              type=(str, str, str),
              help="""Query dataset from which to read retention indices.
              Path to msp, csv, tsv/tabular or parquet file, filetype and retention time unit.""")
@click.option('--ri-source',
              required=True,
              type=str,
              help="Key used in the comment field to identify the retention index value.")
@click.option('--output',
              required=True,
              type=str,
              help="Output filename.")
def ri_from_comment(query, ri_source, output):
    """Read retention indices from the comment field of a query dataset."""
    query_data = load_data(*query)
    query_data.init_ri_from_comment(ri_source)
    query_data.write(output)


if __name__ == "__main__":
    main()
