import sys
from services.store import TaskStore
from models.task import TaskStatus
from ui.renderer import ConsoleRenderer
from commands.add import handle_add
from commands.complete import handle_complete
from commands.delete import handle_delete
from commands.update import handle_update
from commands.view import handle_view


class Colors:
    """ANSI color codes for colorful UI."""
    RESET = "\033[0m"
    BOLD = "\033[1m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[101m"
    BG_GREEN = "\033[102m"
    BG_YELLOW = "\033[103m"
    BG_BLUE = "\033[104m"
    BG_MAGENTA = "\033[105m"
    BG_CYAN = "\033[106m"
    BG_WHITE = "\033[107m"


def print_banner():
    """Display colorful welcome banner."""
    # Check if terminal supports Unicode
    try:
        sys.stdout.encoding.encode('═')
        use_unicode = True
    except:
        use_unicode = False

    if use_unicode:
        banner = f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              WELCOME TO TODO APPLICATION                     ║
║                                                              ║
║            {Colors.WHITE}Organize Your Tasks Efficiently!{Colors.CYAN}              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    else:
        banner = f"""
{Colors.CYAN}{Colors.BOLD}================================================================
||                                                            ||
||              WELCOME TO TODO APPLICATION                   ||
||                                                            ||
||            {Colors.WHITE}Organize Your Tasks Efficiently!{Colors.CYAN}              ||
||                                                            ||
================================================================{Colors.RESET}
"""
    print(banner)


def display_menu():
    """Display the colorful main menu."""
    # Check if terminal supports Unicode
    try:
        sys.stdout.encoding.encode('─')
        use_unicode = True
    except:
        use_unicode = False

    if use_unicode:
        menu = f"""
{Colors.MAGENTA}{Colors.BOLD}┌──────────────────────────────────────────────────────────────┐
│                     TODO APPLICATION                         │
└──────────────────────────────────────────────────────────────┘{Colors.RESET}

{Colors.GREEN}{Colors.BOLD}+  1.{Colors.RESET} {Colors.WHITE}Add Task{Colors.RESET}
{Colors.CYAN}{Colors.BOLD}*  2.{Colors.RESET} {Colors.WHITE}View All Tasks{Colors.RESET}
{Colors.YELLOW}{Colors.BOLD}~  3.{Colors.RESET} {Colors.WHITE}Update Task{Colors.RESET}
{Colors.RED}{Colors.BOLD}X  4.{Colors.RESET} {Colors.WHITE}Delete Task{Colors.RESET}
{Colors.GREEN}{Colors.BOLD}V  5.{Colors.RESET} {Colors.WHITE}Mark Task Complete{Colors.RESET}
{Colors.YELLOW}{Colors.BOLD}O  6.{Colors.RESET} {Colors.WHITE}Mark Task Incomplete{Colors.RESET}
{Colors.RED}{Colors.BOLD}>  7.{Colors.RESET} {Colors.WHITE}Exit{Colors.RESET}

{Colors.MAGENTA}{'─' * 62}{Colors.RESET}
"""
    else:
        menu = f"""
{Colors.MAGENTA}{Colors.BOLD}----------------------------------------------------------------
                     TODO APPLICATION
----------------------------------------------------------------{Colors.RESET}

{Colors.GREEN}{Colors.BOLD}+  1.{Colors.RESET} {Colors.WHITE}Add Task{Colors.RESET}
{Colors.CYAN}{Colors.BOLD}*  2.{Colors.RESET} {Colors.WHITE}View All Tasks{Colors.RESET}
{Colors.YELLOW}{Colors.BOLD}~  3.{Colors.RESET} {Colors.WHITE}Update Task{Colors.RESET}
{Colors.RED}{Colors.BOLD}X  4.{Colors.RESET} {Colors.WHITE}Delete Task{Colors.RESET}
{Colors.GREEN}{Colors.BOLD}V  5.{Colors.RESET} {Colors.WHITE}Mark Task Complete{Colors.RESET}
{Colors.YELLOW}{Colors.BOLD}O  6.{Colors.RESET} {Colors.WHITE}Mark Task Incomplete{Colors.RESET}
{Colors.RED}{Colors.BOLD}>  7.{Colors.RESET} {Colors.WHITE}Exit{Colors.RESET}

{Colors.MAGENTA}{'-' * 62}{Colors.RESET}
"""
    print(menu)


def main():
    """Interactive menu-driven TODO application."""
    store = TaskStore()

    print_banner()
    input(f"{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    while True:
        display_menu()
        choice = input(f"{Colors.CYAN}{Colors.BOLD}> Enter your choice (1-7): {Colors.RESET}").strip()

        if choice == "1":
            # Add Task
            print(f"\n{Colors.GREEN}{Colors.BOLD}{'-' * 60}")
            print(f"+  ADD NEW TASK")
            print(f"{'-' * 60}{Colors.RESET}\n")
            title = input(f"{Colors.YELLOW}>  Enter task title: {Colors.RESET}").strip()
            description = input(f"{Colors.YELLOW}>  Enter task description: {Colors.RESET}").strip()

            if title and description:
                result = handle_add(store, title, description)
                print(f"\n{Colors.GREEN}[SUCCESS!]{Colors.RESET}")
                print(result)
            else:
                print(f"\n{Colors.RED}[ERROR] Title and description cannot be empty!{Colors.RESET}")

            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

        elif choice == "2":
            # View All Tasks
            print(f"\n{Colors.CYAN}{Colors.BOLD}{'-' * 60}")
            print(f"*  VIEW ALL TASKS")
            print(f"{'-' * 60}{Colors.RESET}\n")
            result = handle_view(store)
            print(result)
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

        elif choice == "3":
            # Update Task
            print(f"\n{Colors.YELLOW}{Colors.BOLD}{'-' * 60}")
            print(f"~  UPDATE TASK")
            print(f"{'-' * 60}{Colors.RESET}\n")
            print(handle_view(store))
            try:
                task_id = int(input(f"\n{Colors.YELLOW}Enter task ID to update: {Colors.RESET}").strip())
                title = input(f"{Colors.YELLOW}Enter new title: {Colors.RESET}").strip()
                description = input(f"{Colors.YELLOW}Enter new description: {Colors.RESET}").strip()

                if title and description:
                    result = handle_update(store, task_id, title=title, description=description)
                    print(f"\n{Colors.GREEN}[Task updated successfully!]{Colors.RESET}")
                    print(result)
                else:
                    print(f"\n{Colors.RED}[ERROR] Title and description cannot be empty!{Colors.RESET}")
            except ValueError:
                print(f"{Colors.RED}[ERROR] Invalid task ID. Please enter a number.{Colors.RESET}")
            except KeyError as e:
                print(f"{Colors.RED}[ERROR] {e}{Colors.RESET}")

            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

        elif choice == "4":
            # Delete Task
            print(f"\n{Colors.RED}{Colors.BOLD}{'-' * 60}")
            print(f"X  DELETE TASK")
            print(f"{'-' * 60}{Colors.RESET}\n")
            print(handle_view(store))
            try:
                task_id = int(input(f"\n{Colors.RED}Enter task ID to delete: {Colors.RESET}").strip())
                result = handle_delete(store, task_id)
                print(f"\n{Colors.GREEN}[Task deleted successfully!]{Colors.RESET}")
                print(result)
            except ValueError:
                print(f"{Colors.RED}[ERROR] Invalid task ID. Please enter a number.{Colors.RESET}")
            except KeyError as e:
                print(f"{Colors.RED}[ERROR] {e}{Colors.RESET}")

            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

        elif choice == "5":
            # Mark Task Complete
            print(f"\n{Colors.GREEN}{Colors.BOLD}{'-' * 60}")
            print(f"V  MARK TASK COMPLETE")
            print(f"{'-' * 60}{Colors.RESET}\n")
            print(handle_view(store))
            try:
                task_id = int(input(f"\n{Colors.GREEN}Enter task ID to mark complete: {Colors.RESET}").strip())
                task = store.get(task_id)
                if task.status == TaskStatus.COMPLETED:
                    print(f"\n{Colors.YELLOW}[WARNING] Task {task_id} is already completed!{Colors.RESET}")
                else:
                    result = handle_complete(store, task_id)
                    print(f"\n{Colors.GREEN}[Task marked as COMPLETE!]{Colors.RESET}")
                    print(result)
            except (ValueError, KeyError) as e:
                print(f"{Colors.RED}[ERROR] {e}{Colors.RESET}")

            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

        elif choice == "6":
            # Mark Task Incomplete
            print(f"\n{Colors.YELLOW}{Colors.BOLD}{'-' * 60}")
            print(f"O  MARK TASK INCOMPLETE")
            print(f"{'-' * 60}{Colors.RESET}\n")
            print(handle_view(store))
            try:
                task_id = int(input(f"\n{Colors.YELLOW}Enter task ID to mark incomplete: {Colors.RESET}").strip())
                task = store.get(task_id)
                if task.status == TaskStatus.PENDING:
                    print(f"\n{Colors.YELLOW}[WARNING] Task {task_id} is already pending/incomplete!{Colors.RESET}")
                else:
                    result = handle_complete(store, task_id)
                    print(f"\n{Colors.GREEN}[Task marked as INCOMPLETE/PENDING!]{Colors.RESET}")
                    print(result)
            except (ValueError, KeyError) as e:
                print(f"{Colors.RED}[ERROR] {e}{Colors.RESET}")

            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

        elif choice == "7":
            # Exit
            print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 60}")
            print(f"{Colors.YELLOW}  Thank you for using TODO Application!{Colors.RESET}")
            print(f"{Colors.GREEN}  Have a productive day!{Colors.RESET}")
            print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 60}{Colors.RESET}\n")
            break

        else:
            print(f"\n{Colors.RED}[ERROR] Invalid choice! Please enter a number between 1 and 7.{Colors.RESET}")
            input(f"{Colors.CYAN}Press Enter to continue...{Colors.RESET}")


if __name__ == "__main__":
    main()
