import random
import networkx as nx

# ------------------- PontoColeta -------------------

class PontoColeta:
    def __init__(self, id):
        self.id = id
        self.lixo = random.randint(15, 20)  # Lixo inicial (em metros cúbicos)
        self.animais = {'ratos': 0, 'gatos': 0, 'cachorros': 0}  # Animais presentes no ponto
        self.vizinhos = []  # Lista de conexões para outros pontos (arestas)
    
    def adicionar_animal(self, tipo):
        """Adiciona um animal ao ponto de coleta"""
        if tipo in self.animais:
            self.animais[tipo] += 1
    
    def tem_animais(self):
        """Verifica se existem animais no ponto"""
        return any(self.animais.values())  # Retorna True se houver qualquer animal
    
    def atualizar_dificuldade(self):
        """Atualiza a dificuldade de recolhimento baseado nos animais presentes"""
        if self.animais['ratos'] > 0 and self.animais['gatos'] > 0 and self.animais['cachorros'] > 0:
            return 3  # Maior dificuldade de coleta se todos os animais estão presentes
        elif any(self.animais.values()):
            return 2  # Dificuldade intermediária se apenas um tipo de animal está presente
        return 1  # Dificuldade normal

    def mostrar_animais(self):
        """Exibe quais animais estão presentes no ponto de coleta"""
        animais_presentes = [animal for animal, quantidade in self.animais.items() if quantidade > 0]
        return ', '.join(animais_presentes) if animais_presentes else 'Nenhum animal'


# ------------------- GrafoBairro -------------------

class GrafoBairro:
    def __init__(self, num_pontos):
        self.grafo = nx.Graph()  # Grafo não direcionado
        self.pontos = [PontoColeta(i) for i in range(num_pontos)]  # Lista de pontos de coleta
        for ponto in self.pontos:
            self.grafo.add_node(ponto.id)  # Adicionando os pontos como nós no grafo
    
    def adicionar_conexao(self, ponto1, ponto2, custo):
        """Adiciona uma conexão entre dois pontos de coleta com um custo"""
        self.grafo.add_edge(ponto1, ponto2, weight=custo)  # Adiciona aresta entre ponto1 e ponto2
    
    def gerar_animais(self):
        """Gera aleatoriamente os animais nos pontos de coleta com base nas interações de atração"""
        for ponto in self.pontos:
            if random.random() < 0.50:
                ponto.adicionar_animal('ratos')
            if random.random() < 0.25:
                ponto.adicionar_animal('gatos')
            if random.random() < 0.10:
                ponto.adicionar_animal('cachorros')
            
            # Lógica de atração dos animais entre os pontos
            if ponto.animais['ratos'] > 0:
                if random.random() < 0.75:  # 75% de chance de ter gatos se houver ratos
                    ponto.adicionar_animal('gatos')
                if random.random() < 0.10:  # 10% de chance de ter cachorros se houver ratos
                    ponto.adicionar_animal('cachorros')
            if ponto.animais['gatos'] > 0 and random.random() < 0.75:  # 75% de chance de ter cachorros se houver gatos
                ponto.adicionar_animal('cachorros')

    def caminho_mais_curto(self, origem, destino):
        """Calcula o caminho mais curto entre dois pontos usando o algoritmo de Dijkstra"""
        caminho = nx.dijkstra_path(self.grafo, origem, destino, weight='weight')
        custo = nx.dijkstra_path_length(self.grafo, origem, destino, weight='weight')
        return caminho, custo  # Retorna o caminho e o custo total


# ------------------- Caminhao -------------------

class Caminhao:
    def __init__(self, id, funcionarios):
        self.id = id
        self.funcionarios = funcionarios
        self.lixo_coletado = 0
        self.lixo_nao_compactado = 0
        self.capacidade_max = 50  # Capacidade máxima de lixo
        self.compactacoes = 0  # Número de compactações realizadas
    
    def tempo_para_coletar(self, lixo):
        """Calcula o tempo para coletar uma quantidade de lixo"""
        return lixo // self.funcionarios if lixo % self.funcionarios == 0 else lixo // self.funcionarios + 1

    def compactar_lixo(self):
        """Realiza a compactação do lixo"""
        if self.lixo_nao_compactado > 0 and self.compactacoes < 3:
            self.lixo_coletado += self.lixo_nao_compactado * 0.33
            self.lixo_nao_compactado = 0
            self.compactacoes += 1
            print(f"Compactação {self.compactacoes} realizada no caminhão {self.id}. Lixo compactado: {self.lixo_coletado} metros cúbicos.")
            return 10  # Tempo fixo de compactação
        else:
            self.lixo_coletado += self.lixo_nao_compactado * 0.33
            return 10

    def ir_ao_aterro(self):
        """Simula o caminhão indo ao aterro sanitário"""
        print(f"Caminhão {self.id} indo ao aterro com {self.lixo_coletado} metros cúbicos de lixo.")
        return 20  # Tempo para ir ao aterro


# ------------------- SistemaColeta -------------------

class SistemaColeta:
    def __init__(self, grafo):
        self.grafo = grafo
        self.caminhoes = []
        self.total_coletado = 0
        self.tempo_max = 1440  # Tempo máximo para a coleta (em minutos) ajustado para ser mais realista
        self.tempo_total = 0

    def alocar_caminhoes(self):
        caminhões_alocados = 1
        total_lixo = sum([ponto.lixo for ponto in self.grafo.pontos])
        tempo_restante = self.tempo_max
        
        # Inicializa o ciclo de coleta
        while self.total_coletado < total_lixo and tempo_restante > 0:
            caminhão = Caminhao(caminhões_alocados, 4)  # Alocando 4 funcionários por caminhão
            caminhões_alocados += 1
            self.caminhoes.append(caminhão)

            # Percorrer todos os pontos de coleta
            for ponto in self.grafo.pontos:
                if ponto.lixo > 0:
                    tempo_recolhimento = caminhão.tempo_para_coletar(ponto.lixo)
                    tempo_restante -= tempo_recolhimento
                    self.tempo_total += tempo_recolhimento  # Atualizando o tempo total de coleta
                    print(f"Caminhão {caminhão.id} chegou ao ponto {ponto.id}. Lixo coletado: {ponto.lixo} metros cúbicos.")
                    # Adiciona o lixo ao caminhão
                    caminhão.lixo_nao_compactado += ponto.lixo
                    ponto.lixo = 0  # Lixo recolhido

                    # Verificar se há animais no ponto
                    if ponto.tem_animais():
                        print(f"Caminhão {caminhão.id} chegou ao ponto {ponto.id} com animais: {ponto.mostrar_animais()}")
                        if ponto.animais['cachorros'] > 0 or ponto.animais['gatos'] > 0:
                            print(f"Chamada da carrocinha no ponto {ponto.id}.")
                        if ponto.animais['ratos'] > 0 and ponto.animais['gatos'] > 0 and ponto.animais['cachorros'] > 0:
                            print(f"Detetização no ponto {ponto.id}.")

                    # Realiza compactação se necessário
                    if caminhão.lixo_nao_compactado >= caminhão.capacidade_max * 0.75:  # Se atingir 75% da capacidade
                        tempo_restante -= caminhão.compactar_lixo()
                        self.tempo_total += 10  # Tempo fixo de compactação

                    # Se o caminhão está cheio, vai ao aterro e aloca outro caminhão
                    if caminhão.lixo_coletado >= caminhão.capacidade_max:
                        tempo_restante -= caminhão.ir_ao_aterro()
                        self.tempo_total += 20  # Tempo de ida ao aterro
                        caminhão.lixo_coletado = 0  # Caminhão vazio após ir ao aterro
                        self.total_coletado += caminhão.capacidade_max
                        # Troca para o próximo caminhão
                        caminhão = Caminhao(caminhões_alocados, 4)  # Alocando 4 funcionários por caminhão
                        caminhões_alocados += 1
                        self.caminhoes.append(caminhão)

            if tempo_restante <= 0:
                print("Tempo máximo de coleta alcançado.")
                break  # Para de coletar se o tempo se esgotar
 
        return caminhões_alocados


# ------------------- Execução -------------------

# Configuração inicial do bairro e do sistema
bairro = GrafoBairro(15)  # Reduzindo o número de pontos para evitar travamento
bairro.adicionar_conexao(0, 1, 5)
bairro.adicionar_conexao(1, 2, 3)
bairro.adicionar_conexao(2, 3, 2)
bairro.adicionar_conexao(3, 4, 4)
bairro.adicionar_conexao(4, 5, 2)
bairro.adicionar_conexao(5, 6, 4)
bairro.adicionar_conexao(6, 7, 7)
bairro.adicionar_conexao(7, 8, 8)
bairro.adicionar_conexao(8, 9, 3)
bairro.adicionar_conexao(9, 10, 6)
bairro.adicionar_conexao(10, 11, 2)
bairro.adicionar_conexao(11, 12, 5)
bairro.adicionar_conexao(12, 13, 6)
bairro.adicionar_conexao(13, 14, 3)

bairro.gerar_animais()

# Sistema de coleta de lixo
sistema = SistemaColeta(bairro)
caminhoes_alocados = sistema.alocar_caminhoes()

print(f"\nCaminhões alocados para coleta: {caminhoes_alocados}")
print(f"Tempo total de coleta: {sistema.tempo_total} minutos")
