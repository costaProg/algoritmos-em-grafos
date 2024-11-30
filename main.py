import random
import heapq
import numpy as np

class PontoDeColeta:
    def __init__(self, id, lixo, conexoes):
        self.id = id
        self.lixo = lixo  # metros cúbicos de lixo
        self.conexoes = conexoes  # [(vizinho, custo), ...]
        self.animais = {"ratos": 0, "gatos": 0, "cachorros": 0}

    def atualizar_animais(self):
        self.animais["ratos"] = random.random() < 0.5
        self.animais["gatos"] = random.random() < 0.25
        self.animais["cachorros"] = random.random() < 0.1

class CaminhaoDeLixo:
    def __init__(self, id, capacidade, funcionarios):
        self.id = id
        self.capacidade = capacidade
        self.funcionarios = funcionarios
        self.volume_atual = 0
        self.compactacoes = 0
        self.linha_do_tempo = []

    def compactar(self, tempo_atual):
        if self.compactacoes < 3:
            self.volume_atual *= (1 / 3)
            self.compactacoes += 1
            self.linha_do_tempo.append(
                f"[{tempo_atual} min] Caminhão {self.id}: Realizou compactação ({self.compactacoes}/3). Volume atual: {self.volume_atual:.2f} m³."
            )

    def descarregar(self, tempo_atual):
        if self.volume_atual > 0:
            self.linha_do_tempo.append(
                f"[{tempo_atual} min] Caminhão {self.id}: Descarregou no aterro. Volume descarregado: {self.volume_atual:.2f} m³."
            )
            self.volume_atual = 0
            self.compactacoes = 0

    def coleta(self, ponto, tempo_atual):
        tempo_gasto = int(np.ceil(ponto.lixo / self.funcionarios))
        if any(ponto.animais.values()):
            tempo_gasto *= 2

        if self.volume_atual + ponto.lixo > self.capacidade:
            if self.compactacoes < 3:
                self.compactar(tempo_atual)
            else:
                self.descarregar(tempo_atual)

        if ponto.lixo > 0:
            coletado = min(ponto.lixo, self.capacidade - self.volume_atual)
            ponto.lixo -= coletado
            self.volume_atual += coletado

            self.linha_do_tempo.append(
                f"[{tempo_atual} min] Caminhão {self.id}: Recolheu {coletado} m³ de lixo no ponto {ponto.id}. Volume atual: {self.volume_atual:.2f} m³."
            )
        
        return tempo_gasto

class Carrocinha:
    def __init__(self, id, capacidade):
        self.id = id
        self.capacidade = capacidade
        self.animais = 0
        self.linha_do_tempo = []

    def recolher_animal(self, animal, ponto_id, tempo_atual):
        if self.animais < self.capacidade:
            self.animais += 1
            self.linha_do_tempo.append(
                f"[{tempo_atual} min] Carrocinha {self.id}: Recolheu um {animal} no ponto {ponto_id}. Total de animais: {self.animais}."
            )

    def descarregar(self, tempo_atual):
        if self.animais > 0:
            self.linha_do_tempo.append(
                f"[{tempo_atual} min] Carrocinha {self.id}: Descarregou {self.animais} animais no abrigo."
            )
            self.animais = 0

def dijkstra(pontos, inicio):
    dist = {p.id: float('inf') for p in pontos}
    dist[inicio] = 0
    pq = [(0, inicio)]

    while pq:
        custo_atual, ponto_atual = heapq.heappop(pq)

        if custo_atual > dist[ponto_atual]:
            continue

        for vizinho, custo in pontos[ponto_atual].conexoes:
            novo_custo = custo_atual + custo
            if novo_custo < dist[vizinho]:
                dist[vizinho] = novo_custo
                heapq.heappush(pq, (novo_custo, vizinho))

    return dist

def movimentar_animais(pontos):
    for ponto in pontos:
        for animal in ["gatos", "cachorros"]:
            if ponto.animais[animal]:
                destino_id = random.choice([vizinho for vizinho, _ in ponto.conexoes])
                destino_ponto = next(p for p in pontos if p.id == destino_id)
                destino_ponto.animais[animal] += 1
                ponto.animais[animal] -= 1

def executar_coleta(pontos, caminhoes, carrocinhas, tempo_maximo):
    tempo_atual = 0
    
    while tempo_atual < tempo_maximo:
        for caminhao in caminhoes:
            for ponto in pontos:
                if tempo_atual >= tempo_maximo:
                    break
                
                # Coleta de lixo
                tempo_gasto_coleta = caminhao.coleta(ponto, tempo_atual)
                tempo_atual += tempo_gasto_coleta
                
                # Movimentação e coleta de animais
                movimentar_animais(pontos)

def main():
    with open("entrada.txt", "r") as f:
        num_pontos = int(f.readline().strip())
        pontos = []

        for i in range(num_pontos):
            linha = f.readline().strip().split()
            lixo = int(linha[0])
            conexoes = []
            for j in range(1, len(linha), 2):
                conexoes.append((int(linha[j]), int(linha[j + 1])))
            pontos.append(PontoDeColeta(i, lixo, conexoes))

    for ponto in pontos:
        ponto.atualizar_animais()

    caminhoes_necessarios, funcionarios_necessarios_por_caminhao = calcular_caminhao_minimo(pontos)
    
    caminhoes = [CaminhaoDeLixo(i, 10, funcionarios_necessarios_por_caminhao) for i in range(caminhoes_necessarios)]
    
    carrocinhas_necessarias = max(1, len([p for p in pontos if any(p.animais.values())]) // 5)
    carrocinhas = [Carrocinha(i, 5) for i in range(carrocinhas_necessarias)]

    tempo_maximo = 8 * 60 
    executar_coleta(pontos, caminhoes, carrocinhas, tempo_maximo)

    for caminhao in caminhoes:
        print(f"=== Linha do Tempo do Caminhão {caminhao.id} ===")
        for evento in caminhao.linha_do_tempo:
            print(evento)
    
    for carrocinha in carrocinhas:
        print(f"=== Linha do Tempo da Carrocinha {carrocinha.id} ===")
        for evento in carrocinha.linha_do_tempo:
            print(evento)

def calcular_caminhao_minimo(pontos):
    total_lixo_array = np.array([p.lixo for p in pontos])
    
    capacidade_caminhao_por_dia_array = np.full(total_lixo_array.shape,
                                                fill_value=10 * (8 * (60 / (total_lixo_array.mean()))))
    
    caminhoes_necessarios_array = np.ceil(total_lixo_array / capacidade_caminhao_por_dia_array).astype(int)
    
    caminhoes_necessarios_total = caminhoes_necessarios_array.max()
    
    funcionarios_necessarios_por_caminhao_total = max(3,
                                                      min(5,
                                                          np.ceil(total_lixo_array.sum() /
                                                                 (capacidade_caminhao_por_dia_array.sum() *
                                                                  caminhoes_necessarios_total)).astype(int)))
    
    return caminhoes_necessarios_total, funcionarios_necessarios_por_caminhao_total * caminhoes_necessarios_total

if __name__ == "__main__":
    main()