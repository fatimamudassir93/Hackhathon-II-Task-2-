#!/usr/bin/env python3
"""Test script to demonstrate interactive TODO app with simulated inputs."""

import sys
from io import StringIO

# Simulate user inputs with Enter presses
simulated_input = """

1

Buy Groceries
Get milk, eggs, and bread from the store

2

1

Finish Report
Complete Q4 financial report

2

5

1

2

6

1

7
"""

# Save original stdin
original_stdin = sys.stdin

# Replace stdin with simulated input
sys.stdin = StringIO(simulated_input)

# Add src to path
sys.path.insert(0, 'src')

# Import and run the app
from app import main

try:
    main()
except Exception as e:
    print(f"\nError during test: {e}")
    import traceback
    traceback.print_exc()
finally:
    # Restore original stdin
    sys.stdin = original_stdin

print("\n" + "=" * 60)
print("INTERACTIVE TEST COMPLETED!")
print("=" * 60)
