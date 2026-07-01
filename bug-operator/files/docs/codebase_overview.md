# Codebase Overview: TaskPilot

This document outlines the architecture, components, and known error patterns of the TaskPilot codebase. The `triage-agent` should refer to this document when analyzing incoming bug reports.

## System Architecture

TaskPilot is a modern task management system consisting of three main services:

1.  **Frontend Dashboard (`/services/dashboard`)**: A Next.js web interface where users view, filter, and modify tasks.
2.  **Task Manager Service (`/services/task-manager`)**: A FastAPI Python service that handles task creation, assignment, scheduling, and CRUD operations.
3.  **Notification Worker (`/services/notifier`)**: A Node.js worker that listens to Task Manager events and dispatches notifications via Slack, Email, and SMS.

---

## Service Component Map

### 1. Frontend Dashboard (`/services/dashboard`)
*   **Tech Stack**: Next.js, React, Tailwind CSS, TypeScript.
*   **Key Files**:
    *   `src/components/TaskBoard.tsx`: Render kanban columns.
    *   `src/hooks/useTasks.ts`: Hooks for fetching tasks from the backend.
*   **Common Warnings**: Avoid polling tasks; use WebSockets.

### 2. Task Manager Service (`/services/task-manager`)
*   **Tech Stack**: FastAPI, PostgreSQL (SQLAlchemy), Celery.
*   **Key Files**:
    *   `app/routers/tasks.py`: REST routes for tasks.
    *   `app/services/scheduler.py`: Celery tasks for recurring deadlines.
*   **Common Warnings**: Task deadlock can happen if multiple celery workers lock the same row.

### 3. Notification Worker (`/services/notifier`)
*   **Tech Stack**: Node.js, BullMQ, Redis.
*   **Key Files**:
    *   `src/workers/slack.js`: Sends slack webhook messages.
    *   `src/workers/email.js`: Dispatches emails using SendGrid.

---

## Known Errors & Troubleshooting Playbook

When a bug report matches one of these known issues, refer to the solution below:

### 1. Category: Notifications
*   **Error Code**: `ERR_NOTIF_SLACK_TIMEOUT`
*   **Symptom**: Slack alerts for task assignment fail to deliver or timeout.
*   **Root Cause**: Slack API rate limiting or a broken Slack webhook configuration.
*   **Fix**: Verify the webhook URL in configuration. Add a retry queue with exponential backoff.
*   **Priority**: normal

### 2. Category: Database
*   **Error Code**: `ERR_DB_DEADLOCK_CELERY`
*   **Symptom**: Task deadlines don't update and celery tasks show database locks.
*   **Root Cause**: `SELECT FOR UPDATE` query locks rows in a loop during task status changes.
*   **Fix**: Update `scheduler.py` to use optimistic locking or reduce locking granularity.
*   **Priority**: high

### 3. Category: Dashboard
*   **Error Code**: `ERR_FE_WS_DISCONNECT`
*   **Symptom**: Board doesn't update tasks in real-time. Console shows WebSocket handshake failure.
*   **Root Cause**: Incorrect CORS settings on FastAPI server for WebSockets.
*   **Fix**: Add allowed origin configurations in backend middleware.
*   **Priority**: normal

### 4. Category: Authentication
*   **Error Code**: `ERR_AUTH_EXPIRED_JWT`
*   **Symptom**: Users are kicked out and redirected to login page within 5 minutes of usage.
*   **Root Cause**: Token expiration timer is set to 300 seconds instead of 1 hour in `/services/task-manager/.env`.
*   **Fix**: Set `JWT_EXPIRY_SECONDS=3600`.
*   **Priority**: urgent
