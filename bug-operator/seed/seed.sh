#!/bin/bash
# Seed script for bug-operator pod

echo "=== Seeding codebase_overview.md to RAG files ==="
lemma files upload ./files/docs/codebase_overview.md /docs/codebase_overview.md --yes

echo "=== Seeding sample bug tickets ==="

# 1. Resolved Bug (ready for compile release notes)
lemma records create bugs --yes --data '{
  "title": "FastAPI websocket handshake deadlock on dashboard load",
  "description": "Active WebSocket connection locks thread during NextJS hot-reloading.",
  "category": "Dashboard",
  "priority": "normal",
  "status": "resolved",
  "reproduction_steps": "1. Start dashboard service\n2. Open board page\n3. Hot-reload the client multiple times",
  "suggested_fix": "Add allowed origin configurations in backend middleware as detailed in ERR_FE_WS_DISCONNECT."
}'

# 2. Approved Bug (ready for developer to fix)
lemma records create bugs --yes --data '{
  "title": "Celery task scheduler row lock timeout",
  "description": "Celery worker hangs when attempting to update status of locked database row.",
  "category": "Database",
  "priority": "high",
  "status": "approved",
  "reproduction_steps": "1. Queue 10 status update tasks simultaneously\n2. Observe pg_stat_activity logs showing row lock locks",
  "suggested_fix": "Update scheduler.py to use optimistic locking or reduce locking granularity as detailed in ERR_DB_DEADLOCK_CELERY."
}'

# 3. New Bug (waiting for triage/approval)
lemma records create bugs --yes --data '{
  "title": "Slack alerts assignee username null",
  "description": "Slack message shows Task assigned to null when a user is assigned a task.",
  "category": "Notifications",
  "priority": "normal",
  "status": "new",
  "notes": "Needs agent triage to find correct error code and reproduction steps."
}'

echo "=== Seeding complete! ==="
