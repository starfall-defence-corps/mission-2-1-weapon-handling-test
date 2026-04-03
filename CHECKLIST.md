# Mission 2.1: Weapon Handling Test — Progress Tracker

**Rank**: Lieutenant JG

---

## WHT Range — Obstacle Course

**Start Time**: _______________
**End Time**: _______________

### Mission 1: Write the Role
- [ ] Read all 5 tests in `tests/test_ssh_hardening.py`
- [ ] Created `roles/ssh_hardening/` with tasks
- [ ] Applied role to wht-ssh
- [ ] All 5 tests pass

### Mission 2: Write the Tests
- [ ] Read the `web_server` role and templates
- [ ] Applied role to wht-web
- [ ] Created `tests/test_web_server.py`
- [ ] Basic tests pass (package, service, socket)
- [ ] Security tests fail (catching the bugs)

### Performance Tier
| Time | Rating |
|------|--------|
| Under 30 min | Sharpshooter |
| 30–40 min | Marksman |
| 40–50 min | Qualified |
| 50–60 min | Basic |
| 60+ min | Weapon Returned |

**My Rating**: _______________

---

## Main Mission: Test Everything

- [ ] Copied fleet_hardening role to `main-mission/roles/`
- [ ] Created inventory with fleet nodes
- [ ] Created `site.yml`
- [ ] Created `molecule/default/molecule.yml`
- [ ] Created `tests/test_fleet_hardening.py` with 8+ tests
- [ ] Tests cover SSH, firewall, MOTD, services
- [ ] Role applied successfully
- [ ] All tests pass
- [ ] `make test` — all ARIA checks pass
