import pywikibot

# Define a página e o ID da revisão à qual se deseja retornar
pagina_alvo = ""
id_revisao = 000000
#! Substitua as informações acima pelo o que deseja

# Fazer conexão com a Wiki
site = pywikibot.Site('pt', 'mcw')
site.login()

pagina = pywikibot.Page(site, pagina_alvo)

if not pagina.exists():
    print(f"❌ A página \"{pagina.title()}\" não existe.")
    exit()

print(f"\n📄 Página encontrada: {pagina.title()}")

# Tenta obter o conteúdo da revisão
try:
    conteudo_antigo = pagina.getOldVersion(oldid=id_revisao)
except Exception as e:
    print(f"❌ Não foi possível recuperar a revisão de ID {id_revisao}: {e}")
    exit()

# Verifica se é diferente do código-fonte atual
texto_atual = pagina.text
if texto_atual.strip() == conteudo_antigo.strip():
    print("⚠️ O conteúdo da revisão é idêntico ao atual. Nada a ser feito.")
    exit()

# Mostra um trecho do conteúdo (apenas para confirmar visualmente)
print("\n📝 Trecho do conteúdo da revisão escolhida:\n")
print('\n'.join(conteudo_antigo.strip().splitlines()[:10]))
print("...")

# Confirma a restauração com o usuário antes de prosseguir
print(f"\nVocê está prestes a restaurar a página \"{pagina.title()}\" para a revisão de ID {id_revisao}. Deseja continuar? (y/n)")
confirmacao = input("> ").strip().lower()
if confirmacao != 'y':
    print("❌ Ação cancelada.")
    exit()

# Aplica a alteração
try:
    pagina.text = conteudo_antigo
    pagina.save(summary=f"Revertendo para a revisão de ID {id_revisao}.")
    print("✅ Página restaurada com sucesso.")
except Exception as e:
    print(f"❗ Erro ao tentar salvar: {e}")
