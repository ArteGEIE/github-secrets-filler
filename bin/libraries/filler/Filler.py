"""
Wrapper Class for the Github Secrets Filler
"""

import os
import sys

import dotenv
import github

from ..GithubEnvironmentSecret import GithubEnvironmentSecret

class Filler:

    dotenv_values=None
    github_repository=None
    environment=None
    gh_env_secret=None

    def __init__(self, args):
        '''
        Filler Constructor, takes parsed arguments from the cmd
        '''

        self.load_api_token(args)
        self.load_dotenv_values(args.dotenv_file)
        self.load_github_repository(args.repository_name)
        self.load_environment(args.environment)
        self.load_github_environment_secret()

    def load_github_environment_secret(self):
        '''
        '''

        self.gh_env_secret = GithubEnvironmentSecret(
            repository_id=self.github_repository.id,
            environment=self.environment
        )

    def load_api_token(self, args):
        '''
        Handle the GITHUB_TOKEN environment variable
        Exits the program if not found
        '''

        if args.github_token:
            os.environ["GITHUB_TOKEN"] = args.github_token
        
        if not os.getenv('GITHUB_TOKEN'):
            print("Could not retrieve GITHUB_TOKEN")
            sys.exit(1)

    def load_dotenv_values(self, dotenv_file):
        '''
        Load the values from the dotenv_file
        '''

        if not os.path.isfile(dotenv_file):
            print(f"Could not open DOTENV file {dotenv_file}")
            sys.exit(1)
        
        try:
            self.dotenv_values = dotenv.dotenv_values(dotenv_file)
        
        except Exception as exception:
            print(f"Could not load DOTENV file : {str(exception)}")
            sys.exit(1)
    
    def load_github_repository(self, repository_name):
        '''
        Try to fetch the Github Repository with the Token
        '''

        github_connector = github.Github(os.getenv("GITHUB_TOKEN"))

        try:
            self.github_repository = github_connector \
                .get_repo(repository_name)

        except github.GithubException as exception:
            print(
                f"Could not retrieve Repository {repository_name} : "
                f"{str(exception)}"
            )
            sys.exit(1)

    def load_environment(self, environment):
        '''
        Load the environment name
        '''

        self.environment = environment

    def create_secrets(self):
        '''
        Creates or updates secrets for Project Environment
        '''

        for dotenv_key in self.dotenv_values:
            dotenv_val = self.dotenv_values[dotenv_key]

            if self.gh_env_secret.secret_exists(dotenv_key):
                print(f" » Updating {dotenv_key} ...")

            else:
                print(f" » Creating {dotenv_key} ...")

            self.gh_env_secret.add_secret(
                key=dotenv_key,
                value=dotenv_val
            )
