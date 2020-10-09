#!/usr/bin/env python3

import os
import sys
import subprocess

import json
import shlex
import requests

import argparse
from constants import VERSION
from alive_progress import alive_bar, config_handler

INVALID_TOKEN_MSG = "Error: Gitlab token is required.\nGet your token at %s/profile/personal_access_tokens or pass --help for get full help"
INVALID_METHOD_MSG = "Error: Invalid method. ('ssh' or 'http')"
INVALID_PATH_MSG = "Error: Invalid path name. Path %s does exist."


def validate_args(args, base_url): 
    ''' 
    validate args data. 
    '''
    if not args.token or not valid_token(str(args.token)): 
        print(INVALID_TOKEN_MSG % base_url)
        quit() 
    if args.method and not valid_method(str(args.method)): 
        print(INVALID_METHOD_MSG % (str(args.method))) 
        quit()
    return

def valid_token(token):
    return token and len(token) > 10

def valid_method(method_name): 
    return method_name == "ssh" or method_name == "http" 


def get_projects(args, base_url):
    url = f"{base_url}/api/v4/projects"
    headers = {'PRIVATE-TOKEN': args.token}
    params = {'membership': True, 'per_page': 50000}

    r = requests.get(url, headers=headers, params=params)
    return r.json()    


def fg(text, color): return ("\33[38;5;" + str(color) + "m" + text + "\33[0m")

def git_clone(args, project_url, dir_name):
    try:
        command = f"git clone --mirror {project_url} {dir_name}.git"
        if not args.verbose:
            command += " -q"
        command = shlex.split(command)
        result = subprocess.Popen(command)
        result.wait()
    except Exception as e:
        print("Error on %s: %s \n" % (project_url, e.strerror))

def main():
    parser = argparse.ArgumentParser(description = "Gitlab backup tool, clone all project at once!", add_help=False)

    required = parser.add_argument_group('Required arguments')
    optional = parser.add_argument_group('Optional arguments')

    required.add_argument("-t", "--token", type=str, metavar='str', default = None,
                        help="Gitlab personal access token")

    optional.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")
    
    optional.add_argument("-u", "--url", type=str, metavar='str',
                        help="Specify Gitlab instance URL")

    optional.add_argument("-m", "--method", type=str, metavar='str',
                        help="Specify clone method (default is http)")

    optional.add_argument("-o", "--output", type=str, metavar='str',
                        help="Output directory (defaults to ./gitlab-backup)")

    optional.add_argument("-v", "--version", action='version', version=VERSION)
    

    optional.add_argument(
        '-h',
        '--help',
        action='help',
        default=argparse.SUPPRESS,
        help="Show this message and exit."
    )
  
    args = parser.parse_args() 
    
    base_url = args.url or 'https://gitlab.com'
    if args.verbose:
      print(f"Set gitlab url to {fg(base_url, 39)}")

    folder_name = args.output or 'gitlab-backup'
    
    validate_args(args, base_url)

    method = "ssh_url_to_repo" if args.method == "ssh" else "http_url_to_repo"
    
    projects = get_projects(args, base_url)
    if args.verbose:
        print("\nGot " +
            fg(f"{len(projects)}", 39)+" projects:")
        print([p['name'] for p in projects], "\n")

    with alive_bar(len(projects), enrich_print=False, force_tty=True) as bar:
        for project in projects:
            name = project['name']
            namespace = project['path_with_namespace']
            dir_name = os.path.join(folder_name, namespace)
            project_url = project['ssh_url_to_repo']
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
                print(fg(f"[x] {name}\n", 37))
                bar(fg(f"Cloning {name}\n", 39))
                git_clone(args, project_url, dir_name)
            else:
                print(fg(f"[-] {name} exist\n", 37))
                bar(f"Cloning {name}\n")
  
if __name__ == "__main__": 
    main() 