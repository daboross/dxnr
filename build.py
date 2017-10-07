#!/usr/bin/env python3
import errno
import json
import subprocess
import sys
import urllib.parse
import urllib.request
from argparse import ArgumentParser
from typing import Dict, List, Optional, Union

import base64
import os
import shutil

transcrypt_arguments = ['-n', '-p', '.none', '--noalias',
                        'name,undefined,Infinity,keys,get,set,type,update,values']

transcrypt_dirty_args = transcrypt_arguments + []
transcrypt_clean_args = transcrypt_arguments + ['-b']

mypy_arguments = ['--python-version', '3.5', '--disallow-untyped-defs', '--no-implicit-optional']


class BuildException(Exception):
    pass


def possible_transcrypt_binary_paths(config: 'Configuration') -> List[str]:
    """
    Finds all different places to look for a `transcrypt` binary to run.
    """
    return [
        os.path.join(config.base_dir, 'env', 'bin', 'transcrypt'),
        os.path.join(config.base_dir, 'env', 'Scripts', 'transcrypt.exe'),
        shutil.which('transcrypt'),
        shutil.which('transcrypt.exe'),
    ]


def possible_pip_binary_paths(config: 'Configuration') -> List[str]:
    """
    Finds all different places to look for a `pip` binary to run.
    """
    files = [
        os.path.join(config.base_dir, 'env', 'bin', 'pip'),
        os.path.join(config.base_dir, 'env', 'Scripts', 'pip.exe'),
    ]
    if not config.enter_env:
        for path in (shutil.which('pip'), shutil.which('pip.exe')):
            if path is not None:
                files.append(path)

    return files


def possible_mypy_binary_paths(config: 'Configuration') -> List[str]:
    """
    Finds all different places to look for a `mypy` binary to run.
    """
    files = [
        os.path.join(config.base_dir, 'env', 'bin', 'mypy'),
        os.path.join(config.base_dir, 'env', 'Scripts', 'pip.exe')
    ]
    if not config.enter_env:
        for path in (shutil.which('mypy'), shutil.which('mypy.exe')):
            if path is not None:
                files.append(path)
    return files


class Configuration:
    """
    Utility struct holding all configuration values.
    """

    def __init__(self, base_dir: str, config_json: Dict[str, Union[str, bool]], clean_build: bool = True) -> None:
        self.base_dir = base_dir
        self.username = config_json.get('username') or config_json.get('email')
        assert isinstance(self.username, str)
        self.password = config_json['password']
        assert isinstance(self.password, str)
        self.branch = config_json.get('branch', 'default')
        assert isinstance(self.branch, str)
        self.url = config_json.get('url', 'https://screeps.com')
        assert isinstance(self.url, str)
        self.ptr = config_json.get('ptr', False)
        assert isinstance(self.ptr, bool)
        self.enter_env = config_json.get('enter-env', True)
        assert isinstance(self.enter_env, bool)

        self.clean_build = clean_build

    def transcrypt_executable(self) -> Optional[str]:
        """
        Utility method to find a transcrypt executable file.

        :rtype: str
        """
        for path in possible_transcrypt_binary_paths(self):
            if path is not None and os.path.exists(path):
                return path
        else:
            return None

    def pip_executable(self) -> Optional[str]:
        """
        Utility method to find a pip executable file.

        :rtype: str
        """
        for path in possible_pip_binary_paths(self):
            if path is not None and os.path.exists(path):
                return path
        else:
            return None

    def mypy_executable(self) -> Optional[str]:
        for path in possible_mypy_binary_paths(self):
            if path is not None and os.path.exists(path):
                return path
        else:
            return None


def load_config(base_dir: str) -> Configuration:
    """
    Loads the configuration from the `config.json` file.
    """
    parser = ArgumentParser()
    parser.add_argument("-c", "--config-file", type=str, default='config.json',
                        help="file to load configuration from")
    parser.add_argument("-d", "--dirty-build", action='store_true',
                        help="if true, use past built files for files who haven't changed")
    args = parser.parse_args()

    config_file = os.path.join(base_dir, 'config.json')

    with open(os.path.join(base_dir, config_file)) as f:
        config_json = json.load(f)

    return Configuration(base_dir, config_json, clean_build=not args.dirty_build)


def run_transcrypt(config: Configuration) -> None:
    """
    Compiles source code using the `transcrypt` program.

    :type config: Configuration
    """
    transcrypt_executable = config.transcrypt_executable()
    source_main = os.path.join(config.base_dir, 'src', 'python', 'main.py')

    if config.clean_build:
        cmd_args = transcrypt_clean_args
    else:
        cmd_args = transcrypt_dirty_args

    args = [transcrypt_executable] + cmd_args + [source_main]
    source_dir = os.path.join(config.base_dir, 'src', 'python')

    ret = subprocess.Popen(args, cwd=source_dir).wait()

    if ret != 0:
        raise BuildException("transcrypt failed. exit code: {}. command line '{}'. working dir: '{}'."
                             .format(ret, "' '".join(args), source_dir))


def run_mypy(config: Configuration) -> None:
    """
    Tests source code using the `mypy` program.
    """
    mypy_executable = config.mypy_executable()
    source_main = os.path.join(config.base_dir, 'src', 'python', 'main.py')

    args = [mypy_executable] + mypy_arguments + [source_main]
    source_dir = os.path.join(config.base_dir, 'src', 'python')
    stub_dir = os.path.join(config.base_dir, 'src', 'stubs')

    old_mypy_path = os.environ.get("MYPYPATH")
    if old_mypy_path:
        mypy_path = old_mypy_path + ":" + stub_dir
    else:
        mypy_path = stub_dir
    os.environ["MYPYPATH"] = mypy_path

    ret = subprocess.Popen(args, cwd=source_dir).wait()

    if ret != 0:
        raise BuildException("mypy failed.")

    if old_mypy_path is not None:
        os.environ["MYPYPATH"] = old_mypy_path
    else:
        del os.environ["MYPYPATH"]

def copy_artifacts(config: Configuration) -> None:
    """
    Copies compiled JavaScript files to output directory after `transcrypt` has been run.
    """
    dist_directory = os.path.join(config.base_dir, 'dist')

    try:
        os.makedirs(dist_directory)
    except OSError as e:
        if e.errno == errno.EEXIST:
            shutil.rmtree(dist_directory)
            os.makedirs(dist_directory)
        else:
            raise

    shutil.copyfile(os.path.join(config.base_dir, 'src', 'python', '__javascript__', 'main.js'),
                    os.path.join(dist_directory, 'main.js'))

    js_directory = os.path.join(config.base_dir, 'src', 'javascript')

    if os.path.exists(js_directory) and os.path.isdir(js_directory):
        for name in os.listdir(js_directory):
            source = os.path.join(js_directory, name)
            dest = os.path.join(dist_directory, name)
            shutil.copy2(source, dest)


def check(config: Configuration) -> None:
    print("running mypy...")
    run_mypy(config)


def build(config: Configuration) -> None:
    """
    Compiles source code, and copies JavaScript files to output directory.
    """
    print("running transcrypt...")
    run_transcrypt(config)
    print("copying artifacts...")
    copy_artifacts(config)
    print("build successful.")


def upload(config: Configuration) -> None:
    """
    Uploads JavaScript files found in the output directory to the Screeps server.
    """

    module_files = {}

    dist_dir = os.path.join(config.base_dir, 'dist')

    for file_name in os.listdir(dist_dir):
        with open(os.path.join(dist_dir, file_name)) as f:
            module_files[os.path.splitext(file_name)[0]] = f.read()

    if config.ptr:
        post_url = '{}/ptr/api/user/code'.format(config.url)
    else:
        post_url = '{}/api/user/code'.format(config.url)

    post_data = json.dumps({'modules': module_files, 'branch': config.branch}).encode('utf-8')

    auth_pair = config.username.encode('utf-8') + b':' + config.password.encode('utf-8')

    headers = {
        'Content-Type': b'application/json; charset=utf-8',
        'Authorization': b'Basic ' + base64.b64encode(auth_pair),
    }
    request = urllib.request.Request(post_url, post_data, headers)

    if config.url != 'https://screeps.com':
        print("uploading files to {}, branch {}{}..."
              .format(config.url, config.branch, " on PTR" if config.ptr else ""))
    else:
        print("uploading files to branch {}{}...".format(config.branch, " on PTR" if config.ptr else ""))

    # any errors will be thrown.
    with urllib.request.urlopen(request) as response:
        decoded_data = response.read().decode('utf-8')
        json_response = json.loads(decoded_data)
        if not json_response.get('ok'):
            if 'error' in json_response:
                raise BuildException("upload error: {}".format(json_response['error']))
            else:
                raise BuildException("upload error: {}".format(json_response))

    print("upload successful.")


def install_env(config: Configuration) -> None:
    """
    Creates a virtualenv environment in the `env/` folder, and attempts to install `transcrypt` into it.

    If `enter-env` is False in the `config.json` file, this will instead install `transcrypt`
    into the default location for the `pip` binary which is in the path.
    """
    if config.transcrypt_executable() is not None:
        return
    if config.enter_env:
        env_dir = os.path.join(config.base_dir, 'env')

        if not os.path.exists(env_dir):
            print("creating virtualenv environment...")
            if sys.version_info >= (3, 5):
                args = ['virtualenv', '--system-site-packages', env_dir]
            else:
                args = ['virtualenv', '-p', 'python3.5', '--system-site-packages', env_dir]

            ret = subprocess.Popen(args, cwd=config.base_dir).wait()

            if ret != 0:
                raise BuildException("virtualenv failed. exit code: {}. command line '{}'. working dir: '{}'."
                                     .format(ret, "' '".join(args), config.base_dir))

        if not os.path.exists(os.path.join(env_dir, 'bin', 'transcrypt')) and not os.path.exists(
                os.path.join(env_dir, 'Scripts', 'transcrypt.exe')):
            print("installing transcrypt into env...")

            requirements_file = os.path.join(config.base_dir, 'requirements.txt')

            pip_executable = config.pip_executable()

            if not pip_executable:
                raise BuildException("pip binary not found at any of {}".format(possible_pip_binary_paths(config)))

            install_args = [pip_executable, 'install', '-r', requirements_file]

            ret = subprocess.Popen(install_args, cwd=config.base_dir).wait()

            if ret != 0:
                raise BuildException("pip install failed. exit code: {}. command line '{}'. working dir: '{}'."
                                     .format(ret, "' '".join(install_args), config.base_dir))

    else:
        if not shutil.which('transcrypt'):
            print("installing transcrypt using 'pip'...")

            requirements_file = os.path.join(config.base_dir, 'requirements.txt')

            pip_executable = config.pip_executable()

            if not pip_executable:
                raise BuildException("pip binary not found at any of {}".format(possible_pip_binary_paths(config)))

            install_args = [pip_executable, 'install', '-r', requirements_file]

            ret = subprocess.Popen(install_args, cwd=config.base_dir).wait()

            if ret != 0:
                raise BuildException("pip install failed. exit code: {}. command line '{}'. working dir: '{}'."
                                     .format(ret, "' '".join(install_args), config.base_dir))


def main() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config = load_config(base_dir)

    install_env(config)
    check(config)
    build(config)
    upload(config)


if __name__ == "__main__":
    try:
        main()
    except BuildException as e:
        print("failing:\n\n{}".format(e.args[0] if len(e.args) == 1 else e.args))
