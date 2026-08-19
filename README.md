# Starfall Defence Corps Academy

> 🧭 [← Gateway Simulation](https://github.com/starfall-defence-corps/gateway-simulation) · **You are here: 2.1 Weapon Handling Test** · [2.2 Compliance as Code →](https://github.com/starfall-defence-corps/mission-2-2-compliance-as-code) · [🏠 Academy Hub](https://github.com/starfall-defence-corps/sdc-academy)

> ☁️ **No Docker on your machine?** Create your own copy first (Use this template), then on **your** repo: **Code → Codespaces → Create codespace** — everything is preinstalled. First boot takes ~5 min (one-time); after that it starts fast.

## Mission 2.1: Weapon Handling Test

> *"Private YOLO-Deploy pushed untested code to production. Friday. 16:59. Three nodes down. 'I ran it locally and it worked.' This is why we have the WHT."*

You are a newly-minted Ensign at the Starfall Defence Corps Academy. You know Ansible. Now prove you can test it. This mission teaches Molecule and Testinfra — the tools that ensure your roles work before they touch production.

## Prerequisites

- Completed Module 1 (Missions 1.1–1.5 + Gateway Simulation)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (with Docker Compose v2)
- [GNU Make](https://www.gnu.org/software/make/)
- Python 3.10+ (with `python3-venv`)
- Git

> **Windows users**: Install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) and run all commands from within your WSL terminal.

## Quick Start

```bash
git clone https://github.com/YOUR-USERNAME/mission-2-1-weapon-handling-test.git
cd mission-2-1-weapon-handling-test
make setup
source venv/bin/activate
```

Read your orders: [Mission Briefing](docs/BRIEFING.md)

## Lab Architecture

```
 WHT Range                          Fleet
+------------------+    +----------------------------------+
| wht-ssh  :2241   |    | sdc-web   :2221  (Ubuntu 22.04) |
| Ubuntu 22.04     |    | sdc-db    :2222  (Rocky Linux 9) |
| SSH target       |    | sdc-comms :2223  (Ubuntu 22.04) |
+------------------+    +----------------------------------+
| wht-web  :2242   |
| Ubuntu + nginx   |
+------------------+
```

## Mission Structure

| Part | Description | Location |
|------|-------------|----------|
| Obstacle Course 1 | Given tests, write the role | `workspace/obstacle-course/mission-1/` |
| Obstacle Course 2 | Given buggy role, write tests | `workspace/obstacle-course/mission-2/` |
| Main Mission | Test your fleet_hardening role | `workspace/main-mission/` |

## Available Commands

```
make help          Show available commands
make setup         Launch WHT range + fleet (5 containers)
make test          Ask ARIA to verify your work
make reset         Destroy and rebuild all nodes
make destroy       Tear down everything
make ssh-wht-ssh   SSH into obstacle course target 1
make ssh-wht-web   SSH into obstacle course target 2
make ssh-web       SSH into sdc-web (fleet)
make ssh-db        SSH into sdc-db (fleet)
make ssh-comms     SSH into sdc-comms (fleet)
```

## ARIA Review (Pull Request Workflow)

**Locally** — run `make test` for instant verification.

**On Pull Request** — push your work, open a PR, ARIA reviews automatically.

To enable PR reviews, add `ANTHROPIC_API_KEY` to your repo's Secrets.
