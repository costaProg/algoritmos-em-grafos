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

def movimentar_animais(pontos, carrocinhas, linha_do_tempo_global, tempo_atual):
    for ponto in pontos:
        for animal in ["gatos", "cachorros"]:
            if ponto.animais[animal]:
                carrocinha_disponivel = next((c for c in carrocinhas if c.animais < c.capacidade), None)
                if carrocinha_disponivel:
                    carrocinha_disponivel.recolher_animal(animal, ponto.id, tempo_atual)
                    linha_do_tempo_global.append(f"[{tempo_atual} min] Carrocinha {carrocinha_disponivel.id} recolheu um {animal} no ponto {ponto.id}.")
                    ponto.animais[animal] -= 1

def executar_coleta_simultanea(pontos, caminhoes, carrocinhas, aterro_id, zoonoses_id, tempo_maximo):
    tempo_atual = 0
    linha_do_tempo_global = []

    while tempo_atual < tempo_maximo:
        
        all_collected = all(p.lixo == 0 for p in pontos)

        for caminhao in caminhoes:
            for ponto in pontos:
                if ponto.lixo > 0:
                    all_collected = False
                    tempo_gasto_coleta = caminhao.coleta(ponto, tempo_atual)
                    linha_do_tempo_global.append(f"[{tempo_atual} min] Caminhão {caminhao.id} recolheu lixo no ponto {ponto.id}.")
                    tempo_atual += tempo_gasto_coleta
                
                while caminhao.volume_atual > caminhao.capacidade and caminhao.compactacoes < 3:
                    caminhao.compactar()
                    linha_do_tempo_global.append(f"[{tempo_atual} min] Caminhão {caminhao.id} compactou o lixo.")
                    tempo_atual += dijkstra(pontos, caminhao.id)[aterro_id]

                if caminhao.volume_atual >= caminhao.capacidade and caminhao.compactacoes == 3:
                    linha_do_tempo_global.append(f"[{tempo_atual} min] Caminhão {caminhao.id} indo para o aterro.")
                    tempo_atual += dijkstra(pontos, caminhao.id)[aterro_id]
                    caminhao.descarregar(tempo_atual)
                    linha_do_tempo_global.append(f"[{tempo_atual} min] Caminhão {caminhao.id} descarregou no aterro.")

                movimentar_animais(pontos, carrocinhas, linha_do_tempo_global, tempo_atual)

                if all_collected or tempo_atual >= tempo_maximo:
                    return linha_do_tempo_global
    
    return linha_do_tempo_global

def calcular_recursos_minimos(pontos, tempo_maximo=8*60):
    capacidade_caminhao = 10
    funcionarios_por_caminhao = 5
    capacidade_carrocinha = 5

    total_lixo = sum(p.lixo for p in pontos)
    total_animais = sum(any(p.animais.values()) for p in pontos)

    caminhoes_necessarios = max(1, int(np.ceil(total_lixo / capacidade_caminhao)))

    tempo_total_coleta = sum(int(np.ceil(p.lixo / funcionarios_por_caminhao)) * (2 if any(p.animais.values()) else 1) for p in pontos)

    if tempo_total_coleta > tempo_maximo:
        caminhoes_necessarios = max(caminhoes_necessarios, int(np.ceil(tempo_total_coleta / tempo_maximo)))
    
    funcionarios_necessarios = caminhoes_necessarios * funcionarios_por_caminhao

    carrocinhas_necessarias = max(1, int(np.ceil(total_animais / capacidade_carrocinha)))

    return caminhoes_necessarios, funcionarios_necessarios, carrocinhas_necessarias

def main():
    with open("entrada.txt", "r") as f:
        num_pontos = int(f.readline().strip())
        
        # Ler IDs do aterro e do centro de zoonoses
        aterro_id = int(f.readline().strip())
        zoonoses_id = int(f.readline().strip())

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

    caminhoes_necessarios, funcionarios_necessarios, carrocinhas_necessarias = calcular_recursos_minimos(pontos)

    caminhoes = [CaminhaoDeLixo(i, 10, funcionarios_necessarios // caminhoes_necessarios) for i in range(caminhoes_necessarios)]
    
    carrocinhas = [Carrocinha(i, 5) for i in range(carrocinhas_necessarias)]

    tempo_maximo = 8 * 60 
    linha_do_tempo_global = executar_coleta_simultanea(pontos, caminhoes, carrocinhas, aterro_id, zoonoses_id, tempo_maximo)

    print("=== Linha do Tempo Global ===")
    for evento in linha_do_tempo_global:
        print(evento)

if __name__ == "__main__":
    main()