# Mission 2.1: Weapon Handling Test — Exercises

**Rank**: Lieutenant JG
**Prerequisite**: Module 1 complete (Missions 1.1–1.5 + Gateway Simulation)

---

## Phase 0: Activate Your Environment

```bash
make setup
source venv/bin/activate
```

Verify 5 containers are running: `docker ps` should show wht-ssh, wht-web, sdc-web, sdc-db, sdc-comms.

---

## Phase 1: Understanding Molecule and Testinfra

Before the obstacle course, you need to understand the tools.

### What Molecule Is

Molecule is a testing framework for Ansible roles. It automates the cycle:

```
create → converge → verify → destroy
```

| Step | What happens |
|------|-------------|
| **create** | Spins up test infrastructure (Docker containers, VMs, etc.) |
| **converge** | Runs your Ansible playbook against the test infrastructure |
| **verify** | Runs Testinfra tests to check the resulting state |
| **destroy** | Tears down the test infrastructure |

In this mission, we use **pre-existing containers** (`managed: false`) instead of having Molecule create them. This means you skip create/destroy and focus on converge/verify.

### The molecule.yml File

Every Molecule scenario lives in `molecule/<scenario>/molecule.yml`. Here's the anatomy:

```yaml
# What driver manages the test infrastructure
driver:
  name: default            # 'default' for pre-existing hosts

# What hosts to test against
platforms:
  - name: sdc-web          # Must match your inventory hostname
    managed: false          # We manage the container, not Molecule
    groups:                 # Ansible groups this host belongs to
      - fleet
      - debian

# How Ansible runs
provisioner:
  name: ansible
  inventory:
    links:
      hosts: inventory/hosts.yml   # Point to your inventory

# What test framework to use
verifier:
  name: testinfra
  directory: tests/         # Where to find test files
```

**Key concept**: `managed: false` means the container already exists (started by `make setup`). Molecule just connects to it. This is what we use throughout the Academy.

### What Testinfra Is

Testinfra is a pytest plugin that lets you write tests about the **state of a remote system**. Instead of testing Python code, you test infrastructure.

Every test function receives a `host` fixture that represents a remote machine:

```python
def test_something(host):
    # host gives you access to the remote system
    result = host.run("whoami")
    assert result.stdout.strip() == "root"
```

### Testinfra Helpers

Testinfra provides high-level helpers so you don't have to shell out for everything:

```python
# Package — is it installed?
host.package("nginx").is_installed          # True/False

# Service — is it running? enabled at boot?
host.service("ssh").is_running              # True/False
host.service("ssh").is_enabled              # True/False

# File — does it exist? what's in it?
host.file("/etc/ssh/sshd_config").exists    # True/False
host.file("/etc/ssh/sshd_config").contains("PermitRootLogin no")
host.file("/etc/motd").content_string       # Full file content
host.file("/etc/shadow").mode               # 0o640 (octal)
host.file("/etc/shadow").user               # "root"
host.file("/etc/shadow").group              # "shadow"

# Socket — is something listening?
host.socket("tcp://0.0.0.0:22").is_listening
host.socket("tcp://0.0.0.0:80").is_listening

# Command — run anything
result = host.run("ufw status")
result.stdout      # standard output
result.stderr      # standard error
result.rc          # exit code (0 = success)

# System info
host.system_info.type           # "linux"
host.system_info.distribution   # "ubuntu" or "rocky"
```

### Running Testinfra Tests

Tests run with pytest. You specify the target host(s) via `--hosts`:

```bash
# Single host
pytest tests/ \
  --hosts=ssh://cadet@localhost:2241 \
  --ssh-identity-file=../../.ssh/cadet_key \
  --ssh-config=../../.ssh/testinfra_ssh_config \
  --sudo -v

# Multiple hosts (comma-separated)
pytest tests/ \
  --hosts=ssh://cadet@localhost:2221,ssh://cadet@localhost:2222,ssh://cadet@localhost:2223 \
  --ssh-identity-file=../.ssh/cadet_key \
  --ssh-config=../.ssh/testinfra_ssh_config \
  --sudo -v
```

| Flag | Purpose |
|------|---------|
| `--hosts=ssh://user@host:port` | Target host(s) to test against |
| `--ssh-identity-file=PATH` | SSH private key for authentication |
| `--ssh-config=PATH` | SSH config (we use one that disables host key checking) |
| `--sudo` | Run commands as root on the remote host |
| `-v` | Verbose output (shows each test name and result) |

### Writing a Test File

Test files are Python files named `test_*.py`. Each test function starts with `test_`:

```python
"""Tests for my_role."""


def test_ssh_is_hardened(host):
    """SSH must disable root login."""
    sshd = host.file("/etc/ssh/sshd_config")
    assert sshd.exists
    assert sshd.contains("PermitRootLogin no")


def test_firewall_is_active(host):
    """UFW must be running."""
    result = host.run("ufw status")
    assert "Status: active" in result.stdout
```

**Tips**:
- One assertion per concept (don't cram unrelated checks into one test)
- Test names should describe the expected state, not the implementation
- Use docstrings — they appear in test output
- Test for **absence** of bad config too, not just presence of good config

### Multi-OS Testing

When testing against a mixed fleet, some checks only apply to certain OS families:

```python
def test_ufw_active(host):
    """UFW firewall active on Debian hosts."""
    if host.system_info.distribution not in ("ubuntu", "debian"):
        return  # Skip on non-Debian
    result = host.run("ufw status")
    assert "Status: active" in result.stdout


def test_firewalld_running(host):
    """firewalld running on RedHat hosts."""
    if host.system_info.distribution in ("ubuntu", "debian"):
        return  # Skip on Debian
    svc = host.service("firewalld")
    assert svc.is_running
```

---

## Phase 2: WHT Range — Obstacle Course

> **START YOUR TIMER**

### Mission 1: Write the Role (15–20 min)

**Location**: `workspace/obstacle-course/mission-1/`

```bash
cd workspace/obstacle-course/mission-1
```

1. **Read the 5 tests** at `tests/test_ssh_hardening.py`. Each test is your specification — it tells you exactly what state the system must be in.

2. **Create the role**:
   ```bash
   ansible-galaxy init roles/ssh_hardening
   ```

3. **Write tasks** in `roles/ssh_hardening/tasks/main.yml` that satisfy each test. Don't overthink it — you've done all of this in Module 1.

4. **Apply the role**:
   ```bash
   ansible-playbook -i inventory.yml site.yml
   ```

5. **Run the tests**:
   ```bash
   pytest tests/ --hosts=ssh://cadet@localhost:2241 \
     --ssh-identity-file=../../.ssh/cadet_key \
     --ssh-config=../../.ssh/testinfra_ssh_config \
     --sudo -v
   ```

6. **Iterate** until all 5 pass. Read failure messages — they tell you what's wrong.

### Mission 2: Write the Tests (15–20 min)

**Location**: `workspace/obstacle-course/mission-2/`

```bash
cd workspace/obstacle-course/mission-2
```

1. **Read the role**: Examine `roles/web_server/tasks/main.yml` and `roles/web_server/templates/nginx.conf.j2`. The role works, but it has **security bugs**.

2. **Apply the role**:
   ```bash
   ansible-playbook -i inventory.yml site.yml
   ```

3. **Write tests** at `tests/test_web_server.py`. Include:
   - Basic checks: package installed, service running, port listening, config exists
   - Security checks: find what's wrong in the nginx config and write tests that catch it

4. **Run your tests**:
   ```bash
   pytest tests/test_web_server.py --hosts=ssh://cadet@localhost:2242 \
     --ssh-identity-file=../../.ssh/cadet_key \
     --ssh-config=../../.ssh/testinfra_ssh_config \
     --sudo -v
   ```

5. **Expected result**: Basic tests pass. Security tests **fail** — that's correct. The failing tests prove the bugs exist. You are not fixing the role. You are proving the bugs are there.

> **STOP YOUR TIMER**

| Time | Rating |
|------|--------|
| Under 30 min | Sharpshooter |
| 30–40 min | Marksman |
| 40–50 min | Qualified |
| 50–60 min | Basic |
| 60+ min | Weapon Returned — retry |

---

## Phase 3: Main Mission — Test Everything

**Location**: `workspace/main-mission/`

```bash
cd workspace/main-mission
```

Write a complete test suite for the `fleet_hardening` role from Mission 1.5. You set up everything yourself.

### Step 1: Bring Your Role

Copy your `fleet_hardening` role from Mission 1.5 (or recreate it):

```bash
mkdir -p roles
# Either copy from your 1.5 workspace:
cp -r /path/to/mission-1-5/workspace/roles/fleet_hardening roles/
# Or recreate:
ansible-galaxy init roles/fleet_hardening
```

### Step 2: Create Inventory

Create `inventory/hosts.yml` and `inventory/group_vars/` for the fleet. Same pattern as previous missions — three nodes, two OS families.

| Node | OS | Port |
|------|----|------|
| sdc-web | Ubuntu 22.04 | 2221 |
| sdc-db | Rocky Linux 9 | 2222 |
| sdc-comms | Ubuntu 22.04 | 2223 |

### Step 3: Create ansible.cfg and site.yml

You know the pattern. `ansible.cfg` for connection settings, `site.yml` calling your role.

### Step 4: Create Molecule Configuration

```bash
mkdir -p molecule/default
```

Write `molecule/default/molecule.yml` using the anatomy from Phase 1. Use `managed: false` for all three fleet nodes.

### Step 5: Write Tests

Create `tests/test_fleet_hardening.py` with **at least 8 test functions** covering:

- SSH root login disabled
- SSH password auth disabled
- SSH service running
- Firewall active (both OS families)
- MOTD deployed with expected content
- Telnet removed from Debian nodes
- Any other hardening your role performs

### Step 6: Apply and Verify

```bash
# Apply the role
ansible-playbook -i inventory/hosts.yml site.yml

# Run your tests against all fleet nodes
pytest tests/ \
  --hosts=ssh://cadet@localhost:2221,ssh://cadet@localhost:2222,ssh://cadet@localhost:2223 \
  --ssh-identity-file=../.ssh/cadet_key \
  --ssh-config=../.ssh/testinfra_ssh_config \
  --sudo -v
```

All tests should pass.

### Step 7: Verify with ARIA

```bash
cd ../..   # Back to mission root
make test
```

All 3 phases must pass.

---

*SDC Cyber Command — 2187 — LIEUTENANT JG EYES ONLY*
