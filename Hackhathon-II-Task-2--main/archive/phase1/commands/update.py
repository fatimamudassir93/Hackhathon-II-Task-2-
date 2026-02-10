from services.store import TaskStore
from ui.renderer import ConsoleRenderer


def handle_update(store: TaskStore, task_id: int, title: str = None, description: str = None) -> str:
    """Handle update command."""
    try:
        task = store.update(task_id, title=title, description=description)
        renderer = ConsoleRenderer()
        return renderer.render_single(task)
    except (ValueError, KeyError) as e:
        renderer = ConsoleRenderer()
        return renderer._color(f"Error: {e}", renderer.RED)