"""
ARIA Custom Test Reporter
Provides color-coded, phase-grouped output for WHT verification.
"""
import os
import pytest
import sys

PHASES = {
    "TestObstacleCourse1":   ("1", "WHT Range — Mission 1 (Write the Role)"),
    "TestObstacleCourse2":   ("2", "WHT Range — Mission 2 (Write the Tests)"),
    "TestMainMission":       ("3", "Main Mission — Test Everything"),
}

FRIENDLY = {
    "test_oc1_role_exists":                "Role ssh_hardening exists",
    "test_oc1_tasks_have_content":         "tasks/main.yml has tasks",
    "test_oc1_role_applied_successfully":  "Role applied to wht-ssh",
    "test_oc1_tests_pass":                 "All 5 pre-written tests pass",
    "test_oc2_test_file_exists":           "test_web_server.py exists",
    "test_oc2_tests_have_assertions":      "Tests have meaningful assertions",
    "test_oc2_role_applied":               "Web server role applied to wht-web",
    "test_oc2_tests_catch_bug":            "Tests detect at least one security bug",
    "test_mm_molecule_config_exists":      "molecule.yml exists",
    "test_mm_test_file_exists":            "Test file exists with assertions",
    "test_mm_role_exists":                 "fleet_hardening role exists",
    "test_mm_site_yml_exists":             "site.yml references role",
    "test_mm_test_coverage":               "Tests cover at least 8 checks",
    "test_mm_tests_pass":                  "Tests pass against fleet",
}

# The phase-oriented summary is rendered by the shared `aria-reporter`
# pytest plugin (installed via requirements.txt); this file only declares
# the mission's phases + friendly objective names.
from aria_reporter import configure  # noqa: E402

configure(phases=PHASES, friendly=FRIENDLY, mission_id="2-1")
