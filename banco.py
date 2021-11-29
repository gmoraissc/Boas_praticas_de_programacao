class ContaCorrente:

  def __init__(self, numero, titular, saldo, limite): # atributos # init -> construtora
    
    self.__numero = numero # métodos # __ -> dunder, privado, encapsulamento
    self.__titular = titular
    self.__saldo = saldo
    self.__limite = limite

  def extrato(self):

    return self.__titular, self.__saldo

  def deposito(self, valor_deposito):

    self.__saldo += valor_deposito

  def saque_disponivel(self, valor_a_sacar):
    valor_disponivel_a_sacar = self.__saldo + self.__limite
    return valor_a_sacar <= valor_disponivel_a_sacar

  def saque(self, valor_saque):
    if (self.saque_disponivel(valor_saque)):
      self.__saldo -= valor_saque
    
    else:
      valor_disponivel_a_sacar = self.__saldo + self.__limite
      diferenca_saque = valor_saque - (valor_disponivel_a_sacar)
      return f'Saldo ultrapassa o limite em {diferenca_saque}'

  def transferencia(self, valor_transferencia, destino):

    self.saque(valor_transferencia)
    destino.deposito(valor_transferencia)

  @property
  def saldo(self):# getter e setter, criados para fazer algo com o objeto criado!

    return self.__saldo
  
  @property
  def titular(self):

    return self.__titular
  
  @property #propriedades, usada para getters e setters
  def limite(self):

    return self.__limite
  
  @limite.setter
  def limite(self, novo_limite):

    self.__limite = novo_limite

  @staticmethod
  def codigos_bancos():
    return {'BB': '001', 'Caixa': '104', 'Bradesco': '237'}
    
  
  class Programa:

  def __init__(self, nome, ano):
    self.__nome = nome.capitalize()
    self.__ano = ano
    self.__likes = 0

  @property
  def likes(self):
    return self.__likes

  def like(self):
    self.__likes += 1

  def __str__(self):
    return self.__nome, self.__ano, self.__likes

class Filmes(Programa):

    def __init__(self, nome, ano, duracao):
      super().__init__(nome, ano)      
      self.__duracao = duracao
    
    def __str__(self):
      return self.__nome, self.__ano, self.__likes, self.__duracao

class Series(Programa):

    def __init__(self, nome, ano, temporadas):
      super().__init__(nome, ano)
      self.__temporadas = temporadas
    
    def __str__(self):
      return self.__nome, self.__ano, self.__likes, self.__temporadas
  
class Playlist:

    def __init__(self, nome, programas):
      self.__programas = programas
      self.__nome = nome
    
    def __getitem__(self, item): #magic methods, transforma objeto em iterável (Duck Typing = comportamento como...)
      return self.__programas[item]
    
    def __len__(self):
      return len(self.__programas)
