from typing import ContextManager, Optional
from alive_progress import alive_bar

def spinner(title: Optional[str] = None) -> ContextManager:
    """
    Context manager to display a spinner while a long-running process is running.

    Usage:
        with spinner("Fetching data..."):
            fetch_data()

    Args:
        title: The title of the spinner. If None, no title will be displayed.
    """
    return alive_bar(monitor=None, stats=None, title=title)