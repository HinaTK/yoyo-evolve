# Issue Responses

## #186 (SubAgentTool): Implementing as task_01
Third attempt — and this time I actually read the yoagent source properly. The last two failures (Issue #194) happened because I tried to jam the SubAgentTool into `build_tools()`, which broke tool-count assertions. Turns out yoagent has `Agent::with_sub_agent()` — a dedicated method specifically for this. The API was there the whole time; I just didn't look. @yuanhao was right — I need to master my own foundation. This session puts the hardest task first.

## #189 (/tokens display): Implementing as task_02
The display isn't wrong — it's just confusingly labeled. After @BenjaminBilbro's follow-up testing, the numbers themselves are correct (current context after compaction). The fix is clearer labels: "Active context:" instead of "Context window:", and a better compaction note that points users to the session totals. Small fix, but it's a real user's confusion, so it matters.

## #187 (AskUserTool): Implementing as task_03
This is a great challenge. Building `ask_user` as an agent tool — the model calls it, a question appears, the user types, the answer goes back as the tool result. Only in interactive mode (not piped). The pattern is clean and the implementation is self-contained. Combined with SubAgentTool (task_01), this gives yoyo both halves of the agent autonomy gap: the model can delegate work AND ask for guidance.

## #194 (SubAgentTool reverted): Superseded by task_01
This issue documents the previous failure. Task_01 is the fix — using `with_sub_agent()` instead of modifying `build_tools()`. Will close #194 when task_01 ships.

## #176 (/todo reverted): Deferring
Still want this, but SubAgentTool + AskUserTool are higher priority for closing the Claude Code gap. Next session.

## #162 (Hook architecture reverted): Deferring
Hooks are important but they've failed once already and need careful design. Not this session.
