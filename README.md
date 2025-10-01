# django-python

brandao
38312232

jose
Abc@1234567

FBV - functions base view
CBV - Class Base View

# Checklist Django com Explicações - Desenvolvimento & Code Review

## 🚀 Checklist Rápido para PRs

### ✅ Pré-Requisitos (Antes de Abrir PR)

- **Testes passando localmente** - Execute para garantir que não quebrou nada:
```bash
python manage.py test
```

- **Linting sem erros** - Use para manter código padronizado:
```bash
black .
flake8
isort .
```

- **Migrations criadas se necessário** - Quando alterar models:
```bash
python manage.py makemigrations
```

- **Documentation atualizada** - README, docstrings, comentários quando necessário

- **Título de PR descritivo** - Exemplo:
```
Add user authentication to API endpoints
```

- **Descrição explica WHAT e WHY** - O que mudou e por que foi necessário

- **Referência à issue/ticket** - Link para contexto completo:
```
#123, JIRA-456
```

- **Screenshots para UI** - Evidências visuais de mudanças na interface

- **Breaking changes documentadas** - Mudanças que podem quebrar código existente

### ✅ Durante o Code Review

- **Lógica de negócio correta** - Algoritmo resolve o problema proposto?
- **Performance considerations** - Vai escalar com mais dados/usuários?
- **Security implications** - Introduz vulnerabilidades?
- **Maintainability** - Outro dev consegue entender e modificar?
- **Backward compatibility** - Não quebra funcionalidades existentes?

## 🏗️ Arquitetura e Design

### ✅ Estrutura de Projeto

- **Apps com responsabilidade única** - Cada app faz UMA coisa bem feita:
```
users/
orders/
payments/
```

- **Nomes descritivos** - Usar nomes claros, plural quando apropriado:
```python
# ✅ Bom
user_profiles

# ❌ Ruim
profiles
```

- **Convenções Django** - Estrutura padrão:
```
app/
├── models.py
├── views.py
├── urls.py
├── admin.py
└── tests.py
```

- **`__init__.py` em pacotes** - Python precisa deles para reconhecer como módulos

- **Organização lógica** - Estrutura de diretórios:
```
project/
├── core/          # essencial
├── apps/          # negócio
└── utils/         # utilitários
```

- **Separação de responsabilidades** - Models = dados, Views = apresentação, Services = lógica

### ✅ Design Patterns

- **Service pattern** - Lógica complexa em classes Service ao invés de views "gordas":
```python
class UserService:
    @staticmethod
    def create_user_with_profile(email, name):
        # Lógica complexa aqui
        pass
```

- **Repository pattern** - Abstração da camada de dados quando necessário

- **Views lean** - Views apenas recebem request e retornam response

- **Business logic fora de views** - Regras de negócio em models/services

- **Managers customizados** - Queries complexas organizadas:
```python
User.objects.active()
```

- **Mixins reutilizáveis** - Funcionalidades comuns compartilhadas entre views

### ✅ Configurações (Settings)

- **Settings por ambiente** - Configurações específicas:
```python
# dev.py
DEBUG = True

# staging.py
DEBUG = False

# prod.py
DEBUG = False
```

- **Environment variables** - Senhas e configs em `.env`, não no código:
```python
# settings.py
SECRET_KEY = os.getenv('SECRET_KEY')
```

- **SECRET_KEY segura** - Nunca commitar, usar env var

- **DEBUG=False produção** - Evitar vazamento de informações em prod

- **ALLOWED_HOSTS** - Lista de domínios permitidos para segurança:
```python
ALLOWED_HOSTS = ['mysite.com', 'www.mysite.com']
```

- **Database URL env** - Conexão via variável para flexibilidade

- **Logs estruturados** - Configurar níveis e formatos de log

- **12-Factor App** - Metodologia para apps escaláveis (config, dependencies, etc.)

## 📊 Models e Database

### ✅ Design de Models

- **Nomenclatura CamelCase** - Para classes:
```python
# ✅ Bom
class UserProfile(models.Model):
    pass

# ❌ Ruim
class user_profile(models.Model):
    pass
```

- **help_text informativos**:
```python
email = models.EmailField(help_text="Used for password recovery")
```

- **verbose_name definidos** - Nomes amigáveis para admin/forms:
```python
class Meta:
    verbose_name = "User Profile"
    verbose_name_plural = "User Profiles"
```

- **`__str__` claro** - Para debug:
```python
def __str__(self):
    return f"{self.name} ({self.email})"
```

- **Meta ordering** - Ordem padrão:
```python
class Meta:
    ordering = ['-created_at']
```

- **on_delete explícito** - Nunca deixar implícito:
```python
user = models.ForeignKey(User, on_delete=models.CASCADE)
```

- **related_name** - Para queries reversas claras:
```python
user = models.ForeignKey(User, related_name='user_orders')
```

- **TextChoices** - Para escolhas:
```python
status = models.CharField(choices=StatusChoices.choices)
```

- **Validações no model** - Regras de negócio:
```python
def clean(self):
    if self.start_date > self.end_date:
        raise ValidationError('Start date must be before end date')
```

- **Constraints no DB** - Quando possível:
```python
class Meta:
    constraints = [
        models.UniqueConstraint(fields=['user', 'product'], name='unique_user_product')
    ]
```

### ✅ Migrations

- **Migrations atômicas** - Uma mudança por migration, reversíveis

- **Nomes descritivos**:
```bash
# ✅ Bom
0002_add_user_email_index.py

# ❌ Ruim
0002_auto_20231201_1234.py
```

- **Data vs Schema** - Migrations de dados separadas das de estrutura

- **Testar em staging** - Ambiente similar a produção antes do deploy

- **Backup antes** - Sempre! Especialmente para migrations grandes

- **Sem conflitos** - Resolver conflitos de migration antes do merge

### ✅ Performance e Otimização

- **`select_related()`** - Evita queries extras para ForeignKeys:
```python
posts = Post.objects.select_related('author')
```

- **`prefetch_related()`** - Para Many-to-Many:
```python
authors = Author.objects.prefetch_related('books')
```

- **Índices apropriados** - Em campos filtrados frequentemente:
```python
email = models.EmailField(db_index=True)
```

- **Evitar N+1** - 1 query inicial + N queries extras = problema de performance

- **`only()`/`defer()`** - Carregar apenas campos necessários:
```python
users = User.objects.only('name', 'email')
```

- **`update()` em massa**:
```python
User.objects.filter(active=True).update(last_seen=now)
```

- **`bulk_create()`** - Inserir muitos objetos de uma vez:
```python
User.objects.bulk_create([User(name='User1'), User(name='User2')])
```

- **F() expressions** - Operações no DB:
```python
Product.objects.update(price=F('price') * 1.1)
```

## 🎯 Views, APIs e Serializers

### ✅ Views

- **CBVs quando apropriado** - Reutilização e consistência vs simplicidade das FBVs

- **Métodos sobrescritos** - Customizados:
```python
def get_queryset(self):
    return super().get_queryset().filter(user=self.request.user)

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['extra_data'] = 'value'
    return context
```

- **Context bem estruturado** - Dados organizados para templates

- **Paginação para listas**:
```python
class PostListView(ListView):
    paginate_by = 25
```

- **Status codes corretos** - 200 (OK), 201 (Created), 400 (Bad Request), 404 (Not Found)

- **`get_object_or_404`** - Shortcut Django para erro 404 automático:
```python
user = get_object_or_404(User, pk=user_id)
```

### ✅ Django REST Framework

- **Serializers apropriados** - Um por endpoint, validações específicas:
```python
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name']
```

- **ViewSets quando útil** - Reduz código para CRUD completo:
```python
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

- **Filtering/ordering/pagination**:
```python
filter_backends = [DjangoFilterBackend, OrderingFilter]
pagination_class = StandardResultsSetPagination
```

- **Throttling para APIs públicas** - Rate limiting:
```python
throttle_classes = [AnonRateThrottle]
```

- **Versionamento** - URLs para compatibilidade:
```python
# urls.py
path('api/v1/', include('api.v1.urls')),
path('api/v2/', include('api.v2.urls')),
```

- **Response padronizado** - Formato consistente para erros e sucessos

- **Convenções REST** - GET/POST/PUT/DELETE seguindo padrões

### ✅ Validação e Serialização

- **Input validation** - Nunca confiar em dados do frontend

- **Validação customizada** - Methods nos serializers:
```python
def validate_email(self, value):
    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError("Email already exists")
    return value
```

- **Mensagens claras** - Erros compreensíveis para usuários/developers

- **Validação dupla** - Serializer E model para segurança

- **Serializers otimizados** - Evitar nested muito profundos (performance)

- **SerializerMethodField moderado** - Campos calculados podem ser lentos

## 🔒 Segurança

### ✅ Autenticação e Autorização

- **Permissions adequadas**:
```python
permission_classes = [IsAuthenticated, IsOwner]
```

- **Decorators corretos**:
```python
@login_required
@permission_required('app.change_model')
def my_view(request):
    pass
```

- **Permission classes API** - DRF permission system

- **Least Privilege** - Usuário só acessa o que precisa

- **Sessions seguras** - Timeout, secure cookies

- **Password validation** - Regras fortes para senhas

### ✅ Proteções Built-in

- **CSRF protection** - Token em forms, habilitado por padrão:
```html
{% csrf_token %}
```

- **SSL redirect produção** - Forçar HTTPS:
```python
SECURE_SSL_REDIRECT = True
```

- **HSTS headers** - Browser lembra de usar HTTPS:
```python
SECURE_HSTS_SECONDS = 31536000
```

- **Content-Type protection** - Previne MIME type confusion

- **X-Frame-Options** - Previne clickjacking

- **XSS Filter** - Proteção do browser ativada

- **CSP headers** - Content Security Policy quando necessário

### ✅ Validação e Sanitização

- **SQL injection prevenção** - ORM ao invés de SQL raw

- **XSS prevenção** - Auto-escape de templates Django

- **Upload validation** - Tipo, tamanho, conteúdo de arquivos:
```python
def validate_image(image):
    if image.size > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("Image too large")
```

- **URL validation** - Validar redirects para evitar phishing

- **Rate limiting** - Prevenir ataques de força bruta

- **Input sanitization** - Limpar/validar todos os inputs

## 📝 Qualidade de Código

### ✅ Padrões Python/Django

- **PEP 8 compliance** - Padrão oficial de estilo Python

- **Docstrings importantes** - Métodos complexos explicados:
```python
def calculate_tax(amount, rate):
    """
    Calculate tax for given amount and rate.
    
    Args:
        amount (Decimal): Base amount for tax calculation
        rate (Decimal): Tax rate as percentage (0.1 for 10%)
    
    Returns:
        Decimal: Calculated tax amount
    """
    return amount * rate
```

- **Type hints** - Para clareza:
```python
def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)
```

- **Nomes descritivos**:
```python
# ✅ Bom
def calculate_tax():
    pass

# ❌ Ruim
def calc_tx():
    pass
```

- **Imports organizados** - Stdlib, third-party, local separados:
```python
# Standard library
import os
import sys

# Third-party
import django
from rest_framework import serializers

# Local
from .models import User
```

- **Line length < 88-100** - Legibilidade em diferentes telas

- **Complexidade baixa** - Métodos curtos, uma responsabilidade

### ✅ Manutenibilidade

- **DRY principle** - Don't Repeat Yourself - código reutilizável

- **Baixo acoplamento** - Módulos independentes

- **Código auto-explicativo** - O código conta a história

- **Comentários "porquê"** - Explicar decisões, não o óbvio:
```python
# Using cache here because this query is expensive and called frequently
cached_result = cache.get(cache_key)
```

- **Sem código morto** - Remove prints, variáveis não usadas

- **Single Responsibility** - Uma função = uma responsabilidade

### ✅ Error Handling

- **Exceptions específicas**:
```python
# ✅ Bom
try:
    value = int(user_input)
except ValueError:
    handle_invalid_input()

# ❌ Ruim
try:
    value = int(user_input)
except:
    handle_error()
```

- **Logging adequado** - INFO para operações, ERROR para falhas:
```python
logger.info(f"User {user.id} logged in successfully")
logger.error(f"Failed to process payment for order {order.id}")
```

- **Custom exceptions** - Quando faz sentido:
```python
class InvalidUserError(Exception):
    pass
```

- **Graceful degradation** - Sistema funciona mesmo com falhas parciais

- **Logs sem dados sensíveis** - Nunca logar senhas, tokens

## 🧪 Testing

### ✅ Cobertura e Qualidade

- **Tests unitários** - Cada função/método testado isoladamente:
```python
def test_user_creation():
    user = User.objects.create(email='test@example.com')
    assert user.email == 'test@example.com'
```

- **Coverage > 80%** - Maioria do código coberto por testes:
```bash
coverage run --source='.' manage.py test
coverage report
```

- **Tests integração** - Fluxos completos funcionando:
```python
def test_user_registration_flow():
    response = self.client.post('/register/', {
        'email': 'test@example.com',
        'password': 'secure_password'
    })
    assert response.status_code == 201
    assert User.objects.filter(email='test@example.com').exists()
```

- **Tests independentes** - Ordem não importa, sem side effects

- **Factories > fixtures** - FactoryBoy mais flexível que fixtures JSON:
```python
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    email = factory.Faker('email')
    name = factory.Faker('name')
```

- **Mocking externo** - APIs externas mockadas para testes confiáveis:
```python
@mock.patch('requests.post')
def test_external_api_call(self, mock_post):
    mock_post.return_value.json.return_value = {'success': True}
    result = call_external_api()
    assert result['success'] is True
```

### ✅ Tipos e Organização

- **Unit tests** - Lógica isolada (models, utils, services)

- **Integration tests** - APIs, views, fluxos completos

- **Smoke tests** - Funcionalidades críticas sempre funcionando

- **Nomes descritivos**:
```python
def test_user_login_with_invalid_credentials():
    pass
```

- **Setup/teardown** - Preparação e limpeza adequadas:
```python
def setUp(self):
    self.user = User.objects.create(email='test@example.com')

def tearDown(self):
    User.objects.all().delete()
```

## ⚡ Performance e Escalabilidade

### ✅ Caching

- **Cache queries pesadas** - Resultados custosos em memória:
```python
def expensive_calculation():
    result = cache.get('expensive_result')
    if result is None:
        result = perform_calculation()
        cache.set('expensive_result', result, 3600)  # 1 hour
    return result
```

- **Template cache**:
```html
{% load cache %}
{% cache 500 sidebar request.user.id %}
    <!-- expensive sidebar content -->
{% endcache %}
```

- **Cache invalidation** - Estratégia para limpar cache desatualizado:
```python
def update_user(user_id, data):
    user = User.objects.get(id=user_id)
    user.update(data)
    cache.delete(f'user_{user_id}')
```

- **Redis/Memcached** - Backend de cache robusto:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

- **Cache keys bem nomeadas** - Estruturado:
```python
cache_key = f'user:{user.id}:profile'
```

- **Fragment caching** - Partes específicas de templates

### ✅ Otimizações

- **Static files otimizados** - CDN, compressão, versioning

- **Media uploads** - Resize, compressão automática

- **Gzip compression** - Reduz tamanho das responses:
```python
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    # ... other middleware
]
```

- **Connection pooling** - Reutilizar conexões DB

- **Lazy loading** - Carregar dados apenas quando necessário

- **CDN para assets** - Servir estáticos geograficamente próximo

### ✅ Background Tasks

- **Celery para tasks longas** - Email, relatórios, processamento:
```python
@shared_task
def send_email_task(user_id, subject, message):
    user = User.objects.get(id=user_id)
    send_mail(subject, message, 'from@example.com', [user.email])
```

- **Retry logic** - Tentar novamente em caso de falha:
```python
@shared_task(bind=True, max_retries=3)
def unreliable_task(self):
    try:
        # do something that might fail
        pass
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
```

- **Task monitoring** - Acompanhar execução e falhas

- **Idempotência** - Task pode executar múltiplas vezes sem problema

## 📦 Dependencies e Deploy

### ✅ Dependências

- **Requirements atualizados**:
```bash
pip freeze > requirements.txt
```

- **Versões pinned produção** - Específico:
```
Django==4.2.7
requests==2.31.0
```

- **Dev dependencies separadas**:
```
# requirements-dev.txt
pytest-django==4.7.0
black==23.11.0
flake8==6.1.0
```

- **Virtual environment** - Isolamento de dependências:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

- **Security audit** - Vulnerabilidades conhecidas:
```bash
pip install pip-audit
pip-audit
```

- **Cleanup dependencies** - Remove não utilizadas

### ✅ Deploy e DevOps

- **Health check endpoint** - Para monitoring:
```python
def health_check(request):
    return JsonResponse({'status': 'healthy', 'timestamp': timezone.now()})
```

- **Structured logging** - JSON logs para análise:
```python
LOGGING = {
    'version': 1,
    'formatters': {
        'json': {
            'format': '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
        }
    }
}
```

- **Monitoring/alertas** - Sentry, Datadog, etc.

- **Database backups** - Automatizados e testados

- **Environment vars documentadas**:
```bash
# .env.example
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgres://user:pass@localhost/dbname
DEBUG=True
```

- **CI/CD pipeline** - Deploy automatizado:
```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: python manage.py test
```

- **Rollback plan** - Como voltar versão anterior

## 🔧 Ferramentas e Setup

### ✅ Code Quality Tools

- **Black** - Formatação automática consistente:
```bash
black --line-length 88 .
```

- **Flake8** - Detecta erros de sintaxe e estilo:
```bash
flake8 --max-line-length 88
```

- **isort** - Organiza imports alfabeticamente:
```bash
isort --profile black .
```

- **mypy** - Verificação de tipos estáticos:
```bash
mypy --install-types --non-interactive .
```

- **bandit** - Detecta vulnerabilidades de segurança:
```bash
bandit -r .
```

- **pre-commit** - Executa checks antes do commit:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
```

### ✅ Testing & Development

- **pytest** - Framework de testes mais poderoso:
```bash
pytest --cov=. --cov-report=html
```

- **factory-boy** - Cria dados de teste facilmente:
```python
user = UserFactory(email='specific@email.com')
```

- **coverage.py** - Mede cobertura de testes:
```bash
coverage run --source='.' manage.py test
coverage html
```

- **django-debug-toolbar** - Debug no browser:
```python
INSTALLED_APPS = [
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
```

- **django-extensions** - Comandos úteis extras:
```bash
python manage.py show_urls
python manage.py shell_plus
```

- **django-environ** - Gerencia environment variables:
```python
import environ
env = environ.Env()
SECRET_KEY = env('SECRET_KEY')
```

## 📚 Documentação e Observabilidade

### ✅ Documentação

- **README completo** - Setup, requirements, como rodar:
```markdown
# Project Name

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Start server: `python manage.py runserver`

## Environment Variables
- SECRET_KEY: Django secret key
- DATABASE_URL: Database connection string
```

- **API docs** - Swagger/OpenAPI automático com DRF:
```python
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```

- **Changelog** - Log de mudanças versionado:
```markdown
# Changelog

## [1.2.0] - 2023-12-01
### Added
- User authentication system
### Changed
- Updated Django to 4.2.7
### Fixed
- Fixed email validation bug
```

- **ADRs** - Architecture Decision Records para decisões importantes

- **Inline docs** - Docstrings para código complexo

### ✅ Monitoring

- **APM tools** - New Relic, Datadog para performance

- **Error tracking** - Sentry para exceptions em produção:
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
)
```

- **Query monitoring** - Slow queries, N+1 detection

- **Business metrics** - KPIs importantes do negócio

- **Structured logs** - JSON format para parsing

- **Alertas críticos** - Notificações para problemas graves

## 🚨 Anti-Patterns (EVITAR)

### 🔴 Nunca Fazer

- **Business logic em views** - Views devem ser simples:
```python
# ❌ Ruim
def create_order(request):
    # 50 linhas de lógica complexa aqui
    pass

# ✅ Bom
def create_order(request):
    order = OrderService.create_order(request.data)
    return JsonResponse({'id': order.id})
```

- **N+1 queries não tratadas** - Performance killer:
```python
# ❌ Ruim
for post in posts:
    print(post.author.name)  # Nova query para cada post

# ✅ Bom
posts = Post.objects.select_related('author')
for post in posts:
    print(post.author.name)
```

- **Bare except** - Pega tudo, mascarando erros:
```python
# ❌ Ruim
try:
    risky_operation()
except:
    pass

# ✅ Bom
try:
    risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
```

- **Hardcoded values** - Magic numbers/strings no código:
```python
# ❌ Ruim
if user.age > 18:
    pass

# ✅ Bom
MINIMUM_AGE = 18
if user.age > MINIMUM_AGE:
    pass
```

- **Complex signals** - Side effects invisíveis e difíceis de debug

- **Memory leaks** - Objetos não liberados da memória

- **Overengineering** - Complexidade desnecessária

### 🟡 Cuidado Especial

- **Large querysets sem paginação** - Pode quebrar com muitos dados:
```python
# ❌ Cuidado
all_users = User.objects.all()  # Pode ser milhões

# ✅ Bom
users = User.objects.all()[:100]  # Limite
```

- **Deep nested serializers** - Performance ruim

- **Complex template logic** - Lógica deve estar nas views

- **Loops com queries** - Cada iteração = nova query

- **Missing indexes** - Queries lentas sem índices

## 💡 Princípios Fundamentais

### 🎯 Escalabilidade First
Pense: "E se tiver 100x mais usuários?"

### 🔒 Security by Design
Segurança desde o início, não depois

### 🧪 Tests são Investimento
Previnem bugs caros em produção

### 🏗️ Keep It Simple
Complexidade é inimiga da manutenibilidade

### 📖 Document Decisions
Próximo dev (ou você) vai agradecer

### ⚡ Fail Fast
Detecte problemas cedo no desenvolvimento

### 📊 Measure Everything
Métricas guiam melhorias

## ⚙️ CI/CD Pipeline Essencial

### Pipeline Básico

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
          
      - name: Run linting
        run: |
          flake8 .
          black --check .
          isort --check-only .
          
      - name: Run security scan
        run: bandit -r .
        
      - name: Run tests
        run: |
          python manage.py test
          coverage run --source='.' manage.py test
          coverage report --fail-under=80
          
      - name: Deploy to staging
        if: github.ref == 'refs/heads/develop'
        run: |
          # Deploy commands here
          echo "Deploying to staging..."
          
      - name: Deploy to production
        if: github.ref == 'refs/heads/main'
        run: |
          # Production deploy commands
          echo "Deploying to production..."
          
      - name: Smoke tests production
        if: github.ref == 'refs/heads/main'
        run: |
          # Basic health checks
          curl -