# Main Mission: Test Everything

Write a complete Molecule test scenario for the `fleet_hardening` role from Mission 1.5.

## What You Need to Create

```
main-mission/
  inventory/
    hosts.yml              # Fleet inventory (same as 1.5)
    group_vars/
      all.yml
      debian.yml
      redhat.yml
  roles/
    fleet_hardening/       # Your role from 1.5 (copy or recreate)
  molecule/
    default/
      molecule.yml         # Molecule configuration
  tests/
    test_fleet_hardening.py  # Your Testinfra tests
  site.yml                 # Playbook calling the role
```

## Your Tests Must Cover

1. SSH hardened on all nodes (PermitRootLogin, PasswordAuthentication)
2. SSH service running on all nodes
3. Firewall active (ufw on Debian, firewalld on RedHat)
4. MOTD deployed with "STARFALL" content
5. Telnet removed from Debian nodes
6. At least 8 test functions total

## How to Run

```bash
cd main-mission
ansible-playbook -i inventory/hosts.yml site.yml
pytest tests/test_fleet_hardening.py \
  --hosts=ssh://cadet@localhost:2221,ssh://cadet@localhost:2222,ssh://cadet@localhost:2223 \
  --ssh-identity-file=../.ssh/cadet_key \
  --ssh-config=/dev/null -v
```

## Fleet Nodes

| Node | OS | Port |
|------|----|------|
| sdc-web | Ubuntu 22.04 | 2221 |
| sdc-db | Rocky Linux 9 | 2222 |
| sdc-comms | Ubuntu 22.04 | 2223 |
