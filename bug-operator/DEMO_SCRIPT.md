# BugPilot — Demo Script
**Deadline: 2:00 PM, July 2nd 2026**
**Form: https://forms.gle/Uapf6KpBBuVrqdoZA**

---

## BEFORE YOU HIT RECORD

1. Run in terminal → copy output:
   ```
   lemma auth print-token
   ```

2. Open these 3 things:
   - **Tab 1:** https://bug-desk.apps.lemma.work/ → paste token → CONNECT TO POD
   - **Tab 2:** https://lemma.work → bug-operator → triage-agent (chat open)
   - **Terminal:** PowerShell window ready

3. Start recording: **Win + G** → ⏺ Record

---

## SCENE 1 — Dashboard (30 sec)
> *[Show Tab 1 — scroll slowly through the bug list]*

**SAY:**
"This is BugPilot — an AI bug triage and release operator built on Lemma.

The moment a bug comes in, BugPilot classifies it, scores its severity, and routes it for human approval — automatically.

Here's the live command center. You can see active incidents, their priority levels, affected users, SLA scores, and real-time status — all updating live."

---

## SCENE 2 — Triage Agent Chat (60 sec)
> *[Switch to Tab 2 — triage-agent chat]*

**SAY:**
"The triage agent is always available in chat. Let me ask it to summarize the critical issues right now."

**TYPE IN CHAT:**
```
Summarize the most critical open bugs and their priorities
```

> *[Wait for full response]*

**SAY:**
"It queries the bugs table, groups by priority, and tells me exactly what needs attention — urgent issues first, with a full breakdown."

---

## SCENE 3 — Triage Workflow (45 sec)
> *[Switch to terminal]*

**SAY:**
"When a new bug comes in, I trigger the triage workflow. Watch this."

**RUN THIS COMMAND:**
```powershell
$env:PYTHONUTF8=1; lemma workflows run triage-workflow --file "C:\Users\sahak\.gemini\antigravity-ide\brain\adaa58fd-c243-4be6-adf6-9f33b1162786\scratch\demo_bug.json"
```

> *[Switch back to Tab 1 — dashboard]*

**SAY:**
"The workflow automatically classifies the bug's intent, redacts any PII in the description, calculates the SLA score based on affected users, and queues it for approval. You can see it appear on the dashboard right now — live."

---

## SCENE 4 — Release Agent (45 sec)
> *[Go to Tab 2 — click release-agent in sidebar]*

**SAY:**
"BugPilot also has a release agent that handles release management. Let me ask it to compile release notes."

**TYPE IN CHAT:**
```
Compile release notes for all resolved bugs this week
```

> *[Wait for full response]*

**SAY:**
"It generates three versions automatically — technical notes for the engineering team, a marketing summary for the product page, and an internal changelog. One command, three audiences."

---

## SCENE 5 — Wrap Up (20 sec)
> *[Switch to terminal]*

**RUN:**
```powershell
$env:PYTHONUTF8=1; lemma surfaces get WHATSAPP
```

> *[Show Status: ACTIVE, then switch back to dashboard]*

**SAY:**
"BugPilot is also connected via WhatsApp. Users can report bugs directly by message, and the triage agent responds and creates a ticket automatically.

BugPilot is built entirely on Lemma — two AI agents, four serverless functions, automated triage workflows, a scheduled stale-bug pruner, a WhatsApp surface, and a real-time dashboard.

One pod. Fully automated. Always on."

---

## STOP RECORDING

Then:
1. Save and export the video
2. Upload to Google Drive or YouTube (unlisted)
3. Submit at: **https://forms.gle/Uapf6KpBBuVrqdoZA**

### Submission details:
- **GitHub:** https://github.com/kuntalsaha05/bug-operator
- **Live app:** https://bug-desk.apps.lemma.work/
- **Pod ID:** 019f180f-9681-714f-a7d5-026bfbbed3a6
