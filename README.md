# Github Secrets Filler

Convert your project dotenv files to Github Environment Secret Variables.

[![Code Quality Check](https://github.com/DevOpsActions/github-secrets-filler/actions/workflows/code-quality.yml/badge.svg)](https://github.com/DevOpsActions/github-secrets-filler/actions/workflows/code-quality.yml)

---

## Direct Usage

Prerequisites :
 - Python3
 - Installed dependencies

```bash
# Install dependencies
pip install -r requirements.txt
```

```raw
python main.py -h
usage: main.py [-h] -f DOTENV_FILE -p REPOSITORY_NAME -e ENVIRONMENT [-k GITHUB_TOKEN]

Import dotenv files to Github Projects Environments as Secret Variables

optional arguments:
  -h, --help            show this help message and exit
  -f DOTENV_FILE, --file DOTENV_FILE
                        path to the input dotenv file
  -p REPOSITORY_NAME, --project REPOSITORY_NAME
                        path to the github repository. Ex: ArteGEIE/my-project
  -e ENVIRONMENT, --env ENVIRONMENT
                        environment name
  -k GITHUB_TOKEN, --token GITHUB_TOKEN
                        Github API Token. Can be given through GITHUB_TOKEN environment variable.
```

## 🐳 Docker Usage (recommended)

```bash
export GITHUB_TOKEN=<YOUR_PERSONAL_ACCESS_TOKEN>

docker run --rm -v "$PWD:/dotenv" -e GITHUB_TOKEN="${GITHUB_TOKEN}" -it secrets-filler:latest \
    -f /dotenv/dotenv.example \
    -p "DevOpsActions/slave-repo-1" \
    -e testenv1
```

Explanations :
  1. Mount your local folder `$PWD` to `/dotenv` folder inside the container
  2. Pass `GITHUB_TOKEN` environment variable
  3. Give the script all the needed parameters :
     - `--project` or `-p` : Project Path (`User/Repository`)
     - `--env` or `-e` : Project Environment where the Secrets will be imported
     - `--file` or `-f` : Path to the dotenv file to import, inside the mounted `/dotenv` folder


## Personnal Access Token

In order to use this script, you will need to generate a `PAT` with `repo` scope.

---