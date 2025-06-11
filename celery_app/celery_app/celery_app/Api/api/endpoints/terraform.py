from fastapi import APIRouter, HTTPException
from worker.tasks.terraform import terraform_sync

router = APIRouter()

@router.post("/executar")
async def executar_terraform(action: str = "apply"):
    if action not in {"init", "plan", "apply", "destroy"}:
        raise HTTPException(status_code=400, detail="Ação inválida")

    task = terraform_sync.delay(action=action)
    return {
        "mensagem": f"Ação '{action}' iniciada.",
        "task_id": task.id
    }
