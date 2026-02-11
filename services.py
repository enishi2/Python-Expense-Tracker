from models import Expense, Category
from database import load_expenses, save_expenses
from datetime import datetime

def get_all_expenses() -> list[Expense]:
    """Retorna todos os gastos salvos"""
    return load_expenses()

def add_expense(amount: float, category: Category, description: str, date: datetime = None):
    """Adiciona um novo gasto"""
    expenses = load_expenses()
    if date is None:
        date = datetime.now()

    # cria um ID simples: último ID + 1
    if expenses:
        new_id = max(e.id for e in expenses) + 1
    else:
        new_id = 1

    new_expense = Expense(new_id, amount, category, description, date)
    expenses.append(new_expense)
    save_expenses(expenses)

def remove_expense(expense_id: int) -> bool:
    """Remove gasto pelo ID. Retorna True se removido, False se não existir"""
    expenses = load_expenses()
    for e in expenses:
        if e.id == expense_id:
            expenses.remove(e)
            save_expenses(expenses)
            return True
    return False

def total_month(year: int, month: int) -> float:
    """Calcula o total de gastos de um mês"""
    expenses = load_expenses()
    total = sum(e.amount for e in expenses if e.date.year == year and e.date.month == month)
    return total

def filter_by_category(category: Category) -> list[Expense]:
    """Retorna lista de gastos de uma categoria"""
    expenses = load_expenses()
    return [e for e in expenses if e.category == category]

def search_expenses(keyword: str = "", category: Category = None):
    """
    Retorna lista de despesas que correspondem à keyword na descrição e/ou à categoria.
    Se não passar nenhum parâmetro, retorna todos.
    """
    results = get_all_expenses()
    if keyword:
        results = [e for e in results if keyword.lower() in e.description.lower()]
    if category:
        results = [e for e in results if e.category == category]
    return results





if __name__ == "__main__":
    from datetime import datetime

    add_expense(15, Category.FOOD, "Almoço")
    add_expense(7, Category.TRANSPORT, "Ônibus")

    print("Todos os gastos:")
    for g in get_all_expenses():
        print(g)

    print("\nTotal deste mês:", total_month(2026, 2))