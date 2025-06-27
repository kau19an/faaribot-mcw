import pywikibot, json, re

caminho_JSON = "scripts/data/convert_dates.json"
resumo_edicao = "Convertendo datas para o formato em português."

# Dicionário de tradução dos meses
meses = {
    "january": "janeiro", "february": "fevereiro", "march": "março",
    "april": "abril", "may": "maio", "june": "junho",
    "july": "julho", "august": "agosto", "september": "setembro",
    "october": "outubro", "november": "novembro", "december": "dezembro"
}

# Regex pra datas em inglês: "(mês dia, ano)"
padrao_data = re.compile(
    r"\b(" + "|".join(meses.keys()) + r")\s+(\d{1,2}),\s+(\d{4})\b",
    flags=re.IGNORECASE
)

# Função que traduz a data
def traduzir_data(match):
    mes_en = match.group(1).lower()
    dia = match.group(2)
    ano = match.group(3)
    mes_pt = meses.get(mes_en)
    return f"{dia} de {mes_pt} de {ano}"

# Lê a lista de páginas do arquivo JSON
try:
    with open(caminho_JSON, encoding="utf-8") as f:
        paginas = json.load(f)
except FileNotFoundError:
    print(f"⛔ Arquivo '{caminho_JSON}' não encontrado.")
    exit()

# Filtra as páginas válidas
paginas_validas = [p.strip() for p in paginas if p.strip()]
if not paginas_validas:
    print("⛔ A lista de páginas está vazia.")
    exit()

# Fazer conexão com a Wiki
site = pywikibot.Site("pt", "mcw")
site.login()

# Processa cada página
for titulo in paginas_validas:
    pagina = pywikibot.Page(site, titulo)

    print(f"\n🔍 Processando: {pagina.title()}")

    if not pagina.exists():
        print("❌ Página inexistente. Pulando.")
        continue

    texto_antigo = pagina.text
    novo_texto = padrao_data.sub(traduzir_data, texto_antigo)

    if novo_texto != texto_antigo:
        pagina.text = novo_texto
        try:
            pagina.save(summary=resumo_edicao)
            print("✅ Datas convertidas com sucesso.")
        except Exception as e:
            print(f"❗ Erro ao salvar: {e}")
    else:
        print("⚠️ Nenhuma data em inglês foi encontrada. Pulando.")
