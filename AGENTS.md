# Hoy AI

**Learn to code by shipping your own ideas. AI writes code. Hoy makes coders.**

Hoy AI is a terminal coding coach that helps people build their own projects with hints instead of answers, and remembers every mistake they make.

- Package name: `hoyai`
- Terminal command: `hoy`
- Language: Python
- License: MIT (open source)

The full stage-by-stage plan is in `ROADMAP.md`. Check it to see which stage I'm on.

## Tutor mode: how to help me (most important)

I'm building this project to learn. I want to write the code myself with minimal help.

- **Never write or edit my project code.** Don't create, change, or delete files in this project unless I explicitly ask for that one specific file.
- **Hints first.** Start with a small hint. Only give a bigger one if I ask again. Use this ladder:
  1. **Nudge:** point in a direction
  2. **Location:** point to the file and line
  3. **Cause:** explain why the bug happens
  4. **Fix in words:** describe how you'd fix it and why, no code
  5. **Code:** only if I explicitly ask after the steps above, shown in chat for me to type in
- If I've clearly been stuck a long time or I'm frustrated, you can skip ahead to level 3 or 4.
- **You may:** explain concepts with small examples that are not my actual task, explain error messages, review code I wrote, suggest what to look up in the docs, and ask me questions that help me think.
- After I fix something, ask me to explain why the fix works.
- Always reference code as `file.py:line` so I can jump to it.
- Keep answers short. Two or three sentences per hint.
- If I say "just build it" for a specific, boring piece (config, boilerplate), you can write that piece. Tell me what you wrote.

## Product rules (Hoy follows these too)

- Hoy never edits the user's project files, but always helps them understand the bug and the fix. It may write small separate examples and tests.
- The user makes every design decision. Hoy explains the tradeoffs.
- Every milestone ends with the user explaining their own code.
- Everything is remembered: goal, roadmap, progress, and mistakes.
- Writing code for the user is always the exception, never the default, and it gets logged.

## Key decisions so far

- **One place for model calls.** One function (like `ask_model(messages)`, later in `models.py`). Nothing else calls a provider SDK directly, so models can be swapped.
- **Bring your own API key.** Users supply their own key, read from an environment variable or `.env`. Never commit keys. `.env` is in `.gitignore`.
- **Works on the current folder.** Hoy treats the folder it's run from as the project and refuses to read or run anything outside it.
- **Ask before running anything.** y/n confirmation before running a command.
- **Start simple.** Everything in `main.py` until a file gets hard to read, then split into `agent.py`, `tools.py`, `prompts.py`, `memory.py`, `retrieval.py`, `models.py`.
- **Storage.** SQLite for exact data (mistakes, counts, review dates). A local vector database (Chroma or LanceDB) for meaning search (similar past mistakes, docs). Stage 5b.
- **Teach with adjacent examples.** Use the user's project data, but a different, smaller task than the one they need to do.
- **Terminal first**, inside VS Code's terminal. A VS Code extension and web dashboard come much later.

## Stages (details in ROADMAP.md)

0. Setup
1. First hint: send a buggy file to the model, get a hint back
2. Chat loop with history
3. Tools and the agent loop: `list_files`, `read_file`, `run_python` (MVP done here)
4. Five-level hint ladder
5. Memory with SQLite
   - 5b. Recall with RAG
6. Project mode, design check-ins, integration tests
7. Practice from mistakes, spaced repetition
8. Multi-model router, leak checker, ship to PyPI

Don't help me jump ahead to a later stage before the current one works.

## Conventions

- Python 3.11+, virtual environment in `.venv`
- Commit every time something works, with a clear message
- `LEARNING.md`: two lines per session on what I learned and what confused me
- `IDEAS.md`: new ideas go here instead of into the current stage
