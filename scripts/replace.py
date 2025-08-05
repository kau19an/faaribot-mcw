import pywikibot, json, re

# Protege blocos sensíveis (<nowiki>, <pre>, <code>, comentários etc.)
def proteger_blocos(texto):
    blocos_protegidos = {}
    def proteger(match):
        chave = f"__BLOCO_{len(blocos_protegidos)}__"
        blocos_protegidos[chave] = match.group(0)
        return chave

    padrao = r'(<nowiki>.*?</nowiki>|<pre>.*?</pre>|<code>.*?</code>|<!--.*?-->)'
    texto_temp = re.sub(padrao, proteger, texto, flags=re.DOTALL)
    return texto_temp, blocos_protegidos

def restaurar_blocos(texto_temp, blocos_protegidos):
    for chave, bloco in blocos_protegidos.items():
        texto_temp = texto_temp.replace(chave, bloco)
    return texto_temp

# Substitui apenas palavras isoladas (com \b)
def substituir_palavra_exata(texto, antigo, novo):
    padrao = r'\b' + re.escape(antigo) + r'\b'
    return re.sub(padrao, novo, texto)

# Lê a lista de termos a serem substituídos em pares
# - À esquerda: o termo atual; À direita: o novo termo.
with open("scripts/data/replace.json", encoding="utf-8") as f:
    dados = json.load(f)

# Encontra os termos atuais na página especificada em 'alvo'
pagina_alvo = dados.get('alvo')
if not pagina_alvo:
    print('⛔ Nenhuma página alvo foi definida na lista. Adicione páginas antes de executar o script.')
    exit()

substituicoes = {k: v for k, v in dados.items() if k != 'alvo'}

# Fazer conexão com a Wiki
site = pywikibot.Site('pt', 'mcw')
site.login()

pagina = pywikibot.Page(site, pagina_alvo)
if not pagina.exists():
    print(f'❌  A página "{pagina_alvo}" não existe.')
    exit()

print(f'✏️  Editando: {pagina.title()}')

texto_original = pagina.text
texto_temp, blocos = proteger_blocos(texto_original)

linhas_original = texto_temp.split('\n')
linhas_editadas = linhas_original[:]

# Fazer substituições e mostrar o que mudou
for i, linha in enumerate(linhas_editadas):
    linha_original = linha
    for antigo, novo in substituicoes.items():
        linha = substituir_palavra_exata(linha, antigo, novo)
    if linha != linhas_original[i]:
        print(f'\n🔄 Linha alterada:')
        print(f'➖ {linhas_original[i]}')
        print(f'➕ {linha}')
        linhas_editadas[i] = linha

texto_editado_temp = '\n'.join(linhas_editadas)
texto_editado = restaurar_blocos(texto_editado_temp, blocos)

# Verificar mudanças
if texto_editado != texto_original:
    pagina.text = texto_editado
    pagina.save(summary='')
    #! Altere acima para o motivo pela qual deseja substituir o(s) termo(s)
    print('\n✅ A página foi salva com sucesso!')
else:
    print('\n⚠️  Nenhuma alteração foi feita. Todos os termos já estavam atualizados.')
