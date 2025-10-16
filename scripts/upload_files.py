import pywikibot, os

PASTA_UPLOAD = "scripts/upload"

#! Se deseja adicionar categorias ao arquivo, liste seus nomes abaixo ou mantenha-as vazias.
CATEGORIAS_PADRAO = [
    # "..."
]

# Todas as licenças de arquivo da Wiki
LICENÇAS = {
    '1': {
        'desc': 'Conteúdo do Minecraft',
        'template': 'Licença Mojang'
    },

    '2': {
        'desc': 'Conteúdo de Um Filme Minecraft',
        'template': 'Licença Warner Bros.'
    },

    '3': {
        'desc': 'GNU Free Documentation',
        'template': 'Licença GFDL'
    },

    '4': {
        'desc': 'Creative Commons Attribution 3.0',
        'template': 'Licença cc-by'
    },

    '5': {
        'desc': 'Creative Commons Attribution-NonCommercial 3.0',
        'template': 'Licença cc-by-nc'
    },

    '6': {
        'desc': 'Creative Commons Attribution-NoDerivs 3.0',
        'template': 'Licença cc-by-nd'
    },

    '7': {
        'desc': 'Creative Commons Attribution-ShareAlike 3.0',
        'template': 'Licença cc-by-sa'
    },

    '8': {
        'desc': 'Creative Commons Attribution-NonCommercial-ShareAlike 3.0',
        'template': 'Licença cc-by-nc-sa'
    },

    '9': {
        'desc': 'Não está licenciado ou não tenho certeza',
        'template': 'Licença copyvio'
    },

    '10': {
        'desc': 'Contém geometria simples',
        'template': 'Licença geometria simples'
    },

    '11': {
        'desc': 'Está em domínio público',
        'template': 'Licença domínio público'
    },

    '12': {
        'desc': 'É protegido por direitos autorais, mas o uso é permitido',
        'template': 'Licença direitos autorais'
    },

    '13': {
        'desc': 'Música por C418',
        'template': 'Licença C418'
    },

    '14': {
        'desc': 'Conteúdo da NetEase',
        'template': 'Licença NetEase'
    },

    '15': {
        'desc': 'Creative Commons Public Domain',
        'template': 'Licença cc-pd'
    },

    '16': {
        'desc': 'Arte livre',
        'template': 'Licença free art'
    },

    '17': {
        'desc': 'Conteúdo da Wiki.vg',
        'template': 'Licença wiki.vg'
    },
}

# Regex simples para filtrar apenas as extensões de arquivos permitidas na Wiki
EXTENSOES_VALIDAS = (
    '.png', '.gif', '.jpg', '.jpeg', '.webp', '.ico', '.woff', '.woff2', '.svg', '.ogg',
    '.ogv', '.oga', '.flac', '.opus', '.wav', '.webm', '.mp4', '.mp3', '.midi', '.mid'
)

def listar_arquivos():
    # Verifica se a pasta 'upload' existe e lista os arquivos a serem enviados
    if not os.path.isdir(PASTA_UPLOAD):
        print(f"⛔ A pasta '{PASTA_UPLOAD}' não foi encontrada. Crie-a e adicione os arquivos.")
        exit()

    caminhos = [os.path.join(PASTA_UPLOAD, f) for f in os.listdir(PASTA_UPLOAD)]
    arquivos_validos = [
        c for c in caminhos
        if os.path.isfile(c) and c.lower().endswith(EXTENSOES_VALIDAS)
    ]

    if not arquivos_validos:
        print(f"⚠️  Nenhum arquivo válido foi encontrado na pasta '{PASTA_UPLOAD}'.")
        exit()

    return arquivos_validos

def escolher_licenca():
    global escolha

    # Pede ao usuário para escolher a licença e retorna o 'template' completo
    print("\nSelecione o número da licença a ser aplicada em TODOS os arquivos:")
    print("  0) Nenhuma licença")

    for num, data in LICENÇAS.items():
        # Exibe todas as licenças disponíveis ao usuário
        print(f"  {num}) {data['desc']}")

    while True:
        escolha = input("> Selecione um número (0 para pular): ").strip()
        
        if escolha == '0':
            return "" # Retorna uma string vazia, sem 'template' de licença

        if escolha in LICENÇAS:
            # Retorna a predefinição envelopada com as chaves {{ e }}
            template_name = LICENÇAS[escolha]['template']
            return f"{{{{ {template_name} }}}}"
        else:
            print("\n❌ Opção inválida. Tente novamente.")

def montar_texto_categorias(lista_categorias):
    if not lista_categorias:
        return ""

    categorias_validas = [c.strip() for c in lista_categorias if isinstance(c, str) and c.strip()]
    
    # Formata como [[Categoria:NOME DA CATEGORIA]]
    texto_categorias = "\n" + "\n".join(f"[[Categoria:{c}]]" for c in categorias_validas)
    return texto_categorias

def main():
    global escolha 

    arquivos_para_enviar = listar_arquivos()
    print(f"✅ {len(arquivos_para_enviar)} arquivo(s) válido(s) encontrado(s) para envio.")
    
    # Escolha da licença
    licenca_template_completa = escolher_licenca()
 
    # Montagem do texto das categorias
    categorias_texto = montar_texto_categorias(CATEGORIAS_PADRAO)
    
    #! Preencha as informações sobre o arquivo abaixo, assim como faria na Wiki.
    #? Saiba mais em: https://pt.mc.wiki/w/Predefinição:Informação
    texto_descricao = f"""{{{{Informação
    | description = 
    | franchise installment = 
    | source = 
    | date = 
    | author = 
    | permission = {licenca_template_completa}
    | other versions = 
    | additional information = 
    }}}}
    
    {categorias_texto}"""

    # Conexão com a Wiki
    site = pywikibot.Site('pt', 'mcw')
    site.login()
    
    # Processamento e envio do(s) arquivo(s)
    for i, caminho_local in enumerate(arquivos_para_enviar):
        nome_arquivo = os.path.basename(caminho_local)
        
        # Garante o espaço nominal "Arquivo:"
        titulo_wiki = f"Arquivo:{nome_arquivo}"
        pagina_arquivo = pywikibot.FilePage(site, titulo_wiki)

        print(f"\n[{i+1}/{len(arquivos_para_enviar)}] 🔍 Processando: {nome_arquivo}")
        
        #! Se deseja alterar o comentário do arquivo, basta editar abaixo. É obrigatório.
        comentario = "Enviado via script."
        
        try:
            pagina_arquivo.upload(
                caminho_local,
                comment=comentario,
                text=texto_descricao,
                watch=False,
                #! A linha abaixo ignora avisos por padrão. Se deseja mantê-los, altere para False.
                ignore_warnings=True,
            )
            print(f"✅ '{nome_arquivo}' foi enviado/sobrescrito com sucesso.")

        except Exception as e:
            print(f"❗ Ocorreu um erro fatal ao enviar '{nome_arquivo}': {e}")
            
if __name__ == "__main__":
    main()