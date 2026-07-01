# AI Bug Triage & Release Operator Pod

This pod automates the triage of engineering bug reports (using RAG docs lookup), provides a human approval step, and compiles markdown release notes from resolved bugs.

## Setup & Deployment Runbook

1.  **Authenticate**:
    ```bash
    lemma auth login
    ```
2.  **Create the Pod**:
    ```bash
    lemma pod create bug-operator --description "AI Bug Triage & Release Operator"
    ```
3.  **Select the Pod**:
    ```bash
    lemma config set default_pod bug-operator
    ```
4.  **Import the Bundle**:
    ```bash
    lemma pods import ./bug-operator
    ```
5.  **Seed the Pod**:
    Run the seed script to upload documentation and add sample tickets:
    ```bash
    cd bug-operator
    ./seed/seed.sh
    ```

---

## Verification & Smoke Test

### 1. Table Verification
Check that the schemas were created successfully:
```bash
lemma tables get bugs
lemma tables get releases
```

### 2. Files RAG Verification
Confirm the playbook documentation is uploaded and indexed:
```bash
lemma files search "deadlock" --scope /docs
```

### 3. Agent Triage Verification
Test the triage-agent directly:
```bash
lemma agents run triage-agent "Slack alerts assignee username null"
```
Ensure it returns a structured JSON matching the output schema.

### 4. Workflow Smoke Test
Trigger the triage workflow manually:
```bash
lemma workflows run triage-workflow
```
*   Step 1: Submit the bug details (title: "Auth token expiration too short", description: "JWT tokens expire within 5 minutes.")
*   Step 2: Check the dashboard board to see a new bug with status `new`.
*   Step 3: Submit the active form wait to approve the triage (marking it `approved`).
*   Step 4: Check if the bug status moves to `approved` in the bugs table.

### 5. App Verification
Open the BugPilot App Desk:
```bash
lemma apps open bug-desk
```
Verify the Kanban board renders correctly, updates in real-time, and generates release notes successfully.
