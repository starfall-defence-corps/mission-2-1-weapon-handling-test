# WHT Range — Mission 2: Write the Tests

Create `test_web_server.py` in this directory.

Your tests should verify:
1. nginx package is installed
2. nginx service is running and enabled
3. Configuration file exists at `/etc/nginx/sites-available/default`
4. Port 80 is listening
5. **Find and test for the security bugs in the role**

Run your tests with:
```bash
cd obstacle-course/mission-2
ansible-playbook -i inventory.yml site.yml
pytest tests/test_web_server.py --hosts=ssh://cadet@localhost:2242 \
  --ssh-identity-file=../../.ssh/cadet_key \
  --ssh-config=../../.ssh/testinfra_ssh_config --sudo -v
```

Useful Testinfra helpers:
- `host.package("nginx")` — `.is_installed`
- `host.service("nginx")` — `.is_running`, `.is_enabled`
- `host.socket("tcp://0.0.0.0:80")` — `.is_listening`
- `host.file("/path")` — `.exists`, `.contains("text")`, `.mode`
- `host.run("command")` — `.stdout`, `.rc`
