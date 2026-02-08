from services.store import TaskStore
from ui.renderer import ConsoleRenderer
from services.validator import validate_description


def handle_add(store: TaskStore, title: str, description: str) -> str:
    """Handle add command."""
    try:
        task = store.add(title, description)
        renderer = ConsoleRenderer()
        output = f"Task {task.id} added: {task.title}"
        output += f"\n{renderer.render_frame(store.get_all())}"
        return output
    except ValueError as e:
        renderer = ConsoleRenderer()
        return renderer._color(f"Error: {e}", renderer.RED)