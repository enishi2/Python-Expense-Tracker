import json
from datetime import datetime
from models import Expense, Category


def expense_to_dict(expense: Expense) -> dict:
    return {
        "id": expense.id,
        "amount": expense.amount,
        "category": expense.category.value,
        "description": expense.description,
        "date": expense.date.isoformat()
    }

def dict_to_expense(data: dict) -> Expense:
    categoria_str = data["category"]
    categoria_enum = None
    for c in Category:
        if c.value == categoria_str:
            categoria_enum = c
            break
    if categoria_enum is None:
        categoria_enum = Category.OTHER  # fallback
    return Expense(
        id=data["id"],
        amount=data["amount"],
        category=categoria_enum,
        description=data["description"],
        date=datetime.fromisoformat(data["date"])
    )

def save_expenses(expenses: list[Expense]):
    data = [expense_to_dict(e) for e in expenses]

    with open("expenses.json", "w") as f:
        json.dump(data, f, indent=4)

def load_expenses() -> list[Expense]:
    try:
        with open("expenses.json", "r") as f:
            data = json.load(f)
            return [dict_to_expense(item) for item in data]
    except FileNotFoundError:
        return []

if __name__ == "__main__":
    from datetime import datetime

    e1 = Expense(1, 20, Category.FOOD, "pizza", datetime.now())
    e2 = Expense(2, 8, Category.TRANSPORT, "bus", datetime.now())

    save_expenses([e1, e2])

    gastos = load_expenses()
    print(gastos)