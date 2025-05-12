import pywikibot, unicodedata, re, os

# TODO: Fazer ele indentar a chave final '}' corretamente numa nova linha e não colado com a vírgula do último elemento da lista.
# TODO: Já abrir a lista automaticamente no computador do usuário para conferir em vez de ele ter que fazer isso manualmente.

INDENTACAO = '        '  # 8 espaços (dois TABs)

# Página alvo (de onde a lista será puxada)
# Exemplo: Módulo:SpriteFile/ItemSprite
pagina_alvo = ""

# Garante que a pasta de saída 'data' exista
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Funções auxiliares
def extrair_lista(texto):
    padrao = r'ids\s*=\s*\{(.*?)^\s*\}\s*\n?\}'
    match = re.search(padrao, texto, flags=re.DOTALL | re.MULTILINE)
    return match.group(1).strip() if match else None

def substituir_lista(texto, nova_lista):
    padrao = r'(ids\s*=\s*\{)(.*?)(^\s*\}\s*\n?\})'
    return re.sub(padrao, r'\1\n' + nova_lista + r'\3', texto, flags=re.DOTALL | re.MULTILINE)

def ordenar_linhas(lista_bruta):
    linhas = [linha for linha in lista_bruta.strip().splitlines() if linha.strip()]

    def extrair_chave(linha):
        match = re.search(r'\[\s*"(.+?)"\s*\]', linha)
        if not match:
            return linha.strip()
        chave = match.group(1)
        # Remove os acentos só pra ordenar
        chave_sem_acentos = ''.join(
            c for c in unicodedata.normalize('NFD', chave)
            if unicodedata.category(c) != 'Mn'
        )
        return chave_sem_acentos.lower()

    ordenadas = sorted(linhas, key=extrair_chave)
    return [f"{INDENTACAO}{linha.strip()}" for linha in ordenadas]

# Fazer conexão com a Wiki
site = pywikibot.Site('pt', 'mcw')
site.login()

pagina = pywikibot.Page(site, pagina_alvo)
if not pagina.exists():
    print(f"❌ A página \"{pagina.title()}\" não existe.")
    exit()

print(f"📄 Página encontrada: \"{pagina.title()}\"")

texto_original = pagina.text
lista_bruta = extrair_lista(texto_original)
if not lista_bruta:
    print("❌ A lista não foi encontrada na estrutura esperada.")
    exit()

# 1. Exportar a lista original num arquivo .txt
path_original = os.path.join(DATA_DIR, "lista_original.txt")
with open(path_original, "w", encoding="utf-8") as f:
    f.write(lista_bruta)

print("\n📝 A lista extraída foi salva como 'lista_original.txt' na pasta 'data'.")
input("⏸️  Antes de continuar, confira o conteúdo. Pressione ENTER para continuar...")

# 2. Ordenar e exportar a lista nova
linhas_ordenadas = ordenar_linhas(lista_bruta)
lista_ordenada = '\n'.join(linhas_ordenadas)

path_ordenada = os.path.join(DATA_DIR, "lista_ordenada.txt")
with open(path_ordenada, "w", encoding="utf-8") as f:
    f.write(lista_ordenada)

print("\n🔠 A lista ordenada foi salva como 'lista_ordenada.txt' na pasta 'data'.")
input("⏸️  Antes de continuar, confira a nova lista. Pressione ENTER para aplicar na Wiki...")

# 3. Substituir na página alvo
texto_final = substituir_lista(texto_original, lista_ordenada)

if texto_final != texto_original:
    pagina.text = texto_final
    pagina.save(summary="Organizando a lista em ordem alfabética.")
    print("\n✅ A página foi salva com sucesso!")
else:
    print("⚠️ Nenhuma alteração foi detectada.")