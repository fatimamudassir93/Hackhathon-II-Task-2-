from services.store import TaskStore
from ui.renderer import ConsoleRenderer


def handle_complete(store: TaskStore, task_id: int) -> str:
    """Handle complete/toggle command."""
    try:
        task = store.toggle_status(task_id)
        renderer = ConsoleRenderer()
        status_text = "completed" if task.status.value == "completed" else "incomplete"
        output = f"Task {task_id} marked as {status_text}: {task.title}"
        output += f"\n{renderer.render_frame(store.get_all())}"
        return output
    except (ValueError, KeyError) as e:
        renderer = ConsoleRenderer()
        return renderer._color(f"Error: {e}", renderer.RED)
