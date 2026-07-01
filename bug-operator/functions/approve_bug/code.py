#input_type_name: ApproveBugInput
#output_type_name: ApproveBugResult
#function_name: approve_bug

from typing import Optional
from pydantic import BaseModel
from lemma_sdk import FunctionContext, Pod

class ApproveBugInput(BaseModel):
    bug_id: str
    priority: Optional[str] = None
    sla_score: Optional[str] = None
    category: Optional[str] = None
    reproduction_steps: Optional[str] = None
    suggested_fix: Optional[str] = None
    notes: Optional[str] = None

class ApproveBugResult(BaseModel):
    success: bool

async def approve_bug(ctx: FunctionContext, data: ApproveBugInput) -> ApproveBugResult:
    pod = Pod.from_env()
    payload = {"status": "approved"}
    if data.priority is not None: payload["priority"] = data.priority
    if data.sla_score is not None: payload["sla_score"] = data.sla_score
    if data.category is not None: payload["category"] = data.category
    if data.reproduction_steps is not None: payload["reproduction_steps"] = data.reproduction_steps
    if data.suggested_fix is not None: payload["suggested_fix"] = data.suggested_fix
    if data.notes is not None: payload["notes"] = data.notes
    pod.table("bugs").update(data.bug_id, payload)
    return ApproveBugResult(success=True)
