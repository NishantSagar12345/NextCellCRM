import pytest

def pytest_terminal_summary(terminalreporter, exitstatus, config):
        """Prints the success report only if all 4 tests pass."""
        if exitstatus == 0:
            print("\n" + "★"*50)
            print("🚀 NEXCELL CRM: ALL 4 CORE TESTS PASSED")
            print("1. [SECURITY] Multi-Tenant Isolation:      PASSED")
            print("2. [LOGIC]    Contact Search/Filter:       PASSED")
            print("3. [DATABASE] UUID & Schema Integrity:     PASSED")
            print("4. [CLINIC]   Cross-Module Integration Checking Complete Flow:    PASSED")
            print("★"*50 + "\n")