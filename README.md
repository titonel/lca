# Linhas de Cuidado — Caraguatatuba

Sistema integrado de gestão de **linhas de cuidado** para o AME de Caraguatatuba. Reúne em um único projeto Django os programas de **Hipertensão Arterial Sistêmica (HAS)** e **Anticoagulação**, com autenticação centralizada e controle de acesso por perfil profissional.

---

## Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades por Área](#funcionalidades-por-área)
  - [Core — Autenticação e Usuários](#core--autenticação-e-usuários)
  - [Hipertensão Arterial Sistêmica](#hipertensão-arterial-sistêmica)
  - [Anticoagulação](#anticoagulação)
- [Perfis de Acesso](#perfis-de-acesso)
- [Instalação e Deploy](#instalação-e-deploy)
- [Estrutura do Projeto](#estrutura-do-projeto)

---

## Sobre o Projeto

O sistema foi desenvolvido para apoiar equipes multiprofissionais de saúde no gerenciamento de pacientes vinculados a programas de atenção especializada no âmbito do SUS. Cada linha de cuidado possui fluxos clínicos próprios, com suporte a consultas, prescrições, geração de PDFs, monitoramento e dashboards analíticos.

**Tecnologias utilizadas:**
- Python 3.10+ + Django 5
- SQLite (banco de dados padrão)
- Bootstrap 5.3 + Font Awesome 6 (interface)
- xhtml2pdf + ReportLab (geração de PDFs)
- HTML/CSS/JavaScript no front-end

---

## Funcionalidades por Área

### Core — Autenticação e Usuários

Módulo central responsável pelo controle de acesso a todo o sistema.

**Usuários e Perfis**
- Modelo de usuário customizado com campos profissionais: tipo de profissional (Médico, Enfermeiro, Nutricionista, Farmacêutico, Administrativo), tipo de registro (CRM, COREN, CRN, CRF), número de registro e DRT/matrícula.
- Geração automática de assinatura profissional formatada (utilizada em documentos e prescrições).
- Controle de usuários ativos/inativos.

**Autenticação**
- Tela de login com validação de credenciais.
- Troca de senha obrigatória no primeiro acesso (flag `mudar_senha`).
- Logout seguro com redirecionamento.

**Gestão de Usuários (exclusivo para Administradores)**
- Listagem, criação, edição e remoção de usuários do sistema.
- API JSON para consulta de dados de um usuário por ID.
- Cada usuário pode acumular múltiplas alçadas simultaneamente (ex: Médico + Administrador, Enfermeiro + Navegador).
- Alçadas de sistema configuráveis individualmente por usuário: **Administrador do Sistema** e **Navegador** (independentes do tipo profissional).

**Página Inicial**
- Dashboard de entrada com acesso rápido às linhas de cuidado disponíveis.

---

### Hipertensão Arterial Sistêmica

Módulo completo para gestão da linha de cuidado de HAS, cobrindo todo o percurso do paciente desde a triagem até o acompanhamento contínuo.

**Cadastro de Pacientes**
- Registro com dados pessoais, CPF, SIRESP/CROSS, etnia, município e contato.
- Busca por nome, CPF ou número SIRESP.
- Encerramento de acompanhamento com geração de PDF de alta.
- Exclusão completa de registros (somente administradores).

**Triagem**
- Registro de três aferições de pressão arterial com cálculo automático das médias sistólica e diastólica.
- Determinação de elegibilidade ao programa com base nos critérios clínicos (PA ≥ 140/90 ou PA ≥ 130/80 com diabetes ou lesão de órgão-alvo).
- Geração de PDF de contrarreferência para pacientes não elegíveis.

**Aferição de Pressão Arterial**
- Registro de PA, frequência cardíaca, peso e altura.
- Cálculo automático do IMC.
- Vinculação dos medicamentos em uso no momento da aferição.

**Consulta Multidisciplinar**
- Ficha de avaliação abrangente com dados sociais, antropométricos e clínicos.
- Avaliação de tabagismo com cálculo automático da carga tabágica (maços/ano).
- Registro de lesões de órgão-alvo (coração, cérebro, rins, artérias, olhos).
- Registro de diabetes e tipo.

**Avaliação de Risco Cardiovascular (PREVENT)**
- Cálculo do escore PREVENT com risco estimado em 10 e 30 anos.
- Campos: colesterol total, HDL, pressão sistólica, tratamento anti-hipertensivo, diabetes, tabagismo e TFG estimada.

**Consulta Médica (SOAP)**
- Registro de atendimento médico em formato SOAP (Subjetivo, Objetivo, Avaliação, Plano).
- Codificação por CID-10 (principal e secundários) com conversão automática para CID-11.
- Exibição do escore PREVENT com sinalização visual por faixas de risco:
  - Verde: < 5% | Amarelo: 5–7,5% | Laranja: 7,5–20% | Vermelho: ≥ 20%

**Prescrições Médicas**
- Montagem de prescrição com busca de medicamentos do banco (nome, concentração, posologia, quantidade).
- Classificação por tipo: contínuo, temporário ou controlado.
- Impressão de receita em PDF com separação automática de receituário comum e controlado.
- Reimpressão de prescrições anteriores.

**Pedido de Exames**
- Solicitação de exames laboratoriais vinculada ao atendimento médico.
- Geração de PDF de kit de exames padronizado.
- Consulta de resultados via integração com API de laboratório externo (`http://172.15.0.152:5897/api/laboratorio/{cpf}`).

**Gestão de Medicamentos**
- Cadastro e edição do banco de medicamentos (classe, princípio ativo, dose padrão, nomes comerciais, REMUME).
- Exportação em CSV com codificação UTF-8.

**Gestão de Pacientes (Monitoramento)**
- Acessível na landing page da Hipertensão para perfis **Navegador** e **Administrador**.
- Painel de acompanhamento com estágio atual de cada paciente na linha de cuidado:
  - *Aguardando 1ª Consulta Multidisciplinar*
  - *Aguardando Exames / Retorno Multi*
  - *Aguardando Consulta Médica*
  - *Acompanhamento Contínuo*
- Sinalização visual de risco cardiovascular por cor.
- Painel individual do paciente com totalizadores de consultas e status de exames.
- Botão **Gestão de Pacientes (Admin)** visível exclusivamente para Administradores, com acesso à área de administração de pacientes (`gestao-admin/pacientes/`).

**Prontuário do Paciente**
- Histórico completo com gráficos de evolução da PA (PAS, PAD e PAM) ao longo do tempo.
- Histórico de consultas multidisciplinares e médicas.
- Histórico de prescrições.

**Dashboard Analítico (Administradores)**
- Indicadores: total de pacientes ativos, aferições no mês, tempo médio no programa.
- Distribuição por controle de PA, sexo e faixa etária.
- Filtro por município.

---

### Anticoagulação

Módulo para gestão do programa de anticoagulação oral (warfarina e similares), com foco no monitoramento do INR.

**Cadastro de Pacientes**
- Registro com nome, CPF, CROSS, sexo, município, indicação clínica e médico responsável.
- Definição automática da meta terapêutica de INR:
  - **2,5–3,5** para indicações com prótese valvar mecânica.
  - **2,0–3,0** para demais indicações.
- Alta do paciente com registro de data de encerramento.

**Consulta e Registro de INR**
- Registro de medições de INR com data e hora.
- Campo de intercorrência: permite registrar eventos adversos com descrição textual.
- Sinalização automática de intercorrência ao preencher observações.

**Monitoramento do Paciente**
- Visualização das últimas 10 medições de INR em gráfico de série temporal.
- Exibição da meta terapêutica individualizada.
- Listagem de todos os pacientes ativos com busca por nome, CPF ou CROSS.

**Painel Administrativo**
- Lista de todos os pacientes (ativos e inativos) com ordenação por data de inserção.
- Contagem total de pacientes e usuários do sistema.
- Acesso ao Django Admin para manutenção técnica avançada.

**Dashboard Analítico**
- API com dados consolidados de todos os pacientes ativos e suas medições de INR.
- Integração com sistema externo para cruzamento de dados.

---

## Perfis de Acesso

O sistema adota um modelo RBAC (Role-Based Access Control) com dois tipos de atributos independentes por usuário: **tipo profissional** (função clínica) e **alçadas do sistema** (permissões funcionais). Um mesmo usuário pode ter múltiplas alçadas simultaneamente.

### Tipo Profissional (função clínica)

| Tipo | Código | Acesso clínico |
|------|--------|----------------|
| Médico | MED | Consultas médicas, SOAP, prescrições, monitoramento |
| Enfermeiro | ENF | Consultas multidisciplinares, cadastro de pacientes, aferições, INR |
| Nutricionista | NUT | Consultas multidisciplinares, cadastro de pacientes |
| Farmacêutico | FAR | Consultas multidisciplinares, cadastro de pacientes |

### Alçadas do Sistema (permissões funcionais)

| Alçada | Flag | Permissões |
|--------|------|------------|
| Administrador do Sistema | `is_administrador` | Gestão de usuários, dashboards gerenciais, exclusão de pacientes, gestão de medicamentos, exportações, Gestão de Pacientes (Admin) na Hipertensão |
| Navegador | `is_navegador` | Acesso ao card **Gestão de Pacientes** (fila de monitoramento) na Hipertensão |

> **Exemplo:** um Médico com alçada de Administrador tem acesso às funções clínicas de MED e também às funções administrativas. Um Enfermeiro com alçada de Navegador acessa tanto os atendimentos quanto a fila de monitoramento.

> A alçada de Administrador substitui funcionalmente o tipo profissional `ADM` (mantido por compatibilidade), centralizando a gestão de usuários na página inicial do sistema.

---

## Instalação e Deploy

### Pré-requisitos

- Python 3.10 ou superior (recomendado 3.11+ para suporte nativo a TOML)
- pip
- Git
- (Opcional) Virtualenv ou venv

---

### Passo 1 — Clonar o repositório

```bash
git clone https://github.com/titonel/lca.git
cd lca
```

---

### Passo 2 — Criar e ativar o ambiente virtual

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

---

### Passo 3 — Instalar as dependências

```bash
pip install -r requirements.txt
```

---

### Passo 4 — Configurar o banco de dados

Execute as migrações para criar as tabelas:

```bash
# 1. Gera a migration inicial do core (obrigatório primeiro, pois os outros dependem dele)
python manage.py makemigrations core

# 2. Gera as migrations dos demais apps
python manage.py makemigrations hipertensao
python manage.py makemigrations anticoagulacao

# 3. Aplica todas as migrations
python manage.py migrate
```

---

### Passo 5 — Criar o superusuário (administrador inicial)

```bash
python manage.py createsuperuser
```

Informe o nome de usuário, e-mail (opcional) e senha quando solicitado.

> Após o primeiro login, acesse **Gestão de Usuários** para cadastrar os demais profissionais com seus respectivos perfis (MED, ENF, NUT, FAR).

---

### Passo 6 — (Opcional) Carregar dados iniciais de medicamentos

Os dados de medicamentos são fornecidos no arquivo `medicamentos.toml`.
Para importá-los use o comando abaixo:

```bash
python manage.py load_medicamentos_toml medicamentos.toml
```

Use a flag `--atualizar` para sobrescrever registros já existentes no banco:

```bash
python manage.py load_medicamentos_toml medicamentos.toml --atualizar
```

> **Dependência de Python < 3.11:** instale `tomli` antes de executar o comando:
> ```bash
> pip install tomli
> ```
> Python 3.11+ já inclui suporte nativo a TOML (`tomllib`).

O arquivo `medicamentos.toml` segue a estrutura abaixo — edite-o para adicionar
ou ajustar entradas antes de importar:

```toml
[[medicamentos]]
classe           = "IECA"
principio_ativo  = "Enalapril"   # obrigatório
dose_padrao      = "10 mg"       # obrigatório
nomes_comerciais = "Renitec"
ativo            = true
is_remume        = true
```

---

### Passo 7 — Iniciar o servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse em: [http://localhost:8000](http://localhost:8000)

---

### Deploy em produção

Para ambientes de produção, recomenda-se:

**1. Configurar variáveis de ambiente sensíveis**

Edite `linhas_cuidado/settings.py` e substitua ou exporte via variável de ambiente:

```bash
export SECRET_KEY='sua-chave-secreta-longa-e-aleatória'
export DEBUG=False
export ALLOWED_HOSTS='seu-dominio.com.br,www.seu-dominio.com.br'
```

**2. Configurar banco de dados PostgreSQL (recomendado)**

Instale o driver:
```bash
pip install psycopg2-binary
```

Em `settings.py`, substitua a configuração de `DATABASES`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'linhas_cuidado',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**3. Coletar arquivos estáticos**

```bash
python manage.py collectstatic
```

**4. Usar Gunicorn como servidor WSGI**

```bash
pip install gunicorn
gunicorn linhas_cuidado.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

**5. Configurar Nginx como proxy reverso**

Exemplo de configuração básica (`/etc/nginx/sites-available/linhas_cuidado`):

```nginx
server {
    listen 80;
    server_name seu-dominio.com.br;

    location /static/ {
        alias /caminho/para/lca/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Ative o site:
```bash
sudo ln -s /etc/nginx/sites-available/linhas_cuidado /etc/nginx/sites-enabled/
sudo systemctl reload nginx
```

---

### Integração com API de Laboratório

O módulo de Hipertensão consulta resultados de exames em um serviço externo. Configure o endereço do servidor laboratorial em `hipertensao/views.py`:

```python
# Linha atual (padrão interno Caraguatatuba):
url = f"http://172.15.0.152:5897/api/laboratorio/{cpf}"
```

Substitua pelo endereço correto do serviço laboratorial da sua instituição.

---

## Estrutura do Projeto

```
lca/
├── manage.py
├── requirements.txt
├── medicamentos.toml        # Dados iniciais do banco de medicamentos
├── linhas_cuidado/          # Configuração do projeto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                    # Autenticação e gestão de usuários
│   ├── models.py            # Modelo Usuario customizado (RBAC multi-alçada)
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── decorators.py        # Controle de acesso por perfil
│   └── templates/
│       ├── base.html        # Layout base com navbar padrão
│       ├── login.html
│       ├── index.html
│       ├── trocar_senha.html
│       └── gestao_usuarios.html
├── hipertensao/             # Linha de cuidado HAS
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── decorators.py
│   ├── services_cid.py      # Mapeamento CID-10 → CID-11
│   ├── management/
│   │   └── commands/
│   │       └── load_medicamentos_toml.py  # Importação via TOML
│   └── templates/hipertensao/
│       └── sidebar.html     # Layout base da área HAS (navbar + conteúdo)
├── anticoagulacao/          # Linha de cuidado Anticoagulação
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── decorators.py
│   └── templates/anticoagulacao/
└── db.sqlite3               # Banco de dados (desenvolvimento)
```

---

## Licença

Desenvolvido para uso interno da Ambulatório Médico de Especialidades de Caraguatatuba. Para dúvidas ou contribuições, abra uma issue no repositório.
