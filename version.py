"""Versionsnummer aus Git-Tag extrahieren
"""
from subprocess import check_output, CalledProcessError
from os.path import isdir, join, dirname

# idea from 
def get_version():
    """Version aus git describe extrahieren
    """
    # https://github.com/Changaco/version.py/blob/master/version.py

    # Get the version using "git describe".
    cmd = 'git describe --tags --match [0-9]* --dirty' 
    try:
        version = check_output(cmd.split()).decode().strip()
    except CalledProcessError:
        #in deployment
        try:
            from deploy_version import VERSION
            version = VERSION
        except ImportError:
            # Unable to get version number deploy_version.py
            version = "0.1"

    return version

if __name__ == "__main__":
    print(get_version())
