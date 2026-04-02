# Estrutura do Projeto — Linhas de Cuidado Caraguatatuba

Sistema de gestão clínica para o AME de Caraguatatuba, com duas linhas de cuidado: **Hipertensão (HAS)** e **Anticoagulação**. Desenvolvido em Django 5 com autenticação centralizada e controle de acesso por papel.

---

## Raiz do Projeto

| Arquivo | Função |
|---|---|
| `manage.py` | Ponto de entrada do Django para comandos de gerenciamento (migrate, runserver, etc.) |
| `requirements.txt` | Dependências Python do projeto (Django, xhtml2pdf, pandas, reportlab, etc.) |
| `medicamentos.toml` | Catálogo estruturado de medicamentos usado para popular o banco de dados via comando de importação |
| `medicamentos.txt` | Formato alternativo/legado da lista de medicamentos |
| `migrate_db.py` | Script auxiliar para migração de dados entre bancos |
| `key.txt` | Arquivo de chave de configuração (uso interno) |
| `README.md` | Documentação geral do projeto |
| `estrutura.md` | Este arquivo — descrição da função de cada arquivo do projeto |

---

## `linhas_cuidado/` — Configuração do Projeto Django

| Arquivo | Função |
|---|---|
| `settings.py` | Configurações globais: banco de dados (SQLite dev / PostgreSQL prod), apps instalados, modelo de usuário customizado, idioma (pt-br), fuso horário (America/Sao_Paulo) |
| `urls.py` | Roteamento URL principal — inclui as rotas dos apps `core`, `hipertensao` e `anticoagulacao` |
| `wsgi.py` | Ponto de entrada WSGI para deploy em produção |
| `__init__.py` | Marcador de pacote Python |

---

## `core/` — Autenticação e Gestão de Usuários

Módulo responsável pelo login, perfis profissionais e controle de acesso de todo o sistema.

### Python

| Arquivo | Função |
|---|---|
| `models.py` | Modelo `Usuario` (extensão de `AbstractUser`): tipos profissionais (MED, ENF, NUT, FAR, ADM), papéis sistêmicos (`is_administrador`, `is_navegador`), campos de registro profissional (CRM, COREN, CRN, CRF), geração automática de assinatura |
| `views.py` | Views de autenticação: login, logout, troca de senha, gestão de usuários (criar, editar, ativar/desativar, excluir), página de perfil |
| `forms.py` | Formulários de autenticação e cadastro de usuário |
| `urls.py` | Rotas do módulo core (login, logout, perfil, gestão de usuários) |
| `decorators.py` | Decoradores de controle de acesso reutilizáveis por outros módulos |
| `utils.py` | Utilitários de normalização de nomes (capitalização padronizada ao salvar usuário) |
| `admin.py` | Configuração do painel Django Admin para o modelo `Usuario` |
| `apps.py` | Configuração do app Django |
| `management/commands/normalizar_nomes.py` | Comando de gerenciamento para normalizar nomes de usuários existentes no banco |

### Templates

| Arquivo | Função |
|---|---|
| `templates/base.html` | Template base global com navbar, links de assets (Bootstrap, Font Awesome) e bloco de conteúdo |
| `templates/login.html` | Tela de login com formulário de credenciais |
| `templates/index.html` | Página inicial pós-login com cards de acesso às linhas de cuidado |
| `templates/gestao_usuarios.html` | Painel administrativo de listagem, criação, edição e exclusão de usuários |
| `templates/meu_perfil.html` | Página de perfil do usuário logado com exibição da assinatura profissional |
| `templates/trocar_senha.html` | Formulário de troca de senha (obrigatória no primeiro acesso) |

### Static

| Arquivo | Função |
|---|---|
| `static/core/css/palette.css` | Paleta de cores e estilos globais do sistema |

---

## `hipertensao/` — Linha de Cuidado: Hipertensão Arterial

Módulo clínico completo para triagem, acompanhamento multiprofissional e gestão de pacientes hipertensos.

### Python

| Arquivo | Função |
|---|---|
| `models.py` | Modelos de dados: `Medicamento` (banco de fármacos), `Paciente` (cadastro com CPF, SIRESP, etnia, município), `Aferição` (PA, FC, peso, altura, IMC calculado), modelos de consulta multiprofissional, médica, prescrição e exames |
| `views.py` | Views clínicas (~900 linhas): cadastro e busca de pacientes, triagem (critérios PA ≥ 140/90), aferição, consulta multiprofissional, consulta médica (SOAP), cálculo PREVENT, prescrição, solicitação de exames, alta, geração de PDFs, monitoramento, dashboard |
| `forms.py` | Formulários clínicos: triagem, aferição, consulta multiprofissional, médica, prescrição e exames |
| `urls.py` | Rotas do módulo hipertensão |
| `decorators.py` | Decoradores de permissão específicos para profissionais da linha de hipertensão |
| `services_cid.py` | Serviço de conversão automática de CID-10 para CID-11 |
| `admin.py` | Configuração do Django Admin para os modelos de hipertensão |
| `apps.py` | Configuração do app Django |
| `management/commands/load_medicamentos_toml.py` | Comando para importar/atualizar o banco de medicamentos a partir do arquivo `medicamentos.toml` |

### Templates — Páginas Principais

| Arquivo | Função |
|---|---|
| `templates/hipertensao/sidebar.html` | Layout base do módulo com menu lateral e estrutura de navegação |
| `templates/hipertensao/index.html` | Página inicial da linha de cuidado com resumo e acesso rápido |
| `templates/hipertensao/pacientes.html` | Listagem e busca de pacientes (nome, CPF, SIRESP) |
| `templates/hipertensao/prontuario.html` | Prontuário completo: histórico de aferições (gráficos PAS/PAD/PAM), consultas multiprofissionais, consultas médicas e prescrições |
| `templates/hipertensao/atendimento_landing.html` | Hub de atendimento — ponto de entrada para escolha do tipo de consulta |
| `templates/hipertensao/atendimento_opcoes.html` | Listagem de opções de atendimento disponíveis para o paciente |
| `templates/hipertensao/hub_atendimento.html` | Variante do hub de atendimento (layout alternativo) |
| `templates/hipertensao/admin_pacientes.html` | Painel administrativo de pacientes com exclusão e ações privilegiadas |
| `templates/hipertensao/gestao_medicamentos.html` | Interface de gestão do banco de medicamentos (visualização, busca, exportação CSV) |
| `templates/hipertensao/dashboard.html` | Dashboard analítico: pacientes ativos, aferições mensais, controle pressórico, distribuição por sexo/faixa etária, filtro por município |
| `templates/hipertensao/monitoramento_lista.html` | Lista de pacientes para monitoramento por etapa do fluxo (navegador/admin) |
| `templates/hipertensao/monitoramento_painel.html` | Painel individual de monitoramento com contadores de consultas e status de exames |
| `templates/hipertensao/prescricao_form.html` | Formulário de prescrição medicamentosa com busca dinâmica no banco de fármacos |
| `templates/hipertensao/atendimento_prevent.html` | Calculadora de risco cardiovascular PREVENT com estratificação visual por cor |

### Templates — Formulários de Atendimento

| Arquivo | Função |
|---|---|
| `templates/hipertensao/atendimento/ficha_enf_aval_inicial.html` | Ficha de avaliação inicial de enfermagem: dados sociais, antropométricos, tabagismo, lesão de órgão-alvo |
| `templates/hipertensao/atendimento/ficha_consulta_subsequente.html` | Ficha de consulta multiprofissional de retorno |
| `templates/hipertensao/atendimento/ficha_medica.html` | Ficha de consulta médica em formato SOAP com CID-10/CID-11 e exibição do escore PREVENT |
| `templates/hipertensao/atendimento/req_exames.html` | Formulário de solicitação de exames laboratoriais |

### Templates — Documentos PDF

| Arquivo | Função |
|---|---|
| `templates/hipertensao/pdf_receita.html` | Template de receita médica — gera PDF com separação automática de medicamentos comuns e controlados |
| `templates/hipertensao/pdf_kit_exames.html` | Template de kit completo de exames (receitas + pedidos agrupados) |
| `templates/hipertensao/pdf_pedidos_exames.html` | Template de pedido de exames laboratoriais |
| `templates/hipertensao/pdf_alta.html` | Carta de alta do paciente com resumo do acompanhamento |
| `templates/hipertensao/pdf_contrarreferencia_triagem.html` | Documento de contrarreferência para pacientes não elegíveis na triagem |

### Static

| Arquivo | Função |
|---|---|
| `static/hipertensao/img/header.png` | Imagem de cabeçalho usada nos documentos PDF gerados |
| `static/hipertensao/img/footer.png` | Imagem de rodapé usada nos documentos PDF gerados |

---

## `anticoagulacao/` — Linha de Cuidado: Anticoagulação

Módulo para acompanhamento de pacientes em terapia anticoagulante com monitoramento de INR.

### Python

| Arquivo | Função |
|---|---|
| `models.py` | Modelos: `Paciente` (nome, CPF, CROSS, sexo, município, indicação clínica, médico responsável, meta terapêutica INR automática por indicação), `Medicao` (valor INR, data/hora, intercorrência e descrição) |
| `views.py` | Views: cadastro de pacientes, registro de medições INR, monitoramento, painel administrativo, dashboard analítico (endpoint JSON com todos os pacientes e medições ativas) |
| `urls.py` | Rotas do módulo anticoagulação |
| `decorators.py` | Decoradores de permissão específicos para a linha de anticoagulação |
| `admin.py` | Configuração do Django Admin para os modelos de anticoagulação |
| `apps.py` | Configuração do app Django |

### Templates

| Arquivo | Função |
|---|---|
| `templates/anticoagulacao/base.html` | Layout base do módulo com menu lateral |
| `templates/anticoagulacao/index.html` | Página inicial da linha de cuidado |
| `templates/anticoagulacao/pacientes.html` | Listagem e busca de pacientes ativos/inativos |
| `templates/anticoagulacao/atendimento.html` | Registro de medição INR com exibição do histórico em gráfico das últimas 10 medições e alerta de intercorrências |
| `templates/anticoagulacao/dashboard.html` | Dashboard analítico consolidado da linha de anticoagulação |
| `templates/anticoagulacao/admin/painel.html` | Painel administrativo com contagem de pacientes e usuários e acesso ao Django Admin |
| `templates/anticoagulacao/admin/pacientes_admin.html` | Listagem administrativa de pacientes com data de inserção e opções de gerenciamento |

### Static

| Arquivo | Função |
|---|---|
| `static/anticoagulacao/js/scripts.js` | JavaScript do módulo: lógica de gráficos INR, interações de formulário e comportamentos dinâmicos de interface |

---

## Controle de Acesso (visão geral)

| Nível | Onde é definido | O que controla |
|---|---|---|
| Tipo profissional (MED, ENF, NUT, FAR, ADM) | `core/models.py` | Acesso a formulários e ações clínicas específicas |
| `is_administrador` | `core/models.py` | Gestão de usuários, dashboard, exclusão de pacientes, gestão de medicamentos |
| `is_navegador` | `core/models.py` | Acesso à fila de monitoramento de pacientes |
| Decoradores de app | `*/decorators.py` | Aplicação das permissões nas views de cada módulo |
