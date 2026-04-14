from rich.console import Console
from rich.markdown import Markdown

def show_help(topic: str):
    from BusinessLogic.docs_helper import get_document
    content = get_document(f"{topic.lower()}.md")
    if content is None:
        Console().print(f"[red]No help available for '{topic}'.[/red]")
        return
    Console().print(Markdown(content))