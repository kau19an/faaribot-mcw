## Índice
1. 🤔 [Para que serve?](#-para-que-serve)
2. 🧑🏽‍💻 [Como posso usá-lo?](#-como-posso-usá-lo)<br>
2.1. [Instalando o Python](#1-instalando-o-python-) 🐍<br>
2.2. [Instalando as dependências do Pywikibot](#2-instalando-as-dependências-do-pywikibot-) 📦<br>
2.3. [Configurando o Pywikibot](#3-configurando-o-pywikibot-) 🤖
3. ⚙️ [Rodando os *scripts*](#%EF%B8%8F-rodando-os-scripts)
4. ⏳ [TODOs](#-todos)

## 🤔 Para que serve?
*Faaribot* é o nome do robô que eu utilizo na Minecraft Wiki Brasil para realizar certas tarefas de automatização. Ele é feito totalmente em <img src="https://raw.githubusercontent.com/devicons/devicon/refs/heads/master/icons/python/python-original.svg" alt="Logotipo da linguagem de programação Python" width="16px"> **Python** com o uso da biblioteca [Pywikibot](https://www.mediawiki.org/wiki/Manual:Pywikibot), conectando ao site através da minha conta secundária e executando os *scripts* em meu nome.
* Por ser de uso próprio, algumas funções podem – e muito provavelmente serão – limitadas **apenas a administradores**, como é o caso dos *scripts* que necessitam eliminar uma página, por exemplo, permissão essa **não** concedida aos editores.

Atualmente, o meu robô possui cinco funções:
1. 📅 `convert_dates.py`: Converter datas (inglês → português);
2. 🗑️ `delete_page.py`: Excluir páginas;
3. 🗑️ `delete_template.py`: Excluir predefinições;
4. ➡️ `move_page.py`: Mover páginas;
5. 🔁 `replace.py`: Substituir termos de uma página para outro;
6. ↩️ `rollback.py`: Restaura a revisão de uma página para o ID especificado;
7. 🔠 `sortlist.py`: Ordenar alfabeticamente listas estruturadas em <img src="https://raw.githubusercontent.com/devicons/devicon/refs/heads/master/icons/lua/lua-original.svg" alt="Logoipo da linguagem de programação Lua" width="16px"> Lua [como essa](https://pt.minecraft.wiki/w/Módulo:SpriteFile/ItemSprite).

## 🧑🏽‍💻 Como posso usá-lo?
### 1. Instalando o Python 🐍
Antes de mais nada, **é necessário que você tenha o Python instalado** no seu computador. Caso não tenha, [baixe-o no site oficial](https://www.python.org/downloads/). Se estiver usando <img src="https://raw.githubusercontent.com/devicons/devicon/refs/heads/master/icons/windows11/windows11-original.svg" alt="Logotipo do sistema operacional Windows" width="16px"> Windows, lembre-se de **permitir a criação da variável PATH no seu sistema** para que o Python seja reconhecido pelo Visual Studio Code ou o editor de sua preferência mais facilmente.
* Assim que a instalação for finalizada, você pode confirmar se o Python está na sua máquina ao abrir um prompt de comando/terminal e digitar `py --version`, que deve exibir a versão atual que você acabou de instalar.

### 2. Instalando as dependências do Pywikibot 📦
O próximo passo é instalar as dependências que o Pywikibot necessita para funcionar na sua máquina. Para fazer isso, abra o prompt de comando/terminal e digite as quatro seguintes linhas:
```bash
pip install "requests>=2.20.1"
pip install "mwparserfromhell>=0.5.2"
pip install packaging
pip install importlib_metadata
```

### 3. Configurando o Pywikibot 🤖
Assim que todas elas forem baixadas, instale o próprio Pywikibot com a seguinte linha: `pip install pywikibot`. Em seguida, crie uma pasta no seu computador onde todos os arquivos de configuração que iremos gerar em seguida ficarão armazenados e abra-a com o <img src="https://raw.githubusercontent.com/devicons/devicon/refs/heads/master/icons/vscode/vscode-original.svg" alt="Logotipo do editor Visual Studio Code" width="16px"> Visual Studio Code ou o editor de sua preferência.

Como o Pywikibot não possui a família da Minecraft Wiki por padrão, precisaremos criá-la primeiro com o comando `pwb generate_family_file` para depois fazermos login.
1. Ao executá-lo, você deverá digitar a URL da Minecraft Wiki Brasil, que é: `pt.minecraft.wiki`, e, então, um nome curto para identificá-la. Eu optei por "mcw", mas você quem sabe.
2. Na pergunta sobre criar ou não as *interwikis*, digite `N`. Caso queira um robô que opere nos outros idiomas da Wiki, então digite `e` e indique quais você deseja além do português.
3. Pronto! Você deve ter notado a criação de uma nova pasta chamada `families` e, dentro, um arquivo com esse nome: `(id)_family.py`. Você não precisará mexer em nada!

Antes de entrarmos com a nossa conta na Wiki, é preciso criar um nome de usuário e senha de robô antes. Para isso, [acesse este link](https://pt.minecraft.wiki/w/Especial:BotPasswords) e entre com as suas credenciais. Você verá a página abaixo:
![A página "Senhas de robôs" na Minecraft Wiki Brasil.](https://i.imgur.com/HIsIi7A.png)
1. Digite um nome de usuário para o seu robô e clique em "Criar".
2. Na tela abaixo, defina as permissões que o seu robô necessita e então clique em "Criar" novamente. Eu marquei todas.<br>
![Lista de permissões possíveis para habilitar no robô.](https://i.imgur.com/GdMusRo.png)
3. Uma última página será aberta e, dessa vez, com a senha única que você deverá anotar em algum lugar. Precisaremos dela para o próximo passo.

> Lembrando que, se o seu objetivo for fazer **grandes edições em massa**, considere **criar uma conta secundária** e pedir para [alguém da Weird Gloop](https://pt.minecraft.wiki/w/Minecraft_Wiki:Lista_da_equipe_Weird_Gloop) (hospedagem) ou um [burocrata](https://pt.minecraft.wiki/w/Especial:Lista_de_usuários?group=bureaucrat) para lhe conceder o grupo de usuário "Robôs". Dessa forma, você evita poluir as [mudanças recentes da Wiki](https://pt.minecraft.wiki/w/Especial:Mudanças_recentes) e recebe um filtro especial nas suas edições. Veja, por exemplo, [a minha conta](https://pt.minecraft.wiki/w/Usuário:Faaribot).

Agora, gere os arquivos de configuração do login com `pwb generate_user_files`.
1. Como temos a família da Minecraft Wiki, digite o identificador que definimos antes e confirme. Em seguida, escolha `pt`.
2. Em "*Username*", digite o nome de usuário da sua **conta principal** e prossiga. Escolha `N` para o próximo prompt.
3. Escolha `y` para adicionar uma senha de robô (*BotPassword*) e informe o nome de usuário e senha **do seu robô**.
> Não se preocupe se não ver a senha, ela é oculta por motivos de segurança. Você pode colar e confirmar sem problemas.
4. Escolha `N` para os últimos dois prompts e pronto! Você deverá ver dois arquivos criados: `user-config.py` e `user-password.py`.

Para confirmar se o Pywikibot consegue mesmo logar na sua conta, use o comando `pwb login`.
* Se você ver a mensagem "*Logged in on (id):pt as* (nome da sua conta)", deu tudo certo!

## ⚙️ Rodando os *scripts*
A partir daqui, é você quem manda! Se quiser criar as suas próprias automatizações ou utilizar/se basear nas criadas para o meu robô, sinta-se à vontade! Nesse caso, caso tenha clonado o meu repositório, basta usar `pwb scripts/(nome do script)` e você os rodará!

## ⏳ TODOs
- [ ] Criar este README em inglês;
- [ ] Criar as instruções de como cada *script* funciona.
