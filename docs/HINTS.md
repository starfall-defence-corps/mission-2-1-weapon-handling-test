# Mission 2.1: Weapon Handling Test — Troubleshooting

**Rank**: Lieutenant JG — minimal hints.

---

## pytest-testinfra Connection

**"Connection refused" or "Permission denied"**: Ensure containers are running (`docker ps`). Check the SSH key path in your pytest command.

**Correct invocation**:
```bash
pytest tests/ --hosts=ssh://cadet@localhost:PORT \
  --ssh-identity-file=PATH_TO_KEY \
  --ssh-config=/dev/null -v
```

The `--ssh-config=/dev/null` prevents your local SSH config from interfering.

---

## Obstacle Course Mission 1

**Test names are your specification.** `test_ssh_root_login_disabled` means the test checks `PermitRootLogin no`. Read each test function — the assert statements tell you exactly what state is expected.

**Running from the right directory matters.** `cd` into `obstacle-course/mission-1/` before running ansible-playbook or pytest.

---

## Obstacle Course Mission 2

**You are not fixing the role.** You are writing tests that DETECT the bugs. Some of your tests should fail — that's the point. The failing tests prove the bugs exist.

**Look at the template.** The bugs are in the nginx configuration template, not in the tasks.

---

## Main Mission

**molecule.yml for pre-existing containers**: Use `managed: false` for platforms that are already running (like the fleet).

```yaml
driver:
  name: default
platforms:
  - name: sdc-web
    managed: false
    groups:
      - fleet
      - debian
```

---

*SDC Cyber Command — 2187*
