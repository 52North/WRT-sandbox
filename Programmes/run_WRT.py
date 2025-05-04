import subprocess

subprocess.run(["python", "/home/jovyan/Programmes/load_env.py"])
subprocess.run(["python", "/home/jovyan/Programmes/delete_Images_WRT.py"])
subprocess.run(["python", "/home/jovyan/Programmes/cli.py", "-f", "/home/jovyan/Configuraton/config.template.json"])

