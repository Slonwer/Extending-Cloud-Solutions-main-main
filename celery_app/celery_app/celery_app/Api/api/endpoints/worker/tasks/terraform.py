import subprocess
import os
from celery import shared_task

TERRAFORM_DIR = os.path.join(os.path.dirname(__file__), "../../../terraform")

def run_cmd(command, cwd):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }

@shared_task(bind=True)
def terraform_sync(self, action='apply'):
    cmds = {
        "init": ["terraform", "init"],
        "plan": ["terraform", "plan"],
        "apply": ["terraform", "apply", "-auto-approve"],
        "destroy": ["terraform", "destroy", "-auto-approve"]
    }

    if action not in cmds:
        return {"erro": "ação inválida"}

    init = run_cmd(cmds["init"], TERRAFORM_DIR)
    if init["returncode"] != 0:
        return {"erro": "erro ao inicializar", **init}

    result = run_cmd(cmds[action], TERRAFORM_DIR)
    return result
