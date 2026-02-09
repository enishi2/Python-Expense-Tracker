from services import add_expense, get_all_expenses, remove_expense, total_month
from models import Category
from datetime import datetime


def menu():
    print("\n=== SISTEMA DE CONTROLE FINANCEIRO ===")
    print("1 - Adicionar gasto")
    print("2 - Listar gastos")
    print("3 - Remover gasto")
    print("4 - Total do mês")
    print("0 - Sair")


def main():
    while True:
        menu()
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            # Adicionar gasto
            try:
                valor = float(input("Valor (€): "))
                descricao = input("Descrição: ")

                print("Categorias disponíveis:")
                for c in Category:
                    print(f"- {c.value}")
                cat_input = input("Categoria: ").strip()

                # Transformar texto em Enum
                categoria = None
                for c in Category:
                    if c.value.lower() == cat_input.lower():
                        categoria = c
                        break
                if categoria is None:
                    print("Categoria inválida!")
                    continue

                add_expense(valor, categoria, descricao)
                print("Gasto adicionado com sucesso!")

            except ValueError:
                print("Valor inválido!")

        elif escolha == "2":
            # Listar gastos
            gastos = get_all_expenses()
            if not gastos:
                print("Nenhum gasto registrado.")
            else:
                for g in gastos:
                    print(g)

        elif escolha == "3":
            # Remover gasto
            try:
                id_remove = int(input("ID do gasto a remover: "))
                if remove_expense(id_remove):
                    print("Gasto removido!")
                else:
                    print("ID não encontrado.")
            except ValueError:
                print("ID inválido.")

        elif escolha == "4":
            # Total do mês
            hoje = datetime.now()
            total = total_month(hoje.year, hoje.month)
            print(f"Total do mês atual: €{total:.2f}")

        elif escolha == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()