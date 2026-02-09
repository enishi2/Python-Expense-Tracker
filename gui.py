import tkinter as tk
from tkinter import messagebox, simpledialog
from services import add_expense, get_all_expenses, remove_expense, total_month
from models import Category
from datetime import datetime


root = tk.Tk()
root.title("Sistema de Controle Financeiro")
root.geometry("500x400")

result_area = tk.Text(root, height=15, width=60)
result_area.pack(pady=10)


def gui_add_expense():
    try:
        valor = float(simpledialog.askstring("Valor", "Digite o valor (€):", parent=root))
        descricao = simpledialog.askstring("Descrição", "Digite a descrição:", parent=root)

        cat_input = simpledialog.askstring(
            "Categoria",
            f"Digite a categoria ({', '.join(c.value for c in Category)}):",
            parent=root
        )

        categoria = None
        for c in Category:
            if c.value.lower() == cat_input.lower():
                categoria = c
                break
        if categoria is None:
            messagebox.showerror("Erro", "Categoria inválida!", parent=root)
            return

        add_expense(valor, categoria, descricao)
        messagebox.showinfo("Sucesso", "Gasto adicionado!", parent=root)
        gui_list_expenses()
    except (ValueError, TypeError):
        messagebox.showerror("Erro", "Valor inválido!", parent=root)

def gui_list_expenses():
    gastos = get_all_expenses()
    result_area.delete(1.0, tk.END)
    if not gastos:
        result_area.insert(tk.END, "Nenhum gasto registrado.\n")
    else:
        for g in gastos:
            result_area.insert(tk.END, str(g) + "\n")

def gui_remove_expense():
    try:
        id_remove = int(simpledialog.askstring("Remover", "Digite o ID do gasto a remover:", parent=root))
        if remove_expense(id_remove):
            messagebox.showinfo("Sucesso", "Gasto removido!", parent=root)
            gui_list_expenses()
        else:
            messagebox.showerror("Erro", "ID não encontrado.", parent=root)
    except (ValueError, TypeError):
        messagebox.showerror("Erro", "ID inválido.", parent=root)

def gui_total_month():
    hoje = datetime.now()
    total = total_month(hoje.year, hoje.month)
    messagebox.showinfo("Total do mês", f"Total do mês atual: €{total:.2f}", parent=root)

tk.Button(root, text="Adicionar gasto", width=20, command=gui_add_expense).pack(pady=5)
# Antes
# tk.Button(root, text="Listar gastos", width=20, command=gui_list_expenses).pack(pady=5)
# Agora não precisa mais
tk.Button(root, text="Remover gasto", width=20, command=gui_remove_expense).pack(pady=5)
tk.Button(root, text="Total do mês", width=20, command=gui_total_month).pack(pady=5)

gui_list_expenses()
root.mainloop()