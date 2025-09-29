# Guia Simples do manage.py - Django

## 🎯 O que é o manage.py?

O `manage.py` é o **comando central** do Django que permite executar tarefas administrativas no seu projeto. Ele é criado automaticamente quando você inicia um projeto Django.

## 📋 Comandos Essenciais

### 🚀 Iniciar o Servidor de Desenvolvimento

```bash
python manage.py runserver
```

**O que faz:** Inicia o servidor local na porta 8000 (http://localhost:8000)

**Variações:**
```bash
# Porta customizada
python manage.py runserver 8080

# Permitir acesso de outras máquinas
python manage.py runserver 0.0.0.0:8000
```

---

### 🗄️ Migrations (Banco de Dados)

#### Criar migrations
```bash
python manage.py makemigrations
```
**O que faz:** Detecta mudanças nos models e cria arquivos de migração

**Exemplo:**
```bash
# Para um app específico
python manage.py makemigrations users

# Ver o SQL que será executado
python manage.py sqlmigrate users 0001
```

#### Aplicar migrations
```bash
python manage.py migrate
```
**O que faz:** Aplica as migrations no banco de dados (cria/modifica tabelas)

**Exemplo:**
```bash
# Migrar app específico
python manage.py migrate users

# Voltar para migration específica
python manage.py migrate users 0002
```

#### Ver status das migrations
```bash
python manage.py showmigrations
```
**O que faz:** Mostra quais migrations foram aplicadas

---

### 👤 Usuários e Admin

#### Criar superusuário
```bash
python manage.py createsuperuser
```
**O que faz:** Cria um usuário administrador para acessar o Django Admin (/admin)

**Interativo:**
```
Username: admin
Email: admin@example.com
Password: ********
```

#### Alterar senha
```bash
python manage.py changepassword username
```

---

### 🐚 Shell Interativo

#### Shell padrão
```bash
python manage.py shell
```
**O que faz:** Abre um console Python com o Django carregado

**Exemplo de uso:**
```python
>>> from users.models import User
>>> User.objects.all()
>>> user = User.objects.create(name='João', email='joao@example.com')
>>> user.save()
```

#### Shell Plus (django-extensions)
```bash
python manage.py shell_plus
```
**O que faz:** Shell com auto-import dos models

---

### 🧪 Testes

#### Executar todos os testes
```bash
python manage.py test
```

#### Testar app específico
```bash
python manage.py test users
```

#### Testar classe ou método específico
```bash
# Classe específica
python manage.py test users.tests.UserModelTest

# Método específico
python manage.py test users.tests.UserModelTest.test_user_creation
```

#### Com cobertura
```bash
coverage run --source='.' manage.py test
coverage report
```

---

### 📁 Arquivos Estáticos

#### Coletar arquivos estáticos
```bash
python manage.py collectstatic
```
**O que faz:** Copia todos os arquivos estáticos (CSS, JS, imagens) para um único diretório configurado em `STATIC_ROOT`

**Uso:** Necessário antes de fazer deploy em produção

---

### 🗑️ Limpeza e Manutenção

#### Limpar sessões expiradas
```bash
python manage.py clearsessions
```

#### Limpar cache
```bash
python manage.py clear_cache
```

---

### 🔍 Inspeção e Debug

#### Ver todas as URLs
```bash
python manage.py show_urls  # django-extensions
```

#### Verificar problemas no projeto
```bash
python manage.py check
```
**O que faz:** Verifica erros de configuração, migrations pendentes, etc.

**Específico:**
```bash
# Verificar apenas models
python manage.py check --tag models

# Verificar deploy
python manage.py check --deploy
```

#### Ver estrutura do banco
```bash
python manage.py dbshell
```
**O que faz:** Abre o shell do banco de dados (SQLite, PostgreSQL, etc.)

---

### 📊 Dados e Database

#### Exportar dados (fixtures)
```bash
python manage.py dumpdata > data.json
```

**Específico:**
```bash
# App específico
python manage.py dumpdata users > users.json

# Model específico
python manage.py dumpdata users.User > users.json

# Formato indentado
python manage.py dumpdata users --indent 2 > users.json
```

#### Importar dados
```bash
python manage.py loaddata data.json
```

#### Flush (limpar banco)
```bash
python manage.py flush
```
**⚠️ CUIDADO:** Remove todos os dados do banco!

---

## 🎨 Comandos Úteis (django-extensions)

### Graph Models (diagrama ER)
```bash
python manage.py graph_models -a -o models.png
```

### Executar script Python
```bash
python manage.py runscript nome_do_script
```

### Ver URLs de forma legível
```bash
python manage.py show_urls
```

---

## 🛠️ Criar Comandos Customizados

### Estrutura
```
myapp/
└── management/
    └── commands/
        └── meu_comando.py
```

### Exemplo de comando customizado

```python
# myapp/management/commands/meu_comando.py
from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Descrição do que o comando faz'

    def add_arguments(self, parser):
        # Adicionar argumentos opcionais
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete inactive users',
        )

    def handle(self, *args, **options):
        # Lógica do comando
        if options['delete']:
            deleted = User.objects.filter(is_active=False).delete()
            self.stdout.write(
                self.style.SUCCESS(f'Deleted {deleted[0]} users')
            )
        else:
            count = User.objects.filter(is_active=False).count()
            self.stdout.write(f'Found {count} inactive users')
```

### Usar o comando
```bash
python manage.py meu_comando
python manage.py meu_comando --delete
```

---

## 📝 Dicas e Boas Práticas

### 1. Ver ajuda de qualquer comando
```bash
python manage.py help
python manage.py help migrate
python manage.py migrate --help
```

### 2. Modo verboso
```bash
python manage.py migrate --verbosity 2
# Níveis: 0 (mínimo), 1 (normal), 2 (detalhado), 3 (muito detalhado)
```

### 3. Configuração específica
```bash
python manage.py runserver --settings=myproject.settings.dev
```

### 4. Ver versão do Django
```bash
python manage.py --version
```

### 5. Dry run (simular sem executar)
```bash
python manage.py migrate --plan
python manage.py collectstatic --dry-run
```

---

## ⚙️ Workflow Típico de Desenvolvimento

### Início do dia
```bash
# 1. Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 2. Aplicar migrations
python manage.py migrate

# 3. Iniciar servidor
python manage.py runserver
```

### Após alterar models
```bash
# 1. Criar migration
python manage.py makemigrations

# 2. Verificar SQL
python manage.py sqlmigrate app_name 0001

# 3. Aplicar migration
python manage.py migrate

# 4. Testar
python manage.py test
```

### Antes de commit
```bash
# 1. Verificar problemas
python manage.py check

# 2. Rodar testes
python manage.py test

# 3. Verificar cobertura
coverage run --source='.' manage.py test
coverage report
```

### Deploy
```bash
# 1. Coletar estáticos
python manage.py collectstatic --noinput

# 2. Aplicar migrations
python manage.py migrate

# 3. Verificar configuração de produção
python manage.py check --deploy
```

---

## 🚨 Comandos Perigosos (Use com Cuidado!)

### ⚠️ Flush - Limpa TODOS os dados
```bash
python manage.py flush
```

### ⚠️ Migrate zero - Desfaz todas migrations
```bash
python manage.py migrate app_name zero
```

### ⚠️ DBShell - Acesso direto ao banco
```bash
python manage.py dbshell
# DROP TABLE users;  # 💀 Muito perigoso!
```

---

## 💡 Comandos por Categoria

### 🏗️ Estrutura e Setup
```bash
startproject    # Criar novo projeto
startapp        # Criar novo app
check           # Verificar problemas
```

### 🗄️ Banco de Dados
```bash
makemigrations  # Criar migrations
migrate         # Aplicar migrations
showmigrations  # Status das migrations
sqlmigrate      # Ver SQL da migration
dbshell         # Shell do banco
```

### 👥 Usuários
```bash
createsuperuser    # Criar admin
changepassword     # Alterar senha
```

### 🧪 Desenvolvimento
```bash
runserver       # Servidor local
shell           # Console Python
test            # Executar testes
```

### 📦 Deploy
```bash
collectstatic   # Coletar arquivos estáticos
check --deploy  # Verificar config produção
```

### 🔧 Manutenção
```bash
clearsessions   # Limpar sessões
flush           # Limpar banco
dumpdata        # Exportar dados
loaddata        # Importar dados
```

---

## 📚 Recursos Adicionais

### Documentação Oficial
```
https://docs.djangoproject.com/en/stable/ref/django-admin/
```

### Django Extensions
```bash
pip install django-extensions
```
Adiciona comandos úteis extras como `shell_plus`, `show_urls`, `graph_models`

### Principais comandos do django-extensions
```bash
shell_plus           # Shell com auto-import
show_urls            # Lista todas URLs
graph_models         # Diagrama ER dos models
runscript            # Executar scripts
reset_db             # Resetar banco
export_emails        # Exportar emails
```

---

## 🎓 Resumo Rápido - Top 10 Comandos

```bash
# 1. Iniciar servidor
python manage.py runserver

# 2. Criar migrations
python manage.py makemigrations

# 3. Aplicar migrations
python manage.py migrate

# 4. Criar superusuário
python manage.py createsuperuser

# 5. Shell interativo
python manage.py shell

# 6. Executar testes
python manage.py test

# 7. Coletar estáticos
python manage.py collectstatic

# 8. Verificar problemas
python manage.py check

# 9. Ver ajuda
python manage.py help

# 10. Ver versão
python manage.py --version
```

---

## 🔑 Conclusão

O `manage.py` é sua ferramenta principal para:
- ✅ Gerenciar banco de dados (migrations)
- ✅ Rodar servidor de desenvolvimento
- ✅ Executar testes
- ✅ Administrar usuários
- ✅ Debug e inspeção
- ✅ Deploy e produção

**Dica Final:** Use `python manage.py help` sempre que tiver dúvidas sobre um comando!