from services.store import TaskStore
from models.task import TaskStatus
from ui.renderer import ConsoleRenderer


def handle_view(store: TaskStore, status_filter: TaskStatus = None) -> str:
    """Handle view command with optional status filter."""
    renderer = ConsoleRenderer()
    if status_filter:
        tasks = store.get_by_status(status_filter)
    else:
        tasks = store.get_all()
    return renderer.render_frame(tasks)
