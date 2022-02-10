import sys
from RIAssigner.compute.ComputationMethod import ComputationMethod
import argparse

from RIAssigner.cli import CreateMethodAction, LoadDataAction
from RIAssigner.data import Data


def create_parser():
    parser = argparse.ArgumentParser(prog="RIAssigner")

    required = parser.add_argument_group("required arguments")

    required.add_argument("--reference",
                          required=True,
                          type=str,
                          action=LoadDataAction,
                          nargs=3,
                          help="""Reference dataset containing retention times and indices.
                          Path to CSV or MSP, filetype and retention time unit.""")
    required.add_argument("--query",
                          required=True,
                          type=str,
                          action=LoadDataAction,
                          nargs=3,
                          help="""Query dataset for which to compute retention indices.
                          Path to CSV or MSP, filetype and retention time unit.""")
    required.add_argument("--method",
                          required=True,
                          type=str,
                          action=CreateMethodAction,
                          choices=['kovats', 'cubicspline'],
                          help="Computation method for RI.")
    required.add_argument("--output",
                          required=True,
                          type=str,
                          help="Output filename.")
    return parser


def main(argv):
    """Command line interface for the RIAssigner library.

    Args:
        argv (List[string]): Arguments passed to the program
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    query: Data = args.query
    reference: Data = args.reference
    method: ComputationMethod = args.method

    retention_indices = method.compute(query, reference)
    query.retention_indices = retention_indices

    query.write(args.output)
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
