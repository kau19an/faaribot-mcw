import pywikibot, json

# TODO: Buscar pelos redirecionamentos apontados ao alvo definido e também deletá-los, evitando deixar quaisquer resquícios.

# Opções de exclusão disponíveis (começando em 1)
# - Entre aspas, a mensagem que aparecerá nas mudanças recentes da Wiki.
grupos = [
    "A pedido do autor",
    "Arquivo sobrescreve o repositório",
    "Sem mais utilidade",
    "[[Project:Regras#2|Regra #2]]: Vandalismo",
    None  # Outro motivo (será pedido depois)
]

# Lê a lista de páginas a serem excluídas
caminho = "scripts/data/delete_page.json"
with open(caminho, encoding="utf-8") as f:
    dados = json.load(f)

# Verifica se há pelo menos uma página presente nos grupos
temPagina = any(p.strip() for grupo in dados.values() for p in grupo if isinstance(p, str))
if not temPagina:
    print("⛔ A lista está vazia. Adicione páginas antes de executar o script.")
    exit()

# Fazer conexão com a Wiki
site = pywikibot.Site('pt', 'mcw')
site.login()

print(f"📁 Lendo as páginas marcadas para exclusão em '{caminho}'...")

# Processa cada grupo
for str_opcao, paginas in dados.items():
    try:
        opcao = int(str_opcao)
    except ValueError:
        print(f"\n⚠️  \"{str_opcao}\" foi definido como um grupo na lista porém somente números são aceitos. Ignorando...")
        continue

    if not (1 <= opcao <= len(grupos)):
        print(f"\n⚠️  \"{opcao}\" foi definido como um grupo na lista porém não possui uma mensagem em 'grupos'. Ignorando...")
        continue

    # Ignora as entradas vazias ("") na lista
    paginas_validas = [p.strip() for p in paginas if p.strip()]
    if not paginas_validas:
        continue

    motivo = grupos[opcao - 1]
    if motivo is None:
        print(f"\n📝 Escreva um motivo:")
        motivo = input("> ").strip()

    print(f"\n🔧 {len(paginas_validas)} página(s) encontrada(s) com o motivo: \"{motivo}\"")

    # Confirmação
    if len(paginas_validas) == 1:
        print(f'\nVocê está prestes a excluir: "{paginas_validas[0]}".')
    else:
        print(f'\nVocê está prestes a excluir: "{paginas_validas[0]}" e outros {len(paginas_validas) - 1}.')

    print("\nDeseja prosseguir? (y/n)")
    resposta = input("> ").strip().lower()

    if resposta != 'y':
        print("❌ A ação foi cancelada para este grupo.")
        continue

    # Executa as exclusões
    for alvo in paginas_validas:
        pagina = pywikibot.Page(site, alvo)
        if not pagina.exists():
            print(f"❌ A página \"{alvo}\" não existe.")
            continue

        try:
            pagina.delete(reason=motivo, prompt=False)
            print(f"✅ \"{alvo}\" foi deletado com sucesso.")
        except Exception as e:
            print(f"❗ Erro ao deletar \"{alvo}\": {e}")