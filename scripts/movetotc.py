import pywikibot, json
from pywikibot.page import Page

# TODO: Na parte da busca por redirecionamentos afluentes, o script deve manter o que há após as hashtags encontradas. Ou seja: se for "#REDIRECIONAMENTO [[Poção arremessável#Não fabricável]]", ele não pode simplesmente mover para "#REDIRECIONAMENTO [[Poção Arremessável]]", mas sim, "#REDIRECIONAMENTO [[Poção Arremessável#Não fabricável]]".
# TODO: Verificar se o redirecionamento buscado também não possui subpáginas a serem alteradas. Por exemplo, ao mover "Fogo de artifício" para "Fogo de Artifício", foi encontrado "Fogos de Artifício" e o script o moveu corretamente, mas não percebeu que ele também tinha uma subpágina "Fogos de Artifício/ED", ainda mantendo esse redirecionamento duplo.

# Fazer conexão com a Wiki
site = pywikibot.Site('pt', 'mcw')
site.login()

# Lê a lista de páginas a serem movidas em pares
# - À esquerda: o termo sem title-case;
# - À direita: o termo com title-case.
with open("scripts/data/movetotc.json", encoding="utf-8") as f:
    pares = json.load(f)

# Verifica se há pelo menos uma página presente na lista
if not pares:
    print('⛔ A lista está vazia. Adicione páginas antes de executar o script.')
    exit()

# Define as mensagens que aparecerão nas mudanças recentes da Wiki
resumo_deletar = 'Eliminada para mover "[[{orig}]]"'
resumo_mover = 'Tradução oficial do jogo passou a usar "title-case".'

for origem_titulo, destino_titulo in pares.items():
    # Verificações iniciais
    if not origem_titulo.strip() or not destino_titulo.strip():
        print(f'\n⛔ Par inválido encontrado: "{origem_titulo}": "{destino_titulo}". Nenhum dos dois pode estar vazio. Corrija-o(s) na lista e tente novamente.')
        continue

    if origem_titulo == destino_titulo:
        print(f'\n⛔ A página de destino especificada para "{origem_titulo}" tem o mesmo nome. Corrija-a na lista e tente novamente.')
        continue

    origem = Page(site, origem_titulo)
    destino = Page(site, destino_titulo)

    print(f'\n🔁 Processando: "{origem_titulo}" → "{destino_titulo}"')

    if not origem.exists():
        print(f'\n❌ A página de origem não existe. Pulando.')
        continue

    if destino.exists():
        try:
            print(f'\n🗑️  Deletando a página: "{destino_titulo}"')
            destino.delete(
                reason=resumo_deletar.format(orig=origem_titulo),
                prompt=False
            )
        except Exception as e:
            print(f'\n❗ Erro ao deletar: {e}')
            continue

    try:
        print(f'\n➡️  Movendo a página...')
        origem.move(
            newtitle=destino.title(),
            reason=resumo_mover,
            movetalk=True,     # Move todas as discussões
            movesubpages=True, # Move todas as subpáginas
            noredirect=False   # Mantém o redirecionamento
        )
        print(f'\n✅ Sucesso ao mover!')
    except Exception as e:
        print(f'\n❗ Erro ao mover: {e}')
        continue

    # Atualizar os redirecionamentos que apontavam para a origem
    print(f'\n🔍 Buscando por redirecionamentos que apontam para "{origem_titulo}"...')
    redirs = origem.getReferences(filter_redirects=True, follow_redirects=False)

    for redir in redirs:
        try:
            if redir.isRedirectPage():
                alvo_anterior = redir.getRedirectTarget().title()
                redirect_antigo = Page(site, redir.title())
                redirect_antigo.text = f'#REDIRECIONAMENTO [[{destino_titulo}]]'
                redirect_antigo.save(
                    summary=f'Alvo de redirecionamento alterado de [[{alvo_anterior}]] para [[{destino_titulo}]]'
                )
                print(f'\n🔄 Redirecionamento atualizado: "{redirect_antigo.title()}" → "{destino_titulo}"')
        except Exception as e:
            print(f'❗ Erro ao atualizar o redirecionamento "{redir.title()}": {e}')

    print('\n----------') # Separador