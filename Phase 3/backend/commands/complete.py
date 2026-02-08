from services.store import TaskStore
from ui.renderer import ConsoleRenderer


def handle_complete(store: TaskStore, task_id: int) -> str:
    """Handle complete command."""
    try:
        task = store.toggle_status(task_id)
        renderer = ConsoleRenderer()
        return renderer.render_single(task)
    except KeyError as e:
        renderer = ConsoleRenderer()
        return renderer._color(f"Error: {e}", renderer.RED)