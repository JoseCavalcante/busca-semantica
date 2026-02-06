# Manual do Usuário - Busca Semântica

Bem-vindo ao sistema de **Busca Semântica**! Este manual foi criado para ajudá-lo a navegar e utilizar todas as funcionalidades da plataforma de recrutamento inteligente.

## 1. Acesso ao Sistema

Para acessar a plataforma, abra seu navegador e digite o endereço fornecido pelo administrador (ex: `http://localhost:8001/`).

1.  Você verá a tela de **Login**.
2.  Insira seu **Usuário** e **Senha**.
3.  Clique em **Entrar**.

> **Nota**: Se você não tiver credenciais, entre em contato com o administrador do sistema.

## 2. Visão Geral do Painel (Dashboard)

Após o login, você será direcionado ao Painel Principal. À esquerda, você encontrará o **Menu de Navegação** com as seguintes opções:

*   **🔍 Busca**: Para pesquisar candidatos.
*   **📂 Upload**: Para adicionar novos currículos ao banco de dados.
*   **💼 Vagas**: Para criar e gerenciar vagas de emprego.
*   **📜 Histórico**: Para visualizar suas atividades recentes.
*   **Sair**: Para desconectar sua conta.

## 3. Adicionando Currículos (Upload)

Para que o sistema encontre candidatos, é necessário alimentar o banco de dados com currículos.

1.  Clique em **📂 Upload** no menu lateral.
2.  Você verá um formulário para envio de arquivos.
3.  **Selecione o arquivo**: O sistema aceita formatos **PDF** ou **DOCX**.
4.  (Opcional) Preencha informações adicionais se solicitado (ex: Data de recebimento).
5.  Clique em **Enviar**.
6.  Aguarde o processamento. O sistema irá:
    *   Extrair o texto do arquivo.
    *   Usar Inteligência Artificial para identificar habilidades e experiência.
    *   Salvar o candidato no banco de dados.

## 4. Buscando Candidatos

Esta é a principal funcionalidade do sistema. Você pode buscar candidatos descrevendo o perfil desejado em linguagem natural.

1.  Clique em **🔍 Busca** no menu lateral.
2.  Na caixa de pesquisa, digite o que você procura.
    *   *Exemplo*: "Gerente de projetos com experiência em metodologias ágeis e certificação PMP."
    *   *Exemplo*: "Desenvolvedor Python júnior que saiba FastAPI."
3.  Pressione **Enter** ou clique no botão de busca.
4.  O sistema exibirá uma lista de candidatos ordenados por relevância.
5.  Clique em um candidato para ver mais detalhes ou baixar o currículo original.

## 5. Gerenciando Vagas

Você pode cadastrar vagas para organizar seus processos seletivos.

1.  Clique em **💼 Vagas** no menu lateral.
2.  Para criar uma nova vaga, clique em **Nova Vaga** (ou botão similar).
3.  Preencha os detalhes: Título, Departamento, Descrição, Requisitos, etc.
4.  Salve a vaga.
5.  Futuramente, você poderá usar essa vaga para buscar candidatos automaticamente que se encaixem no perfil.

## 6. Histórico e Auditoria

Para rever suas ações passadas:

1.  Clique em **📜 Histórico** no menu lateral.
2.  Você verá uma lista das suas últimas buscas e uploads.
3.  Isso é útil para retomar uma seleção de onde parou.

## Dicas para Melhores Resultados

*   **Seja específico na busca**: Quanto mais detalhes você der sobre a vaga, melhor a IA entenderá o perfil ideal.
*   **Qualidade dos Arquivos**: Currículos em PDF gerados digitalmente (não escaneados como imagem) têm melhor qualidade de extração.
