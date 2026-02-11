import tkinter as tk
from tkinter import messagebox, simpledialog
from services import add_expense, get_all_expenses, remove_expense, total_month, search_expenses
from models import Category
from datetime import datetime


root = tk.Tk()
root.title("Sistema de Controle Financeiro")
root.geometry("500x500")


def update_results():
    keyword = search_entry.get()
    selected_cat = category_var.get()

    # Define a categoria
    category = None
    if selected_cat != "Todas":
        for c in Category:
            if c.value == selected_cat:
                category = c
                break

    # Chama a função de busca
    results = search_expenses(keyword, category)

    # Atualiza a área de resultados
    result_area.delete(1.0, tk.END)
    if not results:
        result_area.insert(tk.END, "Nenhum gasto encontrado.\n")
    else:
        for g in results:
            result_area.insert(tk.END, str(g) + "\n")


# Caixa de texto para buscar por descrição
search_label = tk.Label(root, text="Buscar por descrição:")
search_label.pack()
search_entry = tk.Entry(root, width=30)
search_entry.pack(pady=5)

# Dropdown para filtrar por categoria
category_label = tk.Label(root, text="Filtrar por categoria:")
category_label.pack()
category_var = tk.StringVar(root)
category_var.set("Todas")  # valor padrão
category_options = ["Todas"] + [c.value for c in Category]
category_menu = tk.OptionMenu(root, category_var, *category_options)
category_menu.pack(pady=5)

result_area = tk.Text(root, height=15, width=60)
result_area.pack(pady=10)

# Atualizar resultados enquanto digita ou muda categoria
search_entry.bind("<KeyRelease>", lambda event: update_results())
category_var.trace_add("write", lambda *args: update_results())

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
    keyword = search_entry.get()
    selected_cat = category_var.get()

    category = None
    if selected_cat != "Todas":
        for c in Category:
            if c.value == selected_cat:
                category = c
                break

    results = search_expenses(keyword or "", category)

    total = sum(e.amount for e in results)
    messagebox.showinfo("Total do mês", f"Total filtrado: €{total:.2f}", parent=root)


# #def gui_search_expenses():
#     keyword = simpledialog.askstring("Busca", "Digite palavra-chave (ou deixe vazio):", parent=root)
#
#     cat_input = simpledialog.askstring(
#         "Categoria",
#         f"Digite a categoria para filtrar ({', '.join(c.value for c in Category)}) ou deixe vazio:",
#         parent=root
#     )

    selected_cat = category_var.get()

    category = None
    if selected_cat != "Todas":
        for c in Category:
            if c.value == selected_cat:
                category = c
                break

    results = search_expenses(keyword or "", category)

    # Atualiza a área de resultados
    result_area.delete(1.0, tk.END)
    if not results:
        result_area.insert(tk.END, "Nenhum gasto encontrado.\n")
    else:
        for g in results:
            result_area.insert(tk.END, str(g) + "\n")


tk.Button(root, text="Adicionar gasto", width=20, command=gui_add_expense).pack(pady=5)
# Antes
# tk.Button(root, text="Listar gastos", width=20, command=gui_list_expenses).pack(pady=5)
# Agora não precisa mais
tk.Button(root, text="Remover gasto", width=20, command=gui_remove_expense).pack(pady=5)
tk.Button(root, text="Total do mês", width=20, command=gui_total_month).pack(pady=5)
#tk.Button(root, text="Buscar gastos", width=20, command=gui_search_expenses).pack(pady=5)

update_results()

gui_list_expenses()
root.mainloop()