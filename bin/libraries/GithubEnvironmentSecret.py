"""
Wrapper Class for the Github Secrets Filler
"""

import urllib3
import os
import json
import sys

from base64 import b64encode
from nacl import encoding, public


class GithubEnvironmentSecret:

    __repository_id = None
    __environment = None
    __github_api_endpoint = "https://api.github.com"
    __env_secret_key = None

    def __init__(self, repository_id: int, environment: str):
        '''
        GithubEnvironmentSecret Constructor
        Takes the Repository ID and Environment Name
        '''

        self.__repository_id = repository_id
        self.__environment = environment

        if not self.__environment_exists():
            print(
                f"Could not retrieve Environment {environment}"
            )
            sys.exit(1)

        else:
            self.__env_secret_key = self.__retrieve_secret_key()

    def __call_github(self, endpoint: str, verb: str, body=None):
        '''
        Wrapper for API Calls to Github APIv3
        Made because some actions are not yet implemented into pygithub
        https://docs.github.com/en/rest/reference/actions
        '''

        user_agent = {'user-agent': 'github-secrets-filler/0.1 (Docker)'}
        http = urllib3.PoolManager(10, headers=user_agent)
        url = f"{self.__github_api_endpoint}{endpoint}"
        headers = {
            'Accept': "application/vnd.github.v3+json",
            'Authorization': f"Bearer {os.getenv('GITHUB_TOKEN', 'NONE')}",
            'Content-Type': "application/json"
        }

        if body:
            resp = http.request(
                verb.upper(),
                url,
                headers=headers,
                body=json.dumps(body)
            )

        else:
            resp = http.request(
                verb.upper(),
                url,
                headers=headers
            )

        response = json.loads(resp.data) if resp.data else None

        if resp.status > 300:
            raise Exception("Exception", str(response))

        return response

    def __retrieve_secret_key(self):
        '''
        To send new Secrets we need to encrypt them with a secret key
        This key is available on the public-key endpoint
        '''

        try:
            result = self.__call_github(
                verb='get',
                endpoint=(
                    f"/repositories/{self.__repository_id}"
                    f"/environments/{self.__environment}"
                    f"/secrets/public-key"
                )
            )

            return result

        except Exception as exception:
            return False

    def __encrypt_secret(self, public_key: str, value: str) -> str:
        '''
        Encrypt a Unicode string using the public key
        '''

        public_key = public.PublicKey(
            public_key.encode("utf-8"),
            encoding.Base64Encoder()
        )
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(value.encode("utf-8"))

        return b64encode(encrypted).decode("utf-8")

    def __environment_exists(self) -> bool:
        '''
        Checks if there is a Secret Key for the Environment
        If not, the environment does not exist
        '''

        return bool(self.__retrieve_secret_key())

    def secret_exists(self, key: str) -> bool:
        '''
        Retrieve information about Project Environment Secret existence
        '''

        try:
            self.__call_github(
                verb='get',
                endpoint=
                    f"/repositories/{self.__repository_id}"
                    f"/environments/{self.__environment}"
                    f"/secrets/{key}"
            )
        
            return True

        except Exception:
            return False

    def add_secret(self, key, value):
        '''
        Adds or updates a Secret for a Repository Environment
        '''

        encrypted = self.__encrypt_secret(
            public_key=self.__env_secret_key['key'],
            value=value
        )

        try:
            self.__call_github(
                verb='put',
                endpoint=
                    f"/repositories/{self.__repository_id}"
                    f"/environments/{self.__environment}"
                    f"/secrets/{key}",
                body={
                    "encrypted_value": encrypted,
                    "key_id": str(self.__env_secret_key['key_id'])
                }
            )

            return True

        except Exception as exception:
            return False
