#!/usr/bin/env python3
"""Test script to demonstrate all todo app functionality."""

import sys
sys.path.insert(0, 'src')

from services.store import TaskStore
from commands.add import handle_add
from commands.complete import handle_complete
from commands.delete import handle_delete
from commands.update import handle_update
from commands.view import handle_view
from models.task import TaskStatus

def main():
    """Run comprehensive test of all commands."""
    store = TaskStore()

    print("=" * 80)
    print("IN-MEMORY PYTHON CONSOLE TODO APP - TEST DEMONSTRATION")
    print("=" * 80)
    print()

    # Test 1: Add tasks
    print("TEST 1: Adding tasks...")
    print(handle_add(store, "Buy groceries", "Get milk, eggs, and bread from the store"))
    print()

    print(handle_add(store, "Finish report", "Complete Q4 financial report and send to manager"))
    print()

    print(handle_add(store, "Email client", "Send project update to client with timeline"))
    print()

    # Test 2: View all tasks
    print("\nTEST 2: Viewing all tasks...")
    print(handle_view(store))
    print()

    # Test 3: Complete a task
    print("\nTEST 3: Completing task 2...")
    print(handle_complete(store, 2))
    print()

    # Test 4: View only pending tasks
    print("\nTEST 4: Viewing only pending tasks...")
    print(handle_view(store, TaskStatus.PENDING))
    print()

    # Test 5: View only completed tasks
    print("\nTEST 5: Viewing only completed tasks...")
    print(handle_view(store, TaskStatus.COMPLETED))
    print()

    # Test 6: Update a task
    print("\nTEST 6: Updating task 1...")
    print(handle_update(store, 1, title="Buy groceries and snacks", description="Get milk, eggs, bread, and healthy snacks"))
    print()

    # Test 7: Delete a task
    print("\nTEST 7: Deleting task 3...")
    print(handle_delete(store, 3))
    print()

    # Test 8: View final state
    print("\nTEST 8: Final view of all tasks...")
    print(handle_view(store))
    print()

    # Test 9: Error handling - invalid task ID
    print("\nTEST 9: Error handling - trying to complete non-existent task...")
    try:
        print(handle_complete(store, 999))
    except:
        print("Error displayed correctly")
    print()

    # Test 10: Error handling - empty title
    print("\nTEST 10: Error handling - trying to add task with empty title...")
    print(handle_add(store, "", "This should fail"))
    print()

    # Test 11: Test toggle - mark completed task back to pending
    print("\nTEST 11: Toggle task 2 back to pending...")
    print(handle_complete(store, 2))
    print()

    print("=" * 80)
    print("ALL TESTS COMPLETED!")
    print("=" * 80)

if __name__ == "__main__":
    main()
