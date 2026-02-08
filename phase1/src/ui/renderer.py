import sys
from typing import List
from models.task import Task, TaskStatus


class ConsoleRenderer:
    """Console rendering with ANSI color and framing.

    FR-011: ANSI color codes with graceful fallback.
    FR-002: Framed task list display.
    FR-017: Handle text overflow (word-wrap within frame).
    """

    # ANSI color codes
    RESET = "\033[0m"
    DIM_GRAY = "\033[90m"
    BRIGHT_WHITE = "\033[97m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    RED = "\033[91m"

    def __init__(self, use_color: bool = None):
        """Initialize renderer.

        Args:
            use_color: Force color on/off. Auto-detects if None.
        """
        if use_color is None:
            self.use_color = sys.stdout.isatty()
        else:
            self.use_color = use_color

        # Check if terminal supports Unicode
        try:
            sys.stdout.encoding.encode('─')
            self.use_unicode = True
        except:
            self.use_unicode = False

    def _color(self, text: str, color_code: str) -> str:
        """Apply color if enabled, otherwise return plain text."""
        if self.use_color:
            return f"{color_code}{text}{self.RESET}"
        return text

    def _format_task_line(self, task: Task) -> List[str]:
        """Format task line with status marker, ID, title and description.

        Returns a list of lines for multi-line task display.
        """
        if task.status == TaskStatus.COMPLETED:
            # Completed tasks: Green checkmark
            if self.use_unicode:
                status_marker = self._color("✓", self.GREEN) + self._color(" DONE ", "\033[42m\033[30m")  # Green background
            else:
                status_marker = self._color("[DONE]", self.GREEN)
            title_color = "\033[32m"  # Green for completed
        else:
            # Pending tasks: Yellow pending indicator
            if self.use_unicode:
                status_marker = self._color("○", self.YELLOW) + self._color(" TODO ", "\033[43m\033[30m")  # Yellow background
            else:
                status_marker = self._color("[TODO]", self.YELLOW)
            title_color = self.BRIGHT_WHITE  # White for pending

        id_str = self._color(f"{task.id:3}", self.CYAN)
        title_line = f"{status_marker} {id_str}: {self._color(task.title, title_color)}"
        desc_line = f"         {self._color(task.description, '\033[90m')}"  # Gray for description
        return [title_line, desc_line]

    def render_frame(self, tasks: List[Task], title: str = "TODO LIST") -> str:
        """Render framed task list with colorful output.

        FR-002: Display all tasks in framed, organized console output.
        FR-017: Handle text overflow (word-wrap within frame).
        """
        width = 76  # 80 columns minus 4 for borders and padding

        # Use ASCII or Unicode box drawing characters
        if self.use_unicode:
            border_h = "═" * width
            tl, tr, bl, br = "╔", "╗", "╚", "╝"
            ml, mr = "╠", "╣"
            v = "║"
        else:
            border_h = "=" * width
            tl, tr, bl, br = "+", "+", "+", "+"
            ml, mr = "+", "+"
            v = "|"

        # Colorful header
        lines = [
            self._color(f"{tl}{border_h}{tr}", self.CYAN),
            self._color(f"{v}{title.center(width)}{v}", "\033[1m\033[96m"),  # Bold cyan
            self._color(f"{ml}{border_h}{mr}", self.CYAN),
        ]

        if not tasks:
            empty_msg = "No tasks yet! Add your first task to get started."
            lines.append(self._color(f"{v}{empty_msg.center(width)}{v}", self.YELLOW))
        else:
            for task in tasks:
                task_lines = self._format_task_line(task)
                for task_line in task_lines:
                    # Calculate visible length (excluding ANSI codes)
                    visible_len = len(task_line)
                    # Count all ANSI escape sequences
                    import re
                    ansi_pattern = re.compile(r'\033\[[0-9;]+m')
                    ansi_codes = ansi_pattern.findall(task_line)
                    for code in ansi_codes:
                        visible_len -= len(code)

                    if visible_len > width:
                        # Truncate if too long
                        task_line = task_line[:width - 3] + "..."
                        visible_len = width
                    # Pad to frame width
                    task_line = task_line + " " * (width - visible_len)
                    lines.append(self._color(f"{v}", self.CYAN) + task_line + self._color(f"{v}", self.CYAN))

        lines.append(self._color(f"{bl}{border_h}{br}", self.CYAN))

        # Colorful footer with summary
        pending = sum(1 for t in tasks if t.status == TaskStatus.PENDING)
        completed = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)

        pending_str = self._color(f"{pending} pending", self.YELLOW)
        completed_str = self._color(f"{completed} completed", self.GREEN)
        total_str = self._color(f"{len(tasks)} tasks total", self.CYAN)

        summary = f"[Stats] {total_str} ({pending_str}, {completed_str})"
        lines.append(summary.center(80 + 40))  # Extra space for ANSI codes

        return "\n".join(lines)
