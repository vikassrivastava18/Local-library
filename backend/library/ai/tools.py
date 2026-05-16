from langchain_core.tools import tool


@tool
def current_day() -> str:
    """Returns current day of the week"""
    from datetime import datetime
    return datetime.now().strftime("%A")


@tool
def current_time() -> str:
    """Returns current time in hour: minutes"""
    from datetime import datetime
    return datetime.now().strftime("%H:%M")
