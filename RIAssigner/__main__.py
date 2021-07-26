from RIAssigner.compute.ComputationMethod import ComputationMethod
import argparse

from RIAssigner.cli import CreateMethodAction, LoadDataAction
from RIAssigner.data import Data


def create_parser():
    parser = argparse.ArgumentParser(prog="RIAssigner")

    parser.add_argument("--reference",
                        required=True,
                        type=str,
                        action=LoadDataAction,
                        help="Reference dataset containing retention times and indices. Path to CSV or MSP.")
    parser.add_argument("--query",
                        required=True,
                        type=str,
                        action=LoadDataAction,
                        help="Query dataset for which to compute retention indices. Path to CSV or MSP.")
    parser.add_argument("--method",
                        required=True,
                        type=str,
                        action=CreateMethodAction,
                        choices=['kovats', 'cubiscpline'],
                        help="Computation method for RI.")
    parser.add_argument("--output",
                        required=True,
                        type=str,
                        help="Output filename.")
    return parser


def main():
    """Command line interface for the RIAssigner library.

    Args:
        argv (List[string]): Arguments passed to the program
    """
    parser = create_parser()
    args = parser.parse_args()

    query: Data = args.query
    reference: Data = args.reference
    method: ComputationMethod = args.method

    retention_indices = method.compute(query, reference)
    query.retention_indices = retention_indices

    query.write(args.output)
    return 0


if __name__ == "__main__":
    main()
