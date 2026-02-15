"""
Utility Functions
"""
def format_currency(amount: float) -> str:
    return f"${amount:,.2f}"

def calculate_percentage_change(old: float, new: float) -> float:
    if old == 0:
        return 0
    return ((new - old) / old) * 100
