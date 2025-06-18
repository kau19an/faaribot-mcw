import pywikibot, re, json

# Caminho do arquivo JSON com a lista de páginas
CAMINHO_JSON = "scripts/data/delete_template.json"
RESUMO_EDICAO = "Removendo predefinição (...)"
#! Altere o resumo acima para a sua predefinição

# Regex para detectar a predefinição (com multilinhas e parâmetros)
#! Altere abaixo para o nome da predefinição que deseja remover:
PREDEF = r"\n?\{\{\s*ALTERE-ISSO.*?\}\}\n?"

# Fazer conexão com a Wiki
site = pywikibot.Site("pt", "mcw")
site.login()

# Lê a lista de páginas a serem excluídas
try:
    with open(CAMINHO_JSON, encoding="utf-8") as f:
        paginas = json.load(f)
except FileNotFoundError:
    print(f"⛔ Arquivo '{CAMINHO_JSON}' não encontrado.")
    exit()

# Verifica se há páginas na lista JSON
paginas_validas = [p.strip() for p in paginas if p.strip()]
if not paginas_validas:
    print("⛔ A lista de páginas está vazia.")
    exit()

# Processa cada página
for titulo in paginas_validas:
    pagina = pywikibot.Page(site, titulo)

    print(f"\n🔍 Processando: {pagina.title()}")

    if not pagina.exists():
        print("❌ Página inexistente. Pulando.")
        continue

    texto_antigo = pagina.text

    # Substitui a predefinição removendo a(s) quebra(s) de linha(s) junto
    novo_texto = re.sub(PREDEF, "", texto_antigo, flags=re.DOTALL | re.IGNORECASE)

    if novo_texto != texto_antigo:
        pagina.text = novo_texto.strip() + "\n"
        try:
            pagina.save(summary=RESUMO_EDICAO)
            print("✅ Predefinição removida com sucesso.")
        except Exception as e:
            print(f"❗ Erro ao salvar: {e}")
    else:
        print("⚠️  Nenhuma predefinição encontrada. Pulando.")