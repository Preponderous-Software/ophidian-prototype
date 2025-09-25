#!/usr/bin/env python3
"""
Test runner script for the Ophidian menu system
"""
import sys
import subprocess
import os


def run_tests():
    """Run all menu-related tests"""
    # Set environment variables for headless testing
    env = os.environ.copy()
    env['SDL_AUDIODRIVER'] = 'dummy'
    env['DISPLAY'] = ':99'
    
    print("Running Ophidian Menu System Tests")
    print("=" * 50)
    
    # List of test modules to run
    test_modules = [
        'tests.state.test_menu_state',
        'tests.graphics.test_main_menu',
        'tests.graphics.test_options_menu',
        'tests.graphics.test_high_scores_menu',
        'tests.test_ophidian_menu_integration'
    ]
    
    total_tests = 0
    failed_tests = 0
    
    for module in test_modules:
        print(f"\nRunning {module}...")
        try:
            result = subprocess.run([
                'xvfb-run', '-a', 'python', '-m', 'unittest', module, '-v'
            ], env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ {module} - PASSED")
                # Count tests from output
                lines = result.stderr.split('\n')
                for line in lines:
                    if 'Ran' in line and 'test' in line:
                        count = int(line.split()[1])
                        total_tests += count
                        break
            else:
                print(f"✗ {module} - FAILED")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                failed_tests += 1
                
        except Exception as e:
            print(f"✗ {module} - ERROR: {e}")
            failed_tests += 1
    
    print("\n" + "=" * 50)
    print(f"Test Summary:")
    print(f"Total tests run: {total_tests}")
    print(f"Modules failed: {failed_tests}")
    
    if failed_tests == 0:
        print("✓ All tests passed!")
        return True
    else:
        print("✗ Some tests failed!")
        return False


def main():
    """Main entry point"""
    if not run_tests():
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()