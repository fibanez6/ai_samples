from rich.live import Live
from rich.spinner import Spinner

async def wait_for_response(awaitable_task, spinner_text="Waiting for the response..."):
    spinner = Spinner("dots", text=spinner_text)
    with Live(spinner, refresh_per_second=10):
        return await awaitable_task


