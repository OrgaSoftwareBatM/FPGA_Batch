# this script is used on windows to wrap shortcuts so that they are executed within an environment
#   It only sets the appropriate prefix PATH entries - it does not actually activate environments

import os
import sys
import subprocess
from os.path import join, pathsep

from menuinst.knownfolders import FOLDERID, get_folder_path, PathNotFoundException

# call as: python cwp.py PREFIX ARGs...

prefix = sys.argv[1]
cwd = sys.argv[2]
args = sys.argv[3:]

new_paths = pathsep.join([prefix,
                         join(prefix, "Library", "mingw-w64", "bin"),
                         join(prefix, "Library", "usr", "bin"),
                         join(prefix, "Library", "bin"),
                         join(prefix, "Scripts")])
env = os.environ.copy()
env['PATH'] = new_paths + pathsep + env['PATH']
env['CONDA_PREFIX'] = prefix

os.chdir(cwd)
sys.exit(subprocess.call(args, env=env))