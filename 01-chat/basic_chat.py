
from rich.markdown import Markdown
from rich.panel import Panel
from ..utils.agent import Agent

agent = Agent()

print(
    Panel(
        Markdown(f"Agent Client {agent.name} using model: **{agent.model}**"),
        title="Basic Chat Completion",
        border_style="bold green",
        padding=(1, 2),
    )
)

response = agent.client.chat.completions.create(
    model=agent.model,
    temperature=0.7,
    messages=[
        {"role": "system", "content": "Eres un asistente útil que hace muchas referencias a gatos y usa emojis."},
        {"role": "user", "content": "Escribe un haiku sobre un gato hambriento que quiere atún"},
    ],
)

print(response.choices[0].message)