import pywikibot, re, json

# Caminho do arquivo JSON com a lista de páginas
caminho_json = "scripts/data/delete_template.json"
resumo_edicao = ""
#! Altere o resumo acima para o que desejar

#! Altere abaixo para o nome da predefinição que deseja remover (não é case-sensitive e permite parâmetros):
predef = ""

# Fazer conexão com a Wiki
site = pywikibot.Site("pt", "mcw")
site.login()

# Lê a lista de páginas a serem excluídas
try:
    with open(caminho_json, encoding="utf-8") as f:
        paginas = json.load(f)
except FileNotFoundError:
    print(f"⛔ Arquivo '{caminho_json}' não encontrado.")
    exit()

# Verifica se há páginas na lista JSON
paginas_validas = [p.strip() for p in paginas if p.strip()]
if not paginas_validas:
    print("⛔ A lista de páginas está vazia.")
    exit()

# Função para remover a predefinição
def remover_predef(texto, nome_predef):
    nome_predef = nome_predef.lower()
    idx = 0
    novo_texto = texto
    while True:
        match = re.search(r"\{\{(" + re.escape(nome_predef) + r")(\s*[\|}])", novo_texto[idx:], re.IGNORECASE)
        if not match:
            break

        inicio = idx + match.start()
        i = inicio
        aberto = 0

        # Conta quantos {{ e }} foram abertos/fechados para saber exatamente onde a predefinição especificada termina
        while i < len(novo_texto) - 1:
            if novo_texto[i:i+2] == "{{":
                aberto += 1
                i += 2
            elif novo_texto[i:i+2] == "}}":
                aberto -= 1
                i += 2
                if aberto == 0: # 0 = encontrado o fim da predefinição especificada
                    # Remove os espaços antes e depois dela, caso houver
                    while inicio > 0 and novo_texto[inicio - 1] in "\n ":
                        inicio -= 1
                    novo_texto = novo_texto[:inicio] + novo_texto[i:]
                    break
            else:
                i += 1 # Avança de caractere caso não encontre {{ ou }}
        else:
            break
    return novo_texto

# Processa cada página
for titulo in paginas_validas:
    pagina = pywikibot.Page(site, titulo)
    print(f"\n🔍 Processando: {pagina.title()}")

    if not pagina.exists():
        print("❌ Página inexistente. Pulando.")
        continue

    texto_antigo = pagina.text
    texto_novo = remover_predef(texto_antigo, predef)

    if texto_antigo != texto_novo:
        pagina.text = texto_novo.strip() + "\n"
        try:
            pagina.save(summary=resumo_edicao)
            print("✅ Predefinição removida com sucesso.")
        except Exception as e:
            print(f"❗ Erro ao salvar: {e}")
    else:
        print("⚠️  Nenhuma predefinição encontrada. Pulando.")