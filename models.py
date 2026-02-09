from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Category(Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    LEISURE = "Leisure"
    BILLS = "Bills"
    OTHER = "Other"


@dataclass
class Expense:
    id: int
    amount: float
    category: Category
    description: str
    date: datetime

    def __str__(self):
        return f"[{self.id}] {self.description} | {self.category.value} | €{self.amount:.2f} | {self.date.strftime('%d/%m/%Y %H:%M')}"


if __name__ == "__main__":
    e = Expense(1, 12.5, Category.FOOD, "almoco", datetime.now())
    print(e)