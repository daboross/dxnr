Building dxnr
=============

### Step1: the environment

You'll need to install some packages from your operating system. Dxnr requires:

- `python3.5`
- `pip-3.5`

Please note that python3.4 will not work, and the pip instillation must also be for python3.5. Check which python
version `pip` is associated to with `pip --version`.

### Step2: virtualenv

Virtualenv can be installed via the OS, but it is recommended to do this via `pip`. The newer `venv` is somewhat
supported by the build script, but you will need to install the dependencies in `requirements.txt` manually if you
use it.

```
# one of these will most likely work for you:
pip install virtualenv
pip3.5 install virtualenv
pip-3.5 install virtualenv
```

### Step3: configuration

You'll want to copy `config.default.json` into a `config.json` file, then add your credentials.

There are two additional options not specified in `config.default.json` that you may wish to add if relevant:

```
// if true, deploy to the public test realm - only works on official server
    "ptr": false
// if present, used instead of https://screeps.com
    "url": "http://server1.screepspl.us:21025"
```

### Step4: running it

```bash
./build.py
```

This script will create a virtualenv, install transcrypt into it, build the files and deploy to the related URL.

On subsequent runs, it will only need to run transcrypt and deploy.