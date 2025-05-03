import subprocess

subprocess.run(["python", "load_env.py"])
subprocess.run(["python", "delete_Images_WRT.py"])
subprocess.run(["python", "cli.py", "-f", "/home/jovyan/Configuraton/config.template.json"])

