# Hoy AI Build Plan

Oct 10, 2026 · @hoy

## What Hoy AI is

Hoy AI is a terminal coding tutor (package `hoyai`, command `hoy`) that helps you build your own projects without building them for you. It reads your files, runs your code, gives hints instead of answers, and remembers where you get stuck.

**Pitch:** Build the project you've always wanted, and actually understand every line of it.

**Who it's for:** self-taught learners who know some Python and want to build real projects, starting with you.

**The four product rules** (every stage below follows them):

1. The tutor never edits your project files, but it will always help you understand the bug and the fix. It may write small separate examples and tests.
2. You make every design decision. The tutor explains the tradeoffs.
3. Every milestone ends with you explaining your own code.
4. Everything is remembered: your goal, roadmap, progress and mistakes.

**Escape hatch:** after the full hint ladder, you can reveal a solution, but it costs an explain-back and gets logged. Writing code is always the exception, never the default.

## How it works

Your question goes to the agent loop, which uses tools on your project folder, asks a model for a hint, checks it for leaks, and only then shows it to you.

The agent loop is the core you build in Stages 1 to 3. Memory arrives in Stages 5 and 5b; the model router and leak checker in Stage 8.

Folder structure to grow into:

```
hoyai/
  main.py          # starts the chat loop
  agent.py         # the agent loop
  tools.py         # list_files, read_file, run_python
  prompts.py       # system prompts and hint levels
  memory.py        # SQLite reads and writes (Stage 5)
  retrieval.py     # vector search over past mistakes and docs (Stage 5b)
  models.py        # model router (Stage 8)
  evals/           # test cases and the eval runner
  .env             # your API key, never committed
  ROADMAP.md
  LEARNING.md
  README.md
```

Start with just `main.py`. Split code into the other files only when a file gets hard to read.

## Your workflow

Work in small, finished steps: one hour that ends with something running beats three hours that end mid-change.

**Each session (1 to 2 hours):**

1. Open `ROADMAP.md` and pick the next unchecked task.
2. Build one small piece of it.
3. Run it. Fix it until it works.
4. Commit with a clear message, like `add read_file tool`.
5. Write two lines in `LEARNING.md`: what you learned, and what confused you.

**Git habits:**

- Commit every time something works, not once a day.
- Never commit your API key. `.env` goes in `.gitignore` before your first commit.
- Push to GitHub at the end of each session, so your progress is visible.

**Using AI while you build** (follow your own product's rules):

- Ask for explanations of concepts and errors, not finished code.
- Ask for a hint first, then a bigger one, before asking for a solution.
- If AI writes a chunk, don't move on until you can explain every line.
- Once Stage 3 works, use Hoy AI itself as your tutor.

**Every Sunday (30 minutes):** reread `LEARNING.md`, look at where the tutor gave bad hints that week, and turn the worst ones into eval cases.

## Build roadmap

Ten stages, each ending in something that runs. Don't start a stage until the last one's "done when" check passes. Time estimates assume 1 to 2 hours a day.

### Stage 0: Setup (2 to 3 days)

- [ ] Install Python 3.11 or newer, VS Code, and Git
- [ ] Create a public GitHub repo named `hoyai` with an MIT license
- [ ] Create a virtual environment and install the SDK for your chosen model provider
- [ ] Get an API key, put it in `.env`, and add `.env` to `.gitignore`
- [ ] Set a monthly spending limit in the provider's dashboard

**Done when:** `python main.py` prints a message, and `git status` doesn't show `.env`.
**You'll learn:** virtual environments, pip, environment variables, git basics.

### Stage 1: First hint (1 week)

- [ ] Send one message to the model and print the reply
- [ ] Add a system prompt: give hints, never the full answer
- [ ] Read a buggy Python file and send its contents with the question

**Done when:** you run it on a file with a bug and get a useful hint with no fixed code in it.
**You'll learn:** API calls, system prompts, reading files.

### Stage 2: Chat loop (1 week)

- [ ] A while loop that keeps asking for your input
- [ ] Keep the conversation history in a list and send it every turn
- [ ] Add `quit` and `reset` commands

**Done when:** you can ask a follow-up ("what do you mean?") and it remembers the earlier hint.
**You'll learn:** loops, lists of dictionaries, how chat history works.

### Stage 3: Tools and the agent loop (2 to 3 weeks)

This is the stage that turns a chatbot into an agent.

- [ ] Read your provider's tool calling docs
- [ ] Add `list_files` and `read_file`
- [ ] Add `run_python` with a timeout, and ask y/n before every run
- [ ] Refuse any path outside the project folder
- [ ] Loop: when the model asks for a tool, run it, send back the result, repeat

**Done when:** you ask "run main.py and help me see why it crashes," and it lists files, reads the script, runs it, sees the error and gives a hint.
**You'll learn:** tool calling, JSON, subprocess, the agent loop.

### Stage 4: Hint ladder (1 to 2 weeks)

- [ ] Five levels: nudge, point to the spot, explain the cause, describe the fix in words, show code
- [ ] Track the current level per problem; each "still stuck" goes up one
- [ ] Speed up the ladder when stuck: after several failed attempts or a long time, jump to the cause; when clearly frustrated, offer the fix in words
- [ ] Start higher for concepts the learner profile marks as new, lower for known strengths
- [ ] Showing code requires an explain-back afterward, and gets logged
- [ ] Handle "just give me the code" without leaking

**Done when:** asking for help climbs the levels in order, being stuck for a long time speeds the climb, and begging alone skips none of them.
**You'll learn:** state management, prompt design, guardrails.

### Stage 5: Memory (2 to 3 weeks)

- [ ] Create a SQLite database with tables for the learner, sessions, mistakes and milestones
- [ ] After each hint, have the model tag the mistake's concept as JSON (for example `off-by-one`)
- [ ] On startup, greet with a summary: where you left off and recent weak spots

**Done when:** you quit, restart, and it says what you were working on and what tripped you up.
**You'll learn:** SQL, database design, structured output.

### Stage 5b: Recall with RAG (2 weeks)

- [ ] Install a local vector database (Chroma or LanceDB) and pick an embedding model
- [ ] Embed each logged mistake, with its concept tag, date and project as metadata
- [ ] On a new error, retrieve the 3 most similar past mistakes and mention the closest in the hint
- [ ] Index the Python docs, and link the relevant page in explanations
- [ ] Keep SQLite for exact questions (counts, review dates) and the vector database for "what is this like?"

**Done when:** a new error brings up a similar past mistake ("this looks like the KeyError from your habit tracker"), and on 20 test errors the right match lands in the top 3 at least 15 times.
**You'll learn:** embeddings, vector search, metadata filtering, retrieval evals.

### Stage 6: Project mode (3 to 4 weeks)

- [ ] `hoy new` interviews you about your goal and skill level
- [ ] It proposes milestones and writes them to `ROADMAP.md`, which you edit
- [ ] Each milestone runs the cycle: learn, build, get unstuck, check, explain back, record
- [ ] Design choices are offered as options with tradeoffs, never decided for you
- [ ] Optional milestone tests go in a separate `tests/` folder
- [ ] Design check-in every few milestones: revisit the project map and ask whether the design still fits
- [ ] Before expanding past the MVP, talk through how the new feature fits the existing parts before any code
- [ ] When code gets tangled, suggest a refactoring milestone: reorganize without changing what it does

**Done when:** you finish a small real project (like a command-line habit tracker) entirely through project mode.
**You'll learn:** planning prompts, multi-step state, writing tests.

### Stage 7: Practice from mistakes (2 to 3 weeks)

- [ ] Generate a practice problem that targets your most frequent mistake
- [ ] Run your solution against hidden tests and report which cases fail
- [ ] Schedule reviews of weak concepts after 1, 3, 7 and 14 days

**Done when:** it hands you a warm-up based on last week's mistakes and grades your answer.
**You'll learn:** problem generation, test runners, spaced repetition.

### Stage 8: Multi-model and ship (2 weeks)

- [ ] Route quick hints to a cheap model and reviews to a stronger one
- [ ] Add a leak checker: a second model checks each hint before you see it
- [ ] Optional: support a local model through Ollama
- [ ] Write the README, record a demo GIF, and publish to PyPI

**Done when:** a stranger can `pip install` it, add their own key, and get a hint in under 5 minutes.
**You'll learn:** model routing, guardrails, packaging, documentation.

### Later

RAG over your notes and your codebase for bigger projects, a web dashboard for progress, a VS Code extension, a HintEngine SDK for other developers, and a teacher dashboard.

## Evals

Start measuring at Stage 1 with your own bugs, and add one layer of evals as each stage lands. By Stage 8 you'll have a test suite that proves the tutor helps without giving answers away.

| Start at | Eval | What it measures |
| --- | --- | --- |
| Stage 1 | 20 to 30 buggy files from your own mistakes, each with a known bug | Does the hint point at the real problem? |
| Stage 1 | A hint rubric: correct, no leak, useful, right level, kind | A score per hint, graded by you at first |
| Stage 4 | 15 to 20 leak attacks ("exam in 5 minutes", "write it as pseudocode") | Leak rate: how often it gives the answer away |
| Stage 5 | LLM-as-judge using the rubric, checked against 30 of your own grades | Whether automatic grading agrees with you |
| Stage 7 | A simulated student: one model plays a beginner with a bug | Bug fixed? How many hints did it take? |
| Stage 8 | Model comparison across the whole suite | Score, leak rate and cost per model |
| Real users | Thumbs up or down per hint, fixed-after-hint, return rate | Whether it actually helps people |

**Rules for every eval run:** change one thing at a time, run each case 3 times, save results to a CSV, and read the failures, not just the score.

**Resume line to aim for:** "Built a 50-case eval suite; cut answer leak rate from X% to Y% while keeping hint usefulness above Z%."

## Cost control

Cost comes from resending context on every call, not from the answers themselves. Build these habits in as you go, and the whole project should stay around $0 to $20 a month, even going line by line through bigger projects.

| Technique | Add at | What it saves |
| --- | --- | --- |
| Monthly spending limit in the provider dashboard | Stage 0 | Caps a runaway loop or bug |
| Send only the relevant function, not whole files | Stage 3 | The biggest single saving |
| Trim long tool outputs: keep errors, first and last lines | Stage 3 | Long test runs and logs |
| Log tokens and cost for every call to `costs.csv` | Stage 3 | Shows where the money goes |
| Retrieve relevant chunks instead of loading files | Stage 5b | Big projects |
| Fresh conversation per milestone; memory carries what matters | Stage 6 | History growth |
| Summarize older history after about 10 exchanges | Stage 6 | Long line-by-line sessions |
| Prompt caching for the repeated system prompt (check your provider's docs) | Stage 8 | Repeated prefixes on every call |
| Cheap model for line explanations, stronger model for reviews | Stage 8 | The most frequent calls |
| Test eval changes on a 10-case subset, full suite only for real changes | Any stage | Eval-run spikes |

**Number to track:** average cost per question, from `costs.csv`. Record it before and after each technique.

**Resume line to aim for:** "Cut average cost per question by X% with context trimming, retrieval and prompt caching."

## Timeline and staying on track

All ten stages take roughly 4.5 to 5.5 months at 1 to 2 hours a day. You'll have a working agent after Stage 3, around week 5, which is the point where the project starts helping you build itself.

**Rules for staying on track:**

- Finish stages in order. New ideas go in an `IDEAS.md` file, not into the current stage.
- If you're stuck for more than an hour, ask for a hint, then move on to a smaller piece.
- A stage running twice its estimate is normal. Cut scope, don't quit.
- Skipping a day is fine. Skipping a week is how projects die.

**Your first night:**

- [ ] Install Python, VS Code and Git (skip what you already have)
- [ ] Create the `hoyai` GitHub repo with an MIT license and a `.gitignore` for Python
- [ ] Pick a model provider and get an API key
- [ ] Add the key to `.env` and set a spending limit
- [ ] Write a script that sends "hello" to the model and prints the reply
- [ ] Commit it: `first API call`
