import click

from RIAssigner.cli import create_method, load_data


@click.command()
@click.option('--reference',
              required=False,
              default=None,
              type=(str, str, str),
              help="""Reference dataset containing retention times and indices.
              Path to msp, csv, tsv/tabular or parquet file, filetype and retention time unit.""")
@click.option('--query',
              required=True,
              type=(str, str, str),
              help="""Query dataset for which to compute retention indices.
              Path to msp, csv, tsv/tabular or parquet file, filetype and retention time unit.""")
@click.option('--method',
              required=False,
              default=None,
              type=click.Choice(['kovats', 'cubicspline']),
              help="Computation method for RI.")
@click.option('--output',
              required=True,
              type=str,
              help="Output filename.")
@click.option('--ri_from_comment',
              default=None,
              type=str,
              help="Extract retention index from comment field using this key.")
def main(reference, query, method, output, ri_from_comment):
    """Command line interface for the RIAssigner library."""
    query_data = load_data(*query)

    if ri_from_comment:
        query_data.init_ri_from_comment(ri_from_comment)
    else:
        if not reference or not method:
            raise click.UsageError(
                "Either --ri_from_comment or both --reference and --method must be provided."
            )
        reference_data = load_data(*reference)
        method_instance = create_method(method)
        retention_indices = method_instance.compute(query_data, reference_data)
        query_data.retention_indices = retention_indices

    query_data.write(output)


if __name__ == "__main__":
    main()
