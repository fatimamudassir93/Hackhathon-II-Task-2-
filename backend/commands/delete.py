from services.store import TaskStore
from ui.renderer import ConsoleRenderer


def handle_delete(store: TaskStore, task_id: int) -> str:
    """Handle delete command."""
    try:
        task = store.get(task_id)
        store.delete(task_id)
        renderer = ConsoleRenderer()
        return f"Task {task_id} '{task.title}' deleted."
    except KeyError as e:
        renderer = ConsoleRenderer()
        return renderer._color(f"Error: {e}", renderer.RED)