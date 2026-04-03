---
CLASSIFICATION: LIEUTENANT JG EYES ONLY
MISSION: 2.1 — WEAPON HANDLING TEST
THEATRE: Starfall Defence Corps Academy
AUTHORITY: SDC Cyber Command, 2187
---

# OPERATION ORDER — MISSION 2.1: WEAPON HANDLING TEST

---

## 1. SITUATION

### 1a. Enemy Forces

Voidborn operative **PRIVATE YOLO-DEPLOY** pushed a "hardening" role to production. No tests. No review. Friday. 16:59. Three nodes went down. His defence: *"I ran it locally and it worked."*

This is why the Starfall Defence Corps requires the Weapon Handling Test. You do not deploy what you have not tested. Ever.

### 1b. Friendly Forces

You have earned the rank of Ensign through Module 1. You know Ansible: inventory, playbooks, templates, roles, vault. But you have never written a test. Every test so far was written for you by ARIA.

That changes now. You will learn Molecule and Testinfra — the tools that prove your roles work before they touch production.

### 1c. Attachments / Support

**ARIA** verifies your test-writing ability. She checks that your tests exist, are meaningful, and catch real bugs.

---

## 2. MISSION

Three parts: the WHT Range (timed obstacle course), then the main mission.

| Part | Objective |
|------|-----------|
| WHT Range — Mission 1 | Given 5 tests, write the role that passes them |
| WHT Range — Mission 2 | Given a buggy role, write tests that catch the bug |
| Main Mission | Write Molecule tests for your fleet_hardening role |

---

## 3. EXECUTION

### 3a. Commander's Intent

Private YOLO-Deploy represents the worst case: untested infrastructure pushed to production. The WHT ensures you never make that mistake. By the end of this mission, you will be able to write Testinfra tests for any Ansible role and run them with Molecule.

### 3b. WHT Range — Obstacle Course (Timed)

> **START YOUR TIMER**

#### Mission 1: Write the Role (15–20 min)

**Location**: `workspace/obstacle-course/mission-1/`

You are given 5 Testinfra tests in `tests/test_ssh_hardening.py`. Read them. Each test describes an expected state. Your job: write the Ansible role that makes all 5 pass.

**Target**: `wht-ssh` (Ubuntu 22.04, port 2241)

Steps:
1. Read the 5 tests — they are your specification
2. Create the role: `ansible-galaxy init roles/ssh_hardening`
3. Write tasks that satisfy each test
4. Apply: `ansible-playbook -i inventory.yml site.yml`
5. Verify: `pytest tests/ --hosts=ssh://cadet@localhost:2241 --ssh-identity-file=../../.ssh/cadet_key --ssh-config=/dev/null -v`
6. Iterate until all 5 pass

#### Mission 2: Write the Tests (15–20 min)

**Location**: `workspace/obstacle-course/mission-2/`

You are given a working `web_server` role that installs and configures nginx. The role works — but it has **security bugs**. Your job: write Testinfra tests that catch the bugs.

**Target**: `wht-web` (Ubuntu 22.04, port 2242)

Steps:
1. Read the role: `roles/web_server/tasks/main.yml` and `templates/nginx.conf.j2`
2. Apply the role: `ansible-playbook -i inventory.yml site.yml`
3. Create `tests/test_web_server.py` with at least 4 tests:
   - Basic checks (package installed, service running, port listening)
   - Security checks that expose the bugs
4. Run your tests: `pytest tests/test_web_server.py --hosts=ssh://cadet@localhost:2242 --ssh-identity-file=../../.ssh/cadet_key --ssh-config=/dev/null -v`
5. Some tests should PASS (basic checks), some should FAIL (bug catches)

> **STOP YOUR TIMER**

| Time | Rating |
|------|--------|
| Under 30 min | Sharpshooter |
| 30–40 min | Marksman |
| 40–50 min | Qualified |
| 50–60 min | Basic |
| 60+ min | Weapon Returned — retry |

### 3c. Main Mission: Test Everything

**Location**: `workspace/main-mission/`

Write a complete test scenario for the `fleet_hardening` role from Mission 1.5. You will need to:

1. Copy (or recreate) your `fleet_hardening` role into `main-mission/roles/`
2. Create `inventory/hosts.yml` and `group_vars/` for the fleet
3. Create `site.yml` that calls the role
4. Create `molecule/default/molecule.yml`
5. Create `tests/test_fleet_hardening.py` with at least 8 tests covering:
   - SSH hardening (PermitRootLogin, PasswordAuthentication)
   - SSH service running
   - Firewall active (both OS families)
   - MOTD deployed
   - Telnet removed
   - Any other hardening your role performs
6. Apply the role and verify your tests pass

**Fleet nodes**: sdc-web (Ubuntu, 2221), sdc-db (Rocky, 2222), sdc-comms (Ubuntu, 2223)

### 3d. Testinfra Quick Reference

```python
# Package
host.package("nginx").is_installed

# Service
host.service("ssh").is_running
host.service("ssh").is_enabled

# File
host.file("/etc/ssh/sshd_config").exists
host.file("/etc/ssh/sshd_config").contains("PermitRootLogin no")
host.file("/etc/ssh/sshd_config").mode == 0o644

# Socket
host.socket("tcp://0.0.0.0:22").is_listening

# Command
result = host.run("ufw status")
assert "Status: active" in result.stdout

# System info
host.system_info.type == "linux"
host.system_info.distribution == "ubuntu"
```

### 3e. Running Tests with pytest-testinfra

```bash
# Against a single host
pytest tests/ --hosts=ssh://cadet@localhost:2241 \
  --ssh-identity-file=../../.ssh/cadet_key \
  --ssh-config=/dev/null -v

# Against multiple hosts
pytest tests/ \
  --hosts=ssh://cadet@localhost:2221,ssh://cadet@localhost:2222,ssh://cadet@localhost:2223 \
  --ssh-identity-file=../.ssh/cadet_key \
  --ssh-config=/dev/null -v
```

---

## 4. SUPPORT

| Resource | Command |
|----------|---------|
| ARIA verification | `make test` |
| Testinfra docs | `python3 -c "import testinfra; help(testinfra)"` |
| Fleet reset | `make reset` |

---

## 5. COMMAND AND SIGNAL

**Commander's Final Order**: Private YOLO-Deploy's era is over. From this point forward, every role you write will be tested. Every deployment will be verified. The WHT proves you understand this. Write the tests. Run them. Trust nothing until Molecule confirms it.

Proceed to the obstacle course. Start your timer.

---

*SDC Cyber Command — 2187 — LIEUTENANT JG EYES ONLY*
