from services.store import TaskStore
from ui.renderer import ConsoleRenderer
from services.validator import validate_task_id


def handle_update(store: TaskStore, task_id: int, title: str = None, description: str = None) -> str:
    """Handle update command."""
    try:
        task = store.update(task_id, title=title, description=description)
        renderer = ConsoleRenderer()
        output = f"Task {task_id} updated successfully"
        output += f"\n{renderer.render_frame(store.get_all())}"
        return output
    except (ValueError, KeyError) as e:
        renderer = ConsoleRenderer()
        return renderer._color(f"Error: {e}", renderer.RED)
