import subprocess

subprocess.run(["python", "load_env.py"])
subprocess.run(["python", "delete_Images_WRT.py"])
subprocess.run(["python", "cli.py", "-f", "config.template.json"])

