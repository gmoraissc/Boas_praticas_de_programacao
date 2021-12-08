class Descontos(object):

  def __init__(self, proximo_desconto):

    self.__proximo_desconto = proximo_desconto
    
class Desconto_por_item(object):
  
  def __init__(self, proximo_desconto):

    self.__proximo_desconto = proximo_desconto
  
  def calcula(self, orcamento):
    if orcamento.total_items > 5:
      return orcamento.valor * 0.1
    else:
      return self.__proximo_desconto.calcula(orcamento)

class Desconto_500_reais(object):

  def __init__(self, proximo_desconto):

    self.__proximo_desconto = proximo_desconto

  def calcula(self, orcamento):

    if orcamento.valor > 500:
      return orcamento.valor * 0.07
    else:
      return self.__proximo_desconto.calcula(orcamento)

class Sem_desconto(object):
    
    def calcula(self):
      return 0
  
class Calculador_de_descontos(object):
  #cadeia de responsabilidades
  def calcula(self, orcamento):

    desconto = Desconto_por_item(
        Desconto_500_reais(Sem_desconto) #seria necessario instanciar a classe caso fosse importada de um módulo
    ).calcula(orcamento)

    return round(desconto, 4)

  
 from abc import ABCMeta, abstractmethod

class Status_Orcamento(object):

  __metaclass__ = ABCMeta
  
  @abstractmethod
  def aplica_desconto_extra(self, orcamento):
    pass

  @abstractmethod
  def aprova(self, orcamento):
    pass
  
  @abstractmethod
  def reprova(self, orcamento):
    pass

  @abstractmethod
  def finaliza(self, orcamento):
    pass
  

class Em_aprovacao(Status_Orcamento):

  def aplica_desconto_extra(self, orcamento):
    
    return orcamento.adiciona_desconto_extra(orcamento.valor * 0.02)

  def aprova(self, orcamento):
    orcamento.estado_atual = Aprovado()
  
  def reprova(self, orcamento):
    orcamento.estado_atual = Reprovado()
  
  def finaliza(self, orcamento):
    raise Exception('Orcamentos em aprovacao nao podem ser finalizados sem serem antes avaliados')

class Aprovado(Status_Orcamento):

  def aplica_desconto_extra(self, orcamento):
    
    return orcamento.adiciona_desconto_extra(orcamento.valor * 0.05)

  def aprova(self, orcamento):
    raise Exception('Orcamento ja aprovado anteriormente')
  
  def reprova(self, orcamento):
    raise Exception('Orcamento aprovado nao pode ser reprovado')
  
  def finaliza(self, orcamento):
    oracamento.estado_atual = Finalizado()

class Reprovado(Status_Orcamento):

  def aplica_desconto_extra(self, orcamento):
    
    raise Exception('Orcamento reprovado não receberá desconto extra')

  def aprova(self, orcamento):
    raise Exception('Orcamento reprovado não pode ser aprovado')
  
  def reprova(self, orcamento):
    raise Exception('Orcamento ja reprovado anteriormente')
  
  def finaliza(self, orcamento):
    oracamento.estado_atual = Finalizado()

class Finalizado(Status_Orcamento):

  def aplica_desconto_extra(self, orcamento):
    
    raise Exception('Orcamento finalizado não receberá desconto extra')

  def aprova(self, orcamento):
    raise Exception('Orcamento finalizado não pode ser aprovado')
  
  def reprovado(self, orcamento):
    raise Exception('Orcamento finalizado não pode ser reprovado')
  
  def finalizado(self, orcamento):
    raise Exception('Orcamento ja finalizado')

class Orcamento(object):

  def __init__(self):
    self.__items = []
    self.estado_atual = Em_aprovacao()
    self.__desconto_extra = 0
  
  def aprova(self):
    self.estado_atual.aprova(orcamento)

  def reprova(self):
    self.estado_atual.reprova(orcamento)
  
  def finaliza(self):
    self.estado_atual.reprova(orcamento)

  def aplica_desconto_extra(self):

    self.estado_atual.aplica_desconto_extra(self)
  
  def adiciona_desconto_extra(self, desconto):

    self.__desconto_extra+= desconto

  @property
  def valor(self):
    total = 0.0
    for item in self.__items:
      total += item.valor
    return total - self.__desconto_extra
  
  def obter_items(self):
    return tuple(self.__items)
  
  @property
  def total_items(self):
    return len(self.__items)

  def adicionar_item(self, item):
    self.__items.append(item)
  
class Item(object):

  def __init__(self, nome, valor):
    self.__nome = nome
    self.__valor = valor

  @property
  def valor(self):
    return self.__valor
  
  @property
  def nome(self):
    return self.__nome

class Calculadora_de_impostos(object):

  def __str__(self):
    return self.__imposto_calculado

  def realiza_calculo(self, orcamento, imposto):

    imposto_calculado = imposto.calcula(orcamento)
    return imposto_calculado

class Impostos(object):
  
  def __init__(self, outro_imposto=None):
    self.__outro_imposto = outro_imposto
  
  def imposto_enario(self, orcamento):
    if self.__outro_imposto != None:
      return self.__outro_imposto.calcula(orcamento)
    else:
      return 0

  @abstractmethod
  def calcula(self, orcamento):
    pass

def IOF(calcula):
  def wrapper(self, orcamento):
    return calcula(self, orcamento) + 50
  return wrapper

class Impostos_Condicionais(Impostos):

  __metaclass__ = ABCMeta

  @IOF
  def calcula(self, orcamento):
    if(self.taxacao(orcamento)):
      return self.taxacao_maxima(orcamento) + self.imposto_enario(orcamento)
    else:
      return self.taxacao_minima(orcamento) + self.imposto_enario(orcamento)

  @abstractmethod #significa que precisa ser aplicado nas classes filhas que a ele se referenciam, por isso o pass
  def taxacao(self, orcamento):
    pass
  
  @abstractmethod
  def taxacao_maxima(self, orcamento):
    pass

  @abstractmethod
  def taxacao_minima(self, orcamento):
    pass

class ISS(Impostos_Condicionais):

  def taxacao(self, orcamento):
    return orcamento.valor >= 500 and orcamento.total_items >= 5
  
  def taxacao_maxima(self, orcamento):
    return orcamento.valor * 0.07 + self.imposto_enario(orcamento)

  def taxacao_minima(self, orcamento):
    return orcamento.valor * 0.05 + self.imposto_enario(orcamento)

class ICMS(Impostos_Condicionais):

  def taxacao(self, orcamento):
    return orcamento.valor > 1500
  
  def taxacao_maxima(self, orcamento):
    return orcamento.valor * 0.04 + self.imposto_enario(orcamento)

  def taxacao_minima(self, orcamento):
    return orcamento.valor * 0.02 + self.imposto_enario(orcamento)
  
  
from datetime import date

class Item(object):

  def __init__(self, descricao, valor):
    self.__descricao = descricao
    self.__valor = valor

    @property
    def descricao(self):
      return self.__descricao
    
    @property
    def valor(self):
      return self.__valor

class Nota_Fiscal(object):

  def __init__(self, razao_social, cnpj, itens, data_de_emissao=date.today(), 
               detalhes='', observadores=[]): #parâmetros opicionais devem ficar por último
    self.__razao_social = razao_social
    self.__cnpj = cnpj
    self.__data_de_emissao = data_de_emissao
    if len(detalhes) > 20:
      raise Exception('Detalhe não pode ter mais que 20 caracteres')
    self.__detalhes = detalhes
    self.__itens = itens
    
    for observador in observadores:
      observador(self)
  
  @property
  def razao_social(self):
    return self.__razao_social
  
  @property
  def cnpj(self):
    return self.__cnpj
  
  @property
  def data_de_emissao(self):
    return self.__data_de_emissao
  
  @property
  def detalhes(self):
    return self.__detalhes

class Criador_de_Nota_Fiscal(object): #builder

  def __init__(self):
    self.__razao_social = None
    self.__cnpj = None
    self.__data_de_emissao = None
    self.__detalhes = None
    self.__itens = None

  def razao_social(self, razao_social):
    self.__razao_social = razao_social
    return self

  def cnpj(self, cnpj):
    self.__cnpj = cnpj
    return self

  def data_de_emissao(self, data_de_emissao):
    self.__data_de_emissao = data_de_emissao
    return self

  def itens(self, itens):
    self.__itens = itens
    return self

  def detalhes(self, detalhes):
    self.__detalhes = detalhes
    return self

  def constroi(self):
    if self.__razao_social is None:
      raise Exception('Razao social deve ser preenchida')
    elif self.__cnpj is None:
      raise Exception('CNPJ deve ser preenchido')
    elif self.__itens is None:
      raise Exception('Não é possível criar nota sem itens')
    
    return Nota_Fiscal(razao_social=self.__razao_social, cnpj=self.__cnpj, 
                       data_de_emissao=self.__data_de_emissao, itens=self.__itens,
                       detalhes=self.__detalhes)

class Observadores(object):

  def imprime(self):
    print(nota_fiscal.cnpj)

  def envia_por_email(self):
    print(nota_fiscal.cnpj)

  def salva_no_banco(self):
    print(nota_fiscal.cnpj)

itens = [
         Item(
             'ITEM A',
              100
              ),
         Item('ITEM B',
              200
              )
  ]

nota_fiscal = Nota_Fiscal(
    razao_social='GSM LTDA',
    cnpj='0123123120',
    itens=itens,
    observadores=[Observadores.imprime, Observadores.envia_por_email, 
                  Observadores.salva_no_banco]
)

nota = (Criador_de_Nota_Fiscal()
                      .razao_social('GSM LTDA')
                      .cnpj('18885893200154')
                      .itens(itens)
                      .detalhes('')
                      .constroi()) #nota criada com builder
