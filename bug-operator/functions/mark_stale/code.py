#input_type_name: MarkStaleInput
#output_type_name: MarkStaleOutput
#function_name: mark_stale

from typing import Optional
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel
from lemma_sdk import FunctionContext, Pod

class MarkStaleInput(BaseModel):
    stale_days: Optional[int] = 14

class MarkStaleOutput(BaseModel):
    marked_count: int
    stale_ids: list

async def mark_stale(ctx: FunctionContext, data: MarkStaleInput) -> MarkStaleOutput:
    pod = Pod.from_env()
    table = pod.table("bugs")
    cutoff = datetime.now(timezone.utc) - timedelta(days=data.stale_days)
    all_bugs = table.list({"limit": 500})
    items = all_bugs.get("items", [])

    marked = []
    for bug in items:
        if bug.get("status") not in ("new", "approved"):
            continue
        if bug.get("stale_pinged"):
            continue
        updated_raw = bug.get("updated_at") or bug.get("created_at")
        if not updated_raw:
            continue
        try:
            updated = datetime.fromisoformat(updated_raw.replace("Z", "+00:00"))
        except Exception:
            continue
        if updated < cutoff:
            existing_notes = bug.get("notes") or ""
            stale_note = f"\n[STALE {datetime.now(timezone.utc).strftime('%Y-%m-%d')}] No activity for {data.stale_days}+ days. Please verify if this issue is still reproducible."
            table.update(bug["id"], {
                "stale_pinged": True,
                "notes": existing_notes + stale_note
            })
            marked.append(bug["id"])

    return MarkStaleOutput(marked_count=len(marked), stale_ids=marked)
