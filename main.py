import json
import os

# Nome do arquivo onde as tarefas serão salvas no disco
ARQUIVO_BANCO = "tasks.json"


def carregar_tarefas():
    """Lê o arquivo JSON e retorna a lista de tarefas.
    Se o arquivo não existir ou estiver corrompido, retorna uma lista vazia.
    """
    if not os.path.exists(ARQUIVO_BANCO):
        return []

    try:
        with open(ARQUIVO_BANCO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except Exception:
        # Tratamento simples para evitar crash caso o arquivo esteja corrompido
        return []


def salvar_tarefas(tarefas):
    """Grava a lista atualizada de tarefas no arquivo JSON."""
    with open(ARQUIVO_BANCO, "w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, ensure_ascii=False, indent=2)


def adicionar_tarefa(tarefas):
    """Pede a descrição ao usuário e adiciona uma nova tarefa na lista."""
    descricao = input("\nDigite a descrição da tarefa: ").strip()

    if not descricao:
        print("❌ A descrição não pode ser vazia.")
        return

    # Gera um ID numérico simples baseado no tamanho da lista + 1
    novo_id = len(tarefas) + 1
    nova_tarefa = {
        "id": novo_id,
        "descricao": descricao,
        "concluida": False
    }

    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)
    print(f"✓ Tarefa '{descricao}' adicionada com sucesso! (ID: {novo_id})")


def listar_tarefas(tarefas):
    """Exibe na tela todas as tarefas cadastradas."""
    if not tarefas:
        print("\n📌 Nenhuma tarefa cadastrada no momento.")
        return

    print("\n--- LISTA DE TAREFAS ---")
    for t in tarefas:
        # Define o status visual com base no booleano t['concluida']
        status = "✔" if t["concluida"] else " "
        print(f"[{status}] ID {t['id']}: {t['descricao']}")
    print("------------------------")


def concluir_tarefa(tarefas):
    """Altera o status de uma tarefa para concluída com base no ID fornecido."""
    listar_tarefas(tarefas)
    if not tarefas:
        return

    try:
        id_busca = int(input("\nDigite o ID da tarefa que deseja concluir: "))
    except ValueError:
        print("❌ Por favor, digite apenas números válidos.")
        return

    # Busca a tarefa pelo ID informado
    for t in tarefas:
        if t["id"] == id_busca:
            if t["concluida"]:
                print("⚠️ Esta tarefa já foi concluída anteriormente.")
                return
            
            t["concluida"] = True
            salvar_tarefas(tarefas)
            print(f"✓ Tarefa #{id_busca} marcada como concluída!")
            return

    print(f"❌ Nenhuma tarefa encontrada com o ID {id_busca}.")


def menu():
    """Interface do usuário via terminal."""
    # Carrega os dados existentes assim que o programa inicia
    tarefas = carregar_tarefas()

    while True:
        print("\n=== GERENCIADOR DE TAREFAS ===")
        print("1. Adicionar tarefa")
        print("2. Listar tarefas")
        print("3. Concluir tarefa")
        print("4. Sair")

        opcao = input("Escolha uma opção (1-4): ").strip()

        if opcao == "1":
            adicionar_tarefa(tarefas)
        elif opcao == "2":
            listar_tarefas(tarefas)
        elif opcao == "3":
            concluir_tarefa(tarefas)
        elif opcao == "4":
            print("\nEncerrando o programa... Bons estudos!")
            break
        else:
            print("❌ Opção inválida, tente novamente.")


# Ponto de entrada padrão em scripts Python
if __name__ == "__main__":
    menu()