import subprocess
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='/home/jovyan/Configuration/envfile')

env = os.environ.copy()
subprocess.run(["python", "/home/jovyan/Programmes/delete_Images_WRT.py"])
subprocess.run(["python", "/home/jovyan/Programmes/cli.py", "-f", "/home/jovyan/Configuration/config.template.json"])
subprocess.run(["python","/home/jovyan/Programmes/compare_routes.py"])
