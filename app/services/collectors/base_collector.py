from abc import ABC, abstractmethod

class BaseCollector(ABC):
    """
    Classe base abstrata para todos os coletores de dados.
    Define a interface que todos os coletores devem seguir.
    """
    @abstractmethod
    def collect(self, region: str):
        """
        O método principal que será chamado para iniciar a coleta de dados.
        Deve ser implementado por todas as subclasses.

        :param region: O código da região (ex: 'BR', 'US') para a coleta.
        """
        pass
