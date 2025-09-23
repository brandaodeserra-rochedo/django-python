# EXEMPLO DIDÁTICO: ORIENTAÇÃO A OBJETOS E PRINCÍPIOS SOLID
# Sistema de Gerenciamento de Funcionários

from abc import ABC, abstractmethod
from typing import List, Protocol
import json

# ============================================================================
# 1. CONCEITOS BÁSICOS DE OOP
# ============================================================================

class Pessoa:
    """
    CLASSE BASE demonstrando ENCAPSULAMENTO
    - Atributos privados (__nome) 
    - Métodos públicos para acesso controlado (@property)
    """
    
    def __init__(self, nome: str, idade: int, cpf: str):
        # __init__ = MÉTODO CONSTRUTOR
        #- Chamado automaticamente quando criamos um objeto: pessoa = Pessoa("João", 25, "123...")
        #- 'self' = referência ao próprio objeto (como 'this' em outras linguagens)
        #- Parâmetros com type hints (: str, : int) = indica o tipo esperado
        
        self.__nome = nome      # __ (duplo underscore) = ATRIBUTO PRIVADO (name mangling)
        self.__idade = idade    # Python transforma __nome em _Pessoa__nome internamente
        self.__cpf = cpf        # Não pode ser acessado diretamente de fora da classe
      
    
    # Métodos públicos (getters/setters)
    @property
    def nome(self) -> str: # -> str = TYPE HINT de retorno (indica que retorna string)
        return self.__nome
    
    @property 
    def idade(self) -> int:
        return self.__idade
    
    @property
    def cpf(self) -> str:
        return self.__cpf
    
    def __str__(self) -> str:
        # __str__ = MÉTODO ESPECIAL (dunder method)
        #- Chamado automaticamente por str() e print()
        #- Define como o objeto é representado como string
        return f"Nome: {self.__nome}, Idade: {self.__idade}"

# ============================================================================
# 2. HERANÇA E POLIMORFISMO
# ============================================================================

class Funcionario(Pessoa):
    """
    HERANÇA: Funcionario herda de Pessoa
    Demonstra reutilização de código
    """
    
    def __init__(self, nome: str, idade: int, cpf: str, salario: float, cargo: str):
        super().__init__(nome, idade, cpf)  # Chama construtor da classe pai : super() = acessa a classe pai (Pessoa)
        self.__salario = salario
        self.__cargo = cargo
    
    @property
    def salario(self) -> float:
        return self.__salario
    
    @property
    def cargo(self) -> str:
        return self.__cargo
    
    # POLIMORFISMO: Método pode ser sobrescrito nas classes filhas
    def calcular_bonus(self) -> float:
        """Método base para cálculo de bônus"""
        return self.__salario * 0.1
    
    def __str__(self) -> str:
        return f"{super().__str__()}, Cargo: {self.__cargo}, Salário: R${self.__salario:.2f}"

# ============================================================================
# 3. PRINCÍPIOS SOLID
# ============================================================================

# SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# Cada classe tem uma única responsabilidade

class Desenvolvedor(Funcionario):
    """Responsabilidade: Gerenciar desenvolvedores"""
    
    def __init__(self, nome: str, idade: int, cpf: str, salario: float, linguagens: List[str]):
        super().__init__(nome, idade, cpf, salario, "Desenvolvedor")
        self.__linguagens = linguagens
    
    @property
    def linguagens(self) -> List[str]:
        return self.__linguagens.copy()
    
    def calcular_bonus(self) -> float:
        """Bônus baseado no número de linguagens"""
        bonus_base = super().calcular_bonus()
        bonus_linguagens = len(self.__linguagens) * 500
        return bonus_base + bonus_linguagens

class Gerente(Funcionario):
    """Responsabilidade: Gerenciar gerentes"""
    
    def __init__(self, nome: str, idade: int, cpf: str, salario: float, equipe_size: int):
        super().__init__(nome, idade, cpf, salario, "Gerente")
        self.__equipe_size = equipe_size
    
    @property
    def equipe_size(self) -> int:
        return self.__equipe_size
    
    def calcular_bonus(self) -> float:
        """Bônus baseado no tamanho da equipe"""
        bonus_base = super().calcular_bonus()
        bonus_equipe = self.__equipe_size * 1000
        return bonus_base + bonus_equipe

# OPEN/CLOSED PRINCIPLE (OCP)
# Aberto para extensão, fechado para modificação

class Estagiario(Funcionario):
    """Nova classe pode ser adicionada sem modificar código existente"""
    
    def __init__(self, nome: str, idade: int, cpf: str, salario: float, periodo: str):
        super().__init__(nome, idade, cpf, salario, "Estagiário")
        self.__periodo = periodo
    
    @property
    def periodo(self) -> str:
        return self.__periodo
    
    def calcular_bonus(self) -> float:
        """Estagiários têm bônus fixo menor"""
        return 500.0

# LISKOV SUBSTITUTION PRINCIPLE (LSP)
# Objetos de classes derivadas devem poder substituir objetos da classe base

def processar_funcionario(funcionario: Funcionario) -> dict:
    """
    Esta função funciona com qualquer subclasse de Funcionario
    sem precisar conhecer o tipo específico (LSP)
    """
    return {
        'nome': funcionario.nome,
        'cargo': funcionario.cargo,
        'salario': funcionario.salario,
        'bonus': funcionario.calcular_bonus()
    }

# INTERFACE SEGREGATION PRINCIPLE (ISP)
# Interfaces específicas são melhores que interfaces genéricas

# OPÇÃO 1: Usando ABC (Abstract Base Class)
class RelatorioABC(ABC):
    """Classe abstrata para geração de relatórios usando ABC"""
    
    # ABC: Classe abstrata que DEVE ser herdada
    #- Não pode ser instanciada diretamente
    #- Classes filhas DEVEM implementar métodos @abstractmethod

    @abstractmethod
    def gerar_relatorio(self, funcionarios: List[Funcionario]) -> str:
        """Método abstrato que deve ser implementado pelas classes filhas"""
        pass

# OPÇÃO 2: Usando Protocol (mais flexível, sem herança obrigatória)
class Relatorio(Protocol):
    """Interface para geração de relatórios usando Protocol"""
    def gerar_relatorio(self, funcionarios: List[Funcionario]) -> str:
        ...

class Persistencia(Protocol):
    """Interface para persistência de dados"""
    def salvar(self, dados: dict) -> bool:
        ...
    
    def carregar(self) -> dict:
        ...

# DEPENDENCY INVERSION PRINCIPLE (DIP)
# Depender de abstrações, não de implementações concretas

# Implementação usando ABC (deve herdar obrigatoriamente)
class RelatorioJSONComABC(RelatorioABC):
    """Implementação concreta de relatório em JSON herdando de ABC"""
    
    def gerar_relatorio(self, funcionarios: List[Funcionario]) -> str:
        dados = []
        for func in funcionarios:
            dados.append(processar_funcionario(func))
        return json.dumps(dados, indent=2, ensure_ascii=False)

# Implementação usando Protocol (sem herança obrigatória)
class RelatorioJSON:
    """Implementação concreta de relatório em JSON (usa Protocol implicitamente)"""
    
    def gerar_relatorio(self, funcionarios: List[Funcionario]) -> str:
        dados = []
        for func in funcionarios:
            dados.append(processar_funcionario(func))
        return json.dumps(dados, indent=2, ensure_ascii=False)

class RelatorioTexto:
    """Implementação concreta de relatório em texto"""
    
    def gerar_relatorio(self, funcionarios: List[Funcionario]) -> str:
        relatorio = "=== RELATÓRIO DE FUNCIONÁRIOS ===\n\n"
        for func in funcionarios:
            info = processar_funcionario(func)
            relatorio += f"• {info['nome']} ({info['cargo']})\n"
            relatorio += f"  Salário: R${info['salario']:.2f}\n"
            relatorio += f"  Bônus: R${info['bonus']:.2f}\n\n"
        return relatorio

class GerenciadorFuncionarios:
    """
    DEPENDENCY INVERSION: Esta classe depende de abstrações (Protocols)
    não de implementações concretas
    """
    
    def __init__(self, gerador_relatorio: Relatorio):
        self.__funcionarios: List[Funcionario] = []
        self.__gerador_relatorio = gerador_relatorio
    
    def adicionar_funcionario(self, funcionario: Funcionario) -> None:
        self.__funcionarios.append(funcionario)
    
    def listar_funcionarios(self) -> List[Funcionario]:
        return self.__funcionarios.copy()
    
    def gerar_relatorio(self) -> str:
        return self.__gerador_relatorio.gerar_relatorio(self.__funcionarios)
    
    def calcular_folha_pagamento(self) -> float:
        """Calcula o total da folha de pagamento incluindo bônus"""
        total = 0
        for func in self.__funcionarios:
            total += func.salario + func.calcular_bonus()
        return total

# ============================================================================
# 4. EXEMPLO DE USO PRÁTICO
# ============================================================================

def exemplo_pratico():
    """Demonstra o uso de todos os conceitos implementados"""
    
    print("🏢 SISTEMA DE GERENCIAMENTO DE FUNCIONÁRIOS")
    print("=" * 50)
    
    # Criando funcionários (POLIMORFISMO em ação)
    dev1 = Desenvolvedor("Ana Silva", 28, "123.456.789-01", 8000, ["Python", "JavaScript", "React"])
    dev2 = Desenvolvedor("Carlos Santos", 32, "987.654.321-02", 9500, ["Java", "Spring", "Docker"])
    gerente1 = Gerente("Maria Oliveira", 35, "456.789.123-03", 12000, 5)
    estagiario1 = Estagiario("João Costa", 22, "321.654.987-04", 2000, "Matutino")
    
    # DEPENDENCY INJECTION: Podemos escolher diferentes tipos de relatório
    gerador_json = RelatorioJSON()
    gerador_texto = RelatorioTexto()
    gerador_json_abc = RelatorioJSONComABC()  # Versão com ABC
    
    # Demonstrando que ambas as abordagens funcionam
    print("🔧 TESTANDO ABC vs PROTOCOL:")
    print("ABC requer herança:", isinstance(gerador_json_abc, RelatorioABC))
    print("Protocol funciona por 'duck typing':", hasattr(gerador_json, 'gerar_relatorio'))
    print()
    
    # Criando gerenciador com relatório em texto
    gerenciador = GerenciadorFuncionarios(gerador_texto)
    
    # Adicionando funcionários
    funcionarios = [dev1, dev2, gerente1, estagiario1]
    for func in funcionarios:
        gerenciador.adicionar_funcionario(func)
    
    # Gerando relatório
    print("📋 RELATÓRIO EM TEXTO:")
    print(gerenciador.gerar_relatorio())
    
    # Calculando folha de pagamento
    total_folha = gerenciador.calcular_folha_pagamento()
    print(f"💰 TOTAL DA FOLHA DE PAGAMENTO: R${total_folha:.2f}")
    
    # Mudando para relatório JSON (DIP em ação)
    gerenciador_json = GerenciadorFuncionarios(gerador_json)
    for func in funcionarios:
        gerenciador_json.adicionar_funcionario(func)
    
    print("\n" + "=" * 50)
    print("📋 MESMO RELATÓRIO EM JSON:")
    print(gerenciador_json.gerar_relatorio())

# Executar exemplo
if __name__ == "__main__":
    exemplo_pratico()

# ============================================================================
# RESUMO DOS CONCEITOS DEMONSTRADOS:
# ============================================================================

"""
🎯 ORIENTAÇÃO A OBJETOS:

1. ENCAPSULAMENTO:
   - Atributos privados (__nome, __salario)
   - Acesso controlado via properties
   - Proteção da integridade dos dados

2. HERANÇA:
   - Pessoa → Funcionario → Desenvolvedor/Gerente/Estagiario
   - Reutilização de código
   - Extensão de funcionalidades

3. POLIMORFISMO:
   - Método calcular_bonus() implementado diferentemente em cada classe
   - Mesma interface, comportamentos diferentes

4. ABSTRAÇÃO:
   - ABC e Protocols definem contratos
   - Classes escondem complexidade interna

🏗️ PRINCÍPIOS SOLID:

1. SRP - Single Responsibility:
   - Cada classe tem uma responsabilidade específica
   - Desenvolvedor, Gerente, Estagiario são classes separadas

2. OCP - Open/Closed:
   - Podemos adicionar novos tipos de funcionário sem modificar código existente
   - Estagiario foi adicionado facilmente

3. LSP - Liskov Substitution:
   - Qualquer subclasse de Funcionario pode ser usada onde Funcionario é esperado
   - processar_funcionario() funciona com todos os tipos

4. ISP - Interface Segregation:
   - Interfaces pequenas e específicas (Relatorio, Persistencia)
   - Classes implementam apenas o que precisam

5. DIP - Dependency Inversion:
   - GerenciadorFuncionarios depende da abstração Relatorio
   - Não depende de implementações concretas
   - Facilita testes e manutenção

🆚 ABC vs PROTOCOL:

ABC (Abstract Base Class):
- Herança obrigatória (RelatorioJSONComABC DEVE herdar de RelatorioABC)
- Métodos @abstractmethod devem ser implementados
- Verificação em tempo de instanciação

Protocol:
- "Duck typing" - se tem o método, funciona
- Não precisa herdar (RelatorioJSON funciona sem herdar)
- Verificação via type hints
- Mais flexível, menos rígido
"""