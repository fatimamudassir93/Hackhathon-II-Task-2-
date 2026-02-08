from services.store import TaskStore
from ui.renderer import ConsoleRenderer
from services.validator import validate_task_id


def handle_delete(store: TaskStore, task_id: int) -> str:
    """Handle delete command."""
    try:
        task = store.get(task_id)
        store.delete(task_id)
        renderer = ConsoleRenderer()
        output = f"Task {task_id} deleted: {task.description}"
        output += f"\n{renderer.render_frame(store.get_all())}"
        return output
    except KeyError as e:
        renderer = ConsoleRenderer()
        return renderer._color(f"Error: {e}", renderer.RED)
