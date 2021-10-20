"""
Github Secrets Filler
__autbhor__ Pierre PATAKI <ppataki __AT__ sdv.fr>
"""

import argparse

from libraries.filler.Filler import Filler

# Rock'n'roll
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            'Import dotenv files to Github Projects '
            'Environments as Secret Variables'
        )
    )

    parser.add_argument(
        '-f', '--file',
        dest='dotenv_file',
        help='path to the input dotenv file',
        required=True
    )

    parser.add_argument(
        '-p', '--project',
        dest='repository_name',
        help='path to the github repository. Ex: ArteGEIE/my-project',
        required=True
    )

    parser.add_argument(
        '-e', '--env',
        dest='environment',
        help='targeted environment\'s name',
        required=True
    )

    parser.add_argument(
        '-k', '--token',
        dest='github_token',
        help=(
            'Github API Token. Can be given through GITHUB_TOKEN '
            'environment variable.'
        ),
        required=False
    )

    args = parser.parse_args()

    print(
        f"Pushing {args.dotenv_file} to {args.repository_name} in Environment {args.environment} ..."
    )

    f = Filler(args)
    f.create_secrets()
