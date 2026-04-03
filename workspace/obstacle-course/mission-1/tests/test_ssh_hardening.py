"""
WHT Range — Mission 1: Given Tests
===================================
These 5 tests define the expected state of a hardened SSH target.
Your job: write the Ansible role that makes ALL of these pass.

Target: wht-ssh (Ubuntu 22.04, port 2241)

Run with:
  cd obstacle-course/mission-1
  ansible-playbook -i inventory.yml site.yml
  pytest tests/ --hosts=ssh://cadet@localhost:2241 \
    --ssh-identity-file=../../.ssh/cadet_key \
    --ssh-config=../../.ssh/testinfra_ssh_config \
    --sudo -v
"""


def test_ssh_root_login_disabled(host):
    """SSH must not allow root login"""
    sshd = host.file("/etc/ssh/sshd_config")
    assert sshd.exists
    assert sshd.contains("PermitRootLogin no")


def test_ssh_password_auth_disabled(host):
    """SSH must not allow password authentication"""
    sshd = host.file("/etc/ssh/sshd_config")
    assert sshd.contains("PasswordAuthentication no")


def test_ssh_service_running(host):
    """SSH service must be running and enabled"""
    ssh = host.service("ssh")
    assert ssh.is_running
    assert ssh.is_enabled


def test_telnet_not_installed(host):
    """Telnet must be removed — insecure protocol"""
    telnet = host.package("telnet")
    assert not telnet.is_installed


def test_firewall_active(host):
    """UFW firewall must be active"""
    result = host.run("ufw status")
    assert "Status: active" in result.stdout
