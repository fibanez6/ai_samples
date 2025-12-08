from rich.live import Live
from rich.spinner import Spinner


async def wait_for_response(awaitable_task, spinner_text="Waiting for the response..."):
    """
    Wait for an async task to complete while displaying a spinner.
    
    Args:
        awaitable_task: An awaitable object (coroutine, task, or future) to wait for.
        spinner_text (str, optional): Text to display next to the spinner. 
            Defaults to "Waiting for the response...".
    
    Returns:
        The result of the awaitable_task once it completes.
    """
    spinner = Spinner("dots", text=spinner_text)
    with Live(spinner, refresh_per_second=10):
        return await awaitable_task


