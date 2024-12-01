import random
import numpy as np
import heapq  # Para Dijkstra

class PontoDeColeta:
    def __init__(self, id, latas, conexoes):
        self.id = id
        self.latas = latas  # Número de latas cheias de lixo
        self.conexoes = conexoes  # [(vizinho, custo), ...]
        self.animais = {"ratos": 0, "gatos": 0, "cachorros": 0}

    def atualizar_animais(self):
        """Atualiza os animais no ponto de coleta de maneira aleatória."""
        self.animais["ratos"] = random.randint(0, 5)  # Ratos aleatórios
        self.animais["gatos"] = random.randint(0, 2)  # Gatos aleatórios
        self.animais["cachorros"] = random.randint(0, 1)  # Cachorros aleatórios

    def mover_animais(self, pontos):
        """Realiza a movimentação dos animais entre os pontos de coleta, baseado em regras."""
        if sum(self.animais.values()) > 0:
            print(f"\n=== Movimentação de Animais no Ponto {self.id} ===")

        # Caso haja ao menos um gato, os ratos fogem
        if self.animais["gatos"] > 0 and self.animais["ratos"] > 0:
            ratos_fugindo = self.animais["ratos"] - 1
            self.animais["ratos"] = 0
            self._redistribuir_animais("ratos", ratos_fugindo, pontos)
            print(f"{ratos_fugindo} ratos fugiram para os pontos vizinhos devido à presença de gatos.")

        # Caso haja ao menos um cachorro, os gatos fogem
        if self.animais["cachorros"] > 0 and self.animais["gatos"] > 1:
            gatos_fugindo = self.animais["gatos"] - 1
            self.animais["gatos"] = 0
            self._redistribuir_animais("gatos", gatos_fugindo, pontos)
            print(f"{gatos_fugindo} gatos fugiram para os pontos vizinhos devido à presença de cachorros.")

        # Caso o ponto não tenha lixo, todos os animais migram
        if self.latas == 0:
            for animal, quantidade in self.animais.items():
                if quantidade > 0:
                    self._redistribuir_animais(animal, quantidade, pontos)
                    print(f"Animais ({animal}) saíram devido à falta de lixo.")
            self.animais = {"ratos": 0, "gatos": 0, "cachorros": 0}

    def _redistribuir_animais(self, animal, quantidade, pontos):
        """Redistribui os animais para pontos vizinhos."""
        for vizinho, _ in self.conexoes:
            if quantidade <= 0:
                break
            pontos[vizinho].animais[animal] += 1
            quantidade -= 1

    def espalhar_lixo(self):
        """Aumenta a quantidade de lixo devido ao espalhamento pelos animais."""
        if sum(self.animais.values()) > 0:
            print(f"Ponto {self.id} - Animais espalharam o lixo!")
            self.latas += random.randint(1, 3)  # Aumenta o lixo devido ao espalhamento


class CaminhaoDeLixo:
    def __init__(self, id, capacidade, funcionarios):
        self.id = id
        self.capacidade = capacidade
        self.funcionarios = funcionarios
        self.volume_atual = 0
        self.compactacoes = 0
        self.linha_do_tempo = []

    def coletar(self, ponto, tempo_atual):
        """Coleta o lixo do ponto de coleta e atualiza o estado do caminhão."""
        if ponto.latas == 0:
            return 0

        lixo_a_coletar = ponto.latas * 0.1  # Cada lata representa 0.1 m³ de lixo
        tempo_base = int(np.ceil(lixo_a_coletar / self.funcionarios))

        if sum(ponto.animais.values()) == 3:  # Vários animais
            lixo_a_coletar *= 1.5  # Lixo espalhado aumenta o volume
            tempo_base *= 2  # Dobra o tempo
            self.linha_do_tempo.append(
                f"[{tempo_atual} min] Caminhão {self.id}: Centro de zoonoses informado sobre animais no ponto {ponto.id}."
            )

        if self.volume_atual + lixo_a_coletar > self.capacidade:
            self.compactar(tempo_atual)
            if self.volume_atual + lixo_a_coletar > self.capacidade:
                self.descarregar(tempo_atual)

        coletado = min(lixo_a_coletar, self.capacidade - self.volume_atual)
        self.volume_atual += coletado
        ponto.latas -= int(coletado / 0.1)

        self.linha_do_tempo.append(
            f"[{tempo_atual} min] Caminhão {self.id}: Coletou {coletado:.2f} m³ de lixo no ponto {ponto.id}. "
            f"Volume atual: {self.volume_atual:.2f} m³."
        )
        return max(1, tempo_base)

    def compactar(self, tempo_atual):
        """Compacta o lixo no caminhão se necessário."""
        if self.compactacoes < 3:
            self.volume_atual *= (1 / 3)
            self.compactacoes += 1
            self.linha_do_tempo.append(
                f"[{tempo_atual} min] Caminhão {self.id}: Compactação realizada ({self.compactacoes}/3)."
            )

    def descarregar(self, tempo_atual):
        """Descarrega o lixo no aterro e reseta o volume."""
        self.linha_do_tempo.append(
            f"[{tempo_atual} min] Caminhão {self.id}: Descarregou no aterro. Volume descarregado: {self.volume_atual:.2f} m³."
        )
        self.volume_atual = 0
        self.compactacoes = 0


class Carrocinha:
    def __init__(self, id, capacidade):
        self.id = id
        self.capacidade = capacidade
        self.animais = 0
        self.linha_do_tempo = []

    def recolher_animais(self, ponto, tempo_atual):
        """Recolhe todos os animais de um tipo específico no ponto e atualiza a linha do tempo da carrocinha."""
        for animal, quantidade in ponto.animais.items():
            if animal in ["gatos", "cachorros"]:  # Apenas recolher gatos e cachorros
                while quantidade > 0 and self.animais < self.capacidade:
                    self.animais += 1
                    quantidade -= 1
                    self.linha_do_tempo.append( 
                        f"[{tempo_atual} min] Carrocinha {self.id}: Recolheu um {animal} no ponto {ponto.id}. "
                        f"Total de animais: {self.animais}."
                    )
                # Atualiza o ponto com a quantidade restante de animais
                ponto.animais[animal] = quantidade

    def descarregar(self, tempo_atual):
        """Descarrega os animais no abrigo e reseta o número de animais."""
        if self.animais > 0:
            self.linha_do_tempo.append(
                f"[{tempo_atual} min] Carrocinha {self.id}: Descarregou {self.animais} animais no abrigo."
            )
            self.animais = 0


def dijkstra(pontos, origem):
    """Calcula as distâncias mínimas entre pontos usando o algoritmo de Dijkstra."""
    dist = {ponto.id: float('inf') for ponto in pontos}
    dist[origem] = 0
    pq = [(0, origem)]  # (distancia, ponto_id)
    
    while pq:
        distancia_atual, ponto_id = heapq.heappop(pq)
        
        if distancia_atual > dist[ponto_id]:
            continue
        
        for vizinho, custo in pontos[ponto_id].conexoes:
            nova_distancia = distancia_atual + custo
            if nova_distancia < dist[vizinho]:
                dist[vizinho] = nova_distancia
                heapq.heappush(pq, (nova_distancia, vizinho))

    return dist


def executar_coleta(pontos, caminhoes, carrocinhas, tempo_maximo):
    tempo_atual = 0
    caminhões_em_uso = caminhoes.copy()

    distancias = {ponto.id: dijkstra(pontos, ponto.id) for ponto in pontos}

    while tempo_atual < tempo_maximo:
        if all(ponto.latas == 0 for ponto in pontos):
            print("Todos os pontos estão limpos. Finalizando...")
            break

        # Coleta de lixo
        for caminhao in caminhões_em_uso:
            for ponto in pontos:
                if ponto.latas > 0:
                    tempo_atual += caminhao.coletar(ponto, tempo_atual)

        # Adiciona novos caminhões se necessário
        if any(caminhao.volume_atual >= caminhao.capacidade for caminhao in caminhões_em_uso):
            caminhões_em_uso.append(CaminhaoDeLixo(len(caminhões_em_uso), 10, random.randint(3, 5)))
            print("Novo caminhão alocado para coleta!")

        # Recolhimento de animais
        for carrocinha in carrocinhas:
            for ponto in pontos:
                carrocinha.recolher_animais(ponto, tempo_atual)  # Passa o objeto ponto corretamente

        # Movimentação e espalhamento dos animais
        for ponto in pontos:
            ponto.mover_animais(pontos)
            ponto.espalhar_lixo()

def main():
    # Lê dados do arquivo de entrada
    with open("entrada.txt", "r") as f:
        num_pontos = int(f.readline().strip())
        pontos = []
        for i in range(num_pontos):
            linha = f.readline().strip().split()
            latas = int(linha[0])
            conexoes = [(int(linha[j]), int(linha[j + 1])) for j in range(1, len(linha), 2)]
            pontos.append(PontoDeColeta(i, latas, conexoes))

    # Atualiza os animais nos pontos de coleta
    for ponto in pontos:
        ponto.atualizar_animais()

    # Inicializa caminhões e carrocinhas
    caminhoes = [CaminhaoDeLixo(i, 5, random.randint(3, 5)) for i in range(3)]
    carrocinhas = [Carrocinha(i, 5) for i in range(2)]

    # Executa o ciclo de coleta
    executar_coleta(pontos, caminhoes, carrocinhas, 8 * 60)

    # Exibe a linha do tempo dos caminhões
    for caminhao in caminhoes:
        print(f"=== Linha do Tempo do Caminhão {caminhao.id} ===")
        for evento in caminhao.linha_do_tempo:
            print(evento)

    # Exibe a linha do tempo das carrocinhas
    for carrocinha in carrocinhas:
        print(f"=== Linha do Tempo da Carrocinha {carrocinha.id} ===")
        for evento in carrocinha.linha_do_tempo:
            print(evento)


if __name__ == "__main__":
    main()