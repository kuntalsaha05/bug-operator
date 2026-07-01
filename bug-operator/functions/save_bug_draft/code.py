#input_type_name: SaveBugDraftInput
#output_type_name: SaveBugDraftResult
#function_name: save_bug_draft

from typing import Optional
from pydantic import BaseModel
from lemma_sdk import FunctionContext, Pod

class SaveBugDraftInput(BaseModel):
    title: str
    description: str
    reporter_email: Optional[str] = None
    intent_type: Optional[str] = "bug"
    category: Optional[str] = None
    priority: Optional[str] = "normal"
    sla_score: Optional[str] = None
    parent_id: Optional[str] = None
    affected_users: Optional[int] = 1
    component_tags: Optional[str] = None
    reproduction_steps: Optional[str] = None
    suggested_fix: Optional[str] = None
    repro_script: Optional[str] = None
    notes: Optional[str] = None

class SaveBugDraftResult(BaseModel):
    bug_id: str

async def save_bug_draft(ctx: FunctionContext, data: SaveBugDraftInput) -> SaveBugDraftResult:
    pod = Pod.from_env()
    payload = {
        "title": data.title,
        "description": data.description,
        "status": "new",
        "priority": data.priority or "normal",
    }
    if data.reporter_email: payload["reporter_email"] = data.reporter_email
    if data.intent_type: payload["intent_type"] = data.intent_type
    if data.category: payload["category"] = data.category
    if data.sla_score: payload["sla_score"] = data.sla_score
    if data.parent_id: payload["parent_id"] = data.parent_id
    if data.affected_users is not None: payload["affected_users"] = data.affected_users
    if data.component_tags: payload["component_tags"] = data.component_tags
    if data.reproduction_steps: payload["reproduction_steps"] = data.reproduction_steps
    if data.suggested_fix: payload["suggested_fix"] = data.suggested_fix
    if data.repro_script: payload["repro_script"] = data.repro_script
    if data.notes: payload["notes"] = data.notes

    # If this is a duplicate, increment the parent's duplicate_count
    if data.parent_id:
        try:
            parent = pod.table("bugs").get(data.parent_id)
            current_count = parent.get("duplicate_count") or 0
            pod.table("bugs").update(data.parent_id, {"duplicate_count": current_count + 1})
        except Exception:
            pass

    record = pod.table("bugs").create(payload)
    return SaveBugDraftResult(bug_id=str(record["id"]))
