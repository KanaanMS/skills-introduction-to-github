# Beginner Checklist for the Cloud AI SaaS Coursework

If you are brand new to the tooling and concepts used in this coursework, use this checklist as a companion to the main README. Each block indicates *exactly* what you need to install or type so you can build confidence step by step.

## 1. Prepare your workstation

1. **Install Git**
   - Windows: install [Git for Windows](https://git-scm.com/download/win) and select the default options.
   - macOS: install the Xcode Command Line Tools by running `xcode-select --install`.
   - Linux: use your package manager, e.g. `sudo apt install git` on Ubuntu/Debian.
2. **Install Python 3.10 or newer**
   - Download from [python.org](https://www.python.org/downloads/) (Windows/macOS) and tick *"Add Python to PATH"* during installation.
   - On Linux, use your package manager: `sudo apt install python3 python3-venv python3-pip`.
3. **Install Docker Desktop** (needed from Stage 2 onwards)
   - Windows/macOS: download from [docker.com](https://www.docker.com/get-started/).
   - Linux: follow the [official engine instructions](https://docs.docker.com/engine/install/).
4. **Create a GitHub account** if you do not already have one. You will use it to push your work and open pull requests.

> ✅ *Checkpoint:* you can run `git --version`, `python --version`, and `docker --version` in a terminal and receive version numbers.

## 2. Clone the coursework repository

```bash
# Replace YOUR-USERNAME with your GitHub handle
git clone https://github.com/YOUR-USERNAME/skills-introduction-to-github.git
cd skills-introduction-to-github
```

Set up the Git remotes if you are working from a classroom fork:

```bash
git remote add upstream https://github.com/kcl-5ccsacca/skills-introduction-to-github.git
```

> ✅ *Checkpoint:* `git remote -v` should list both `origin` (your fork) and `upstream` (the classroom template).

## 3. Adopt the GitFlow branch model

1. Start a development branch for each stage:
   ```bash
   git checkout -b feature/stage-01-vision-prototype
   ```
2. Make changes, then commit with a meaningful message:
   ```bash
   git status
   git add src/main.py
   git commit -m "Implement YOLO inference endpoint"
   ```
3. Push the branch and open a pull request in GitHub targeting `develop`:
   ```bash
   git push origin feature/stage-01-vision-prototype
   ```
4. After review, merge the pull request into `develop`, then promote stable milestones to `main`.

> ✅ *Checkpoint:* run `git branch` locally and confirm you are on the correct feature branch before editing files.

## 4. Create a Python virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

This isolates your coursework dependencies from other Python projects on your machine.

> ✅ *Checkpoint:* the terminal prompt shows `(.venv)` at the beginning while the environment is active.

## 5. Run the FastAPI server for the first time

1. Ensure the virtual environment from the previous step is active.
2. Start the application:
   ```bash
   uvicorn src.main:app --reload
   ```
3. Open your browser to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) and execute the sample requests shown there.

If you see validation errors or missing dependency warnings, double-check that `requirements.txt` was installed inside the virtual environment.

> ✅ *Checkpoint:* the `/health` endpoint returns JSON containing `{"vision_backend": "mock", "language_backend": "mock"}` by default.

## 6. Record your progress in the README

After you complete a stage:

- Add a short note under **Next Steps** describing what changed.
- Update `docs/costs.md` with any new assumptions relevant to Stage 8.
- Link to any scripts, database migrations, or configuration files that were introduced.

Keeping the documentation up to date will make the final video much easier to prepare.

## 7. Prepare for upcoming stages

- **Stage 2:** read tutorials on Dockerfiles and Docker Compose. Save links in `docs/` for quick reference.
- **Stage 4:** research lightweight databases (SQLite, PostgreSQL) and decide which one fits your constraints.
- **Stage 5 & 7:** create a Firebase project ahead of time so you can integrate storage and authentication without rushing.
- **Stage 9:** bookmark monitoring solutions (Prometheus, Grafana, OpenTelemetry). Note how they deploy inside Docker Compose.

## 8. Practice the submission workflow

1. Run the automated tests locally:
   ```bash
   pytest
   ```
2. Build and run the Docker image (after Stage 2):
   ```bash
   docker compose build
   docker compose up
   ```
3. Keep a log of commands you use to deploy or test the system. These will appear in the final video alongside Git history.

> ✅ *Final checkpoint:* you are comfortable cloning the repo, creating feature branches, running the FastAPI app, and pushing commits for review.

Feel free to copy this checklist into your notes and tick items off as you progress. When you encounter blockers, capture them as GitHub Issues so you can discuss them with peers or demonstrators.
