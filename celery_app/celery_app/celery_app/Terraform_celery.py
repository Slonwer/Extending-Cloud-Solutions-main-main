import os
import subprocess
import logging
from celery import Celery
from redis import Redis
from redis.lock import Lock
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Celery configuration
app = Celery(
    'terraform_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

# Configure Celery
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Redis connection for locking
redis_client = Redis(host='localhost', port=6379, db=0)

@app.task(bind=True, max_retries=3)
def run_terraform(self, workspace_path, command, vars_dict=None):
    """
    Celery task to execute Terraform commands with synchronization.
    
    Args:
        workspace_path (str): Path to Terraform configuration directory
        command (str): Terraform command to run (e.g., 'apply', 'destroy')
        vars_dict (dict): Optional dictionary of Terraform variables
    """
    lock_name = f"terraform_lock_{workspace_path}"
    
    try:
        # Acquire distributed lock
        with Lock(redis_client, lock_name, timeout=3600):
            logger.info(f"Starting Terraform {command} in {workspace_path}")
            
            # Change to workspace directory
            os.chdir(workspace_path)
            
            # Initialize Terraform
            init_cmd = ["terraform", "init"]
            subprocess.run(init_cmd, check=True, capture_output=True, text=True)
            
            # Prepare Terraform command
            tf_cmd = ["terraform", command, "-auto-approve"]
            
            # Add variables if provided
            if vars_dict:
                for key, value in vars_dict.items():
                    tf_cmd.extend(["-var", f"{key}={value}"])
            
            # Execute Terraform command
            result = subprocess.run(
                tf_cmd,
                check=True,
                capture_output=True,
                text=True
            )
            
            logger.info(f"Terraform {command} completed successfully")
            return {
                "status": "success",
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
    except subprocess.CalledProcessError as e:
        logger.error(f"Terraform command failed: {e.stderr}")
        self.retry(countdown=60)
        return {
            "status": "error",
            "error": str(e),
            "stderr": e.stderr
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

def queue_terraform_task(workspace_path, command, vars_dict=None):
    """
    Helper function to queue a Terraform task.
    
    Args:
        workspace_path (str): Path to Terraform configuration directory
        command (str): Terraform command to run
        vars_dict (dict): Optional dictionary of Terraform variables
    
    Returns:
        str: Task ID
    """
    task = run_terraform.delay(workspace_path, command, vars_dict)
    return task.id

if __name__ == "__main__":
    # Example usage
    workspace = "/path/to/terraform/config"
    command = "apply"
    variables = {"region": "us-west-2", "instance_type": "t2.micro"}
    
    task_id = queue_terraform_task(workspace, command, variables)
    logger.info(f"Queued Terraform task with ID: {task_id}")