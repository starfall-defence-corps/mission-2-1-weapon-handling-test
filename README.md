# Starfall Defence Corps Academy

> 🧭 [← Gateway Simulation](https://github.com/starfall-defence-corps/gateway-simulation) · **You are here: 2.1 Weapon Handling Test** · [2.2 Compliance as Code →](https://github.com/starfall-defence-corps/mission-2-2-compliance-as-code) · [🏠 Academy Hub](https://github.com/starfall-defence-corps/sdc-academy) · [📚 Field Manuals](https://github.com/starfall-defence-corps/sdc-academy/tree/main/field-manuals)

> ☁️ **No Docker on your machine?** Create your own copy first (Use this template), then on **your** repo: **Code → Codespaces → Create codespace** — everything is preinstalled. First boot takes ~5 min (one-time); after that it starts fast.

## Mission 2.1: Weapon Handling Test

> *"Reaver YOLO-Deploy pushed untested code to production. Friday. 16:59. Three nodes down. 'I ran it locally and it worked.' This is why we have the WHT."*

You are a newly-minted Lieutenant at the Starfall Defence Corps Academy. You know Ansible. Now prove you can test it. This mission teaches Molecule and Testinfra — the tools that ensure your roles work before they touch production.

This is the first mission of **Module 2: Advanced Individual Training**. Scaffolding is reduced from here on: you get a briefing, a set of targets, and ARIA's pass/fail verdict.

## Briefing

Voidborn operative **Reaver YOLO-Deploy** pushed a "hardening" role to production with no tests and no review. Three nodes went down. Up to now, every test you have run was written for you by ARIA. That changes here: you learn to write the tests yourself, in both directions — code that satisfies a test, and tests that expose bad code.

The mission has three parts: a timed obstacle course on the **WHT Range** (two missions), then the main mission against the fleet. Full orders are in the [Mission Briefing](docs/BRIEFING.md).

## Objectives

`make test` verifies three phases. Each phase maps to one part of the mission:

| Phase | Part | ARIA checks |
|-------|------|-------------|
| 1 | Obstacle Course — Mission 1: *Write the Role* | An `ssh_hardening` role exists in `workspace/obstacle-course/mission-1/roles/` with at least 3 tasks, applies to `wht-ssh` without errors, and all 5 provided Testinfra tests in `tests/test_ssh_hardening.py` pass |
| 2 | Obstacle Course — Mission 2: *Write the Tests* | You have written `workspace/obstacle-course/mission-2/tests/test_web_server.py` with at least 4 test functions; the provided `web_server` role applies to `wht-web`; and your tests produce a mix of passes (basic checks) and failures (the planted security bugs) |
| 3 | Main Mission: *Test Everything* | `workspace/main-mission/` contains your `fleet_hardening` role, a `site.yml`, `molecule/default/molecule.yml`, and Testinfra tests with at least 8 test functions — and those tests pass against all three fleet nodes after the role is applied |

In Mission 2 you are **not** fixing the role. Failing tests are the evidence that the bugs exist.

## What You'll Learn

- How Molecule is structured: `molecule.yml`, platforms, and the create → converge → verify → destroy lifecycle
- Pointing Molecule at machines that already exist (`managed: false` platforms)
- Writing Testinfra tests with `host.package()`, `host.service()`, `host.file()`, `host.socket()` and `host.run()`
- Running Testinfra against remote hosts over SSH with `pytest --hosts=ssh://…`
- Test-driven infrastructure: reading tests as a specification, then writing the role to meet it
- Writing tests that catch defects in a role someone else wrote
- Testing one role across two OS families (Ubuntu and Rocky Linux)

## Prerequisites

- Completed Module 1 (Missions 1.1–1.6 + Gateway Simulation) — the main mission tests your `fleet_hardening` role from [Mission 1.5](https://github.com/starfall-defence-corps/mission-1-5-clean-house)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (with Docker Compose v2)
- [GNU Make](https://www.gnu.org/software/make/)
- **Ansible, Molecule and pytest-testinfra**: provided by the lab — `make setup` builds a local venv from `requirements.txt`; no host install needed
- Python 3.10+ (with `python3-venv`)
- Git

> **Windows users**: Install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) and run all commands from within your WSL terminal.

## Quick Start

```bash
# 1. Use this template on GitHub (green button, top right) to create YOUR OWN
#    copy. Set it Public, then clone it:
git clone https://github.com/YOUR-USERNAME/mission-2-1-weapon-handling-test.git
cd mission-2-1-weapon-handling-test

# 2. Check your machine is mission-ready
make doctor

# 3. Launch the WHT Range + fleet (5 containers)
make setup

# 4. Activate the virtual environment
source venv/bin/activate
```

5. **Read your orders**: [Mission Briefing](docs/BRIEFING.md)
6. **Work the phases**: [Exercises](docs/EXERCISES.md)
7. **Stuck?** [Hints & Troubleshooting](docs/HINTS.md)
8. **Track progress**: [Checklist](CHECKLIST.md)
9. **Ready?** `make test`, then `make submit`

Run every command — `ansible-playbook`, `pytest` and `make` — from the **project root** (the folder with the `Makefile`). An `ansible.cfg` lives there, so no `cd` is needed.

## Lab Architecture

```
 Your Machine
+---------------------------------------------------------------+
|  workspace/                                                   |
|    obstacle-course/mission-1/   (given tests → you write role) |
|    obstacle-course/mission-2/   (given role → you write tests) |
|    main-mission/                (you build everything)         |
|    .ssh/cadet_key               (auto-generated)               |
|    .ssh/testinfra_ssh_config    (auto-generated)               |
|                                                               |
|   WHT Range                     Fleet                         |
|  +------------------+   +----------------------------------+  |
|  | wht-ssh  :2241   |   | sdc-web   :2221  (Ubuntu 22.04)  |  |
|  | Ubuntu 22.04     |   | sdc-db    :2222  (Rocky Linux 9) |  |
|  | SSH target       |   | sdc-comms :2223  (Ubuntu 22.04)  |  |
|  +------------------+   +----------------------------------+  |
|  | wht-web  :2242   |                                         |
|  | Ubuntu + nginx   |                                         |
|  +------------------+                                         |
+---------------------------------------------------------------+
```

| Node | Used in | OS | SSH port |
|------|---------|----|----------|
| `wht-ssh` | Obstacle Course — Mission 1 | Ubuntu 22.04 | 2241 |
| `wht-web` | Obstacle Course — Mission 2 | Ubuntu 22.04 + nginx | 2242 |
| `sdc-web` | Main Mission | Ubuntu 22.04 | 2221 |
| `sdc-db` | Main Mission | Rocky Linux 9 | 2222 |
| `sdc-comms` | Main Mission | Ubuntu 22.04 | 2223 |

All nodes accept SSH as `cadet` with the key `make setup` generates. `make setup` also writes `workspace/.ssh/testinfra_ssh_config`, which you pass to `pytest --ssh-config=…` so your local SSH config does not interfere.

## Mission Structure

| Part | Description | Location |
|------|-------------|----------|
| Obstacle Course 1 | Given 5 tests, write the role | `workspace/obstacle-course/mission-1/` |
| Obstacle Course 2 | Given a buggy role, write tests that catch the bugs | `workspace/obstacle-course/mission-2/` |
| Main Mission | Write Molecule + Testinfra tests for your `fleet_hardening` role | `workspace/main-mission/` |

The obstacle course is timed (start the timer before Mission 1, stop it after Mission 2):

| Time | Rating |
|------|--------|
| Under 30 min | Sharpshooter |
| 30–40 min | Marksman |
| 40–50 min | Qualified |
| 50–60 min | Basic |
| 60+ min | Weapon Returned — retry |

The timer is yours to keep — `make test` grades correctness, not time. The main mission's expected layout is described in [`workspace/main-mission/README.md`](workspace/main-mission/README.md).

## Available Commands

```
make help          Show available commands
make doctor        Check your machine is mission-ready (Docker, ports, tools)
make setup         Launch WHT range + fleet (5 containers)
make test          Ask ARIA to verify your work
make submit        Submit your work for ARIA review (branch, commit, push, PR)
make reset         Destroy and rebuild all nodes
make destroy       Tear down everything
make ssh-wht-ssh   SSH into wht-ssh (obstacle course target 1, port 2241)
make ssh-wht-web   SSH into wht-web (obstacle course target 2, port 2242)
make ssh-web       SSH into sdc-web (fleet, Ubuntu, port 2221)
make ssh-db        SSH into sdc-db (fleet, Rocky Linux, port 2222)
make ssh-comms     SSH into sdc-comms (fleet, Ubuntu, port 2223)
```

> **Note:** `make submit` uses the [GitHub CLI](https://cli.github.com/) — install `gh` and run `gh auth login` once before your first submission.

## Mission Files

| File | Purpose |
|------|---------|
| [BRIEFING.md](docs/BRIEFING.md) | Mission briefing (operation order) — **read this first** |
| [EXERCISES.md](docs/EXERCISES.md) | Phase-by-phase guide: Molecule and Testinfra primer, obstacle course, main mission |
| [HINTS.md](docs/HINTS.md) | Troubleshooting and hints |
| [CHECKLIST.md](CHECKLIST.md) | Progress tracker, with space to record your obstacle-course time |

## Checking Your Work: `make test`

`make test` runs ARIA's grader (`molecule/default/tests/test_wht.py`) against the running lab and reports each objective, phase by phase. For the live checks it applies your playbooks and runs your Testinfra tests against the containers, so the lab must be up (`make setup`). It needs no API key and works offline.

- Run it as often as you like. If a node gets into a state you can't explain, `make reset` rebuilds the containers; your `workspace/` files are preserved.
- The mission is complete when all three phases are green.

You can also run any Testinfra suite yourself while you work — the exact `pytest` commands are in [EXERCISES.md](docs/EXERCISES.md).

## Submission and ARIA Review

When `make test` is green, `make submit` creates a `mission-submission` branch (or uses your current branch if you are not on `main`), commits `workspace/` and `CHECKLIST.md`, pushes, and opens a pull request to `main` in **your own** copy. You can also do this by hand with `git` and the GitHub web UI.

Opening or updating the pull request runs the **ARIA Review** workflow (`.github/workflows/aria-review.yml`). It does not re-run the grader — the deterministic checks need the Docker lab, so your local `make test` is the verdict. Instead, ARIA reads your submitted workspace files and posts a qualitative, in-character code review as a PR comment. Each new push updates the same comment.

To enable PR reviews, add an API key to your repo:
1. Get a key from [platform.claude.com](https://platform.claude.com/)
2. In your repo: **Settings** > **Secrets and variables** > **Actions** > **New repository secret**
3. Name: `ANTHROPIC_API_KEY`, Value: your key

Without a key, the comment says the review was skipped and the check still passes; `make test` works locally either way.

## Hints Policy

At Lieutenant rank, hints are minimal. [HINTS.md](docs/HINTS.md) covers connection problems, where to run commands from, and short pointers per part. The tests are your specification: read the test names and assertions first, then ARIA's messages in `make test`, then the hints. [EXERCISES.md](docs/EXERCISES.md) is the step-by-step guide if you need it. For deeper reference, see [FM-3 — Molecule & Testing Reference](https://github.com/starfall-defence-corps/sdc-academy/blob/main/field-manuals/FM-3-molecule-testing-reference.md).

## Troubleshooting

**"Connection refused" or "Permission denied" from Testinfra**: Check the containers are running (`docker ps` should show all 5) and that your `pytest` command points at the right port, `workspace/.ssh/cadet_key` and `workspace/.ssh/testinfra_ssh_config`.

**Tests fail against a correct role**: Pass `--sudo`. Some checks read root-owned state.

**`make test` fails with "No module named pytest"**: Run `make setup` first — it creates the Python virtual environment.

**Need a clean slate**: `make reset` destroys and rebuilds all nodes; `make destroy` tears everything down.
