import random
import math

# Variáveis globais para armazenar resultados
total_lixo_coletado = 0
total_animais_recolhidos = 0

class PontoColeta:
    def __init__(self, id, volume_lixo, lixo_espalhado):
        self.id = id
        self.volume_lixo = volume_lixo  # em metros cúbicos
        self.lixo_espalhado = lixo_espalhado

class Caminhao:
    def __init__(self, capacidade):
        self.capacidade_total = capacidade
        self.volume_atual = 0
        self.compactacoes = 0  # Contador de compactações

    def coletar_lixo(self, volume):
        if (self.volume_atual + volume) <= self.capacidade_total:
            self.volume_atual += volume

    def esvaziar(self):
        global total_lixo_coletado
        total_lixo_coletado += self.volume_atual  # Atualiza o total de lixo coletado
        print(f"Caminhão descarrega {self.volume_atual:.2f} m³ de lixo.")
        self.volume_atual = 0
        self.compactacoes = 0  # Reinicia o contador de compactações após descarregar

class GerenciadorColetaLixo:
    def __init__(self):
        self.caminhoes = []
        self.pontos_coleta = {}
        self.capacidade_caminhao = 10  # em metros cúbicos
        self.max_compactacoes = 3

    def alocar_caminhao(self, ponto, tempo_atual):
        caminhao_disponivel = next((c for c in self.caminhoes if c.volume_atual < self.capacidade_caminhao), None)
        if not caminhao_disponivel:
            caminhao_disponivel = Caminhao(self.capacidade_caminhao)
            self.caminhoes.append(caminhao_disponivel)

        volume_coletado = min(caminhao_disponivel.capacidade_total - caminhao_disponivel.volume_atual, self.pontos_coleta[ponto].volume_lixo)
        
        if volume_coletado > 0:
            caminhao_disponivel.coletar_lixo(volume_coletado)
            self.pontos_coleta[ponto].volume_lixo -= volume_coletado
            
            print(f"{tempo_atual} min: Caminhão {len(self.caminhoes)} coleta {volume_coletado:.2f} m³ de lixo do ponto {ponto}.")
        
            # Compactar o lixo se o caminhão estiver cheio
            if caminhao_disponivel.volume_atual >= caminhao_disponivel.capacidade_total:
                self.compactar_lixo(caminhao_disponivel, tempo_atual)

    def calcular_tempo_coleta(self, ponto, funcionarios):
        volume_lixo = self.pontos_coleta[ponto].volume_lixo
        tempo_base = volume_lixo / funcionarios  # metros cúbicos por funcionário por minuto
        if self.pontos_coleta[ponto].lixo_espalhado:
            tempo_base *= 2  # Tempo dobra se o lixo foi espalhado
        return max(1, math.ceil(tempo_base))

    def compactar_lixo(self, caminhao, tempo_atual):
        if caminhao.compactacoes < self.max_compactacoes:
            caminhao.volume_atual *= (1/3)  # Compacta para um terço do volume atual
            caminhao.compactacoes += 1
            print(f"{tempo_atual} min: Caminhão {len(self.caminhoes)} compacta o lixo para {caminhao.volume_atual:.2f} m³.")
        else:
            print(f"{tempo_atual} min: Caminhão {len(self.caminhoes)} não pode compactar mais. Precisa descarregar.")

class GerenciadorAnimaisRua:
    def __init__(self):
        self.animais_por_ponto = {}
        
    def inicializar_animais(self, pontos_coleta):
        for ponto in pontos_coleta:
            self.animais_por_ponto[ponto] = {
                'ratos': random.randint(0, 1),
                'gatos': random.randint(0, 1),
                'cachorros': random.randint(0, 1)
            }

    def recolher_animais(self, ponto, tempo_atual):
        global total_animais_recolhidos
        
        animais_recolhidos = min(5, sum(self.animais_por_ponto[ponto].values()))  
        
        for animal in ['gatos', 'cachorros']:
            while animais_recolhidos > 0 and self.animais_por_ponto[ponto][animal] > 0:
                print(f"{tempo_atual} min: Carrocinha recolhe um {animal} do ponto {ponto}.")
                self.animais_por_ponto[ponto][animal] -= 1
                animais_recolhidos -= 1
                
                total_animais_recolhidos += 1  # Atualiza o total de animais recolhidos
                
        return min(5 - animais_recolhidos, sum(self.animais_por_ponto[ponto].values()))  

class SimuladorBairro:
    def __init__(self, gerenciador_lixo, gerenciador_animais):
        self.gerenciador_lixo = gerenciador_lixo
        self.gerenciador_animais = gerenciador_animais
        self.tempo_atual = 0

    def simular_dia(self):
        while True:  
            todos_visitados = True
            
            for ponto in list(self.gerenciador_lixo.pontos_coleta.keys()):
                funcionarios = random.randint(3, 5)
                tempo_coleta = self.gerenciador_lixo.calcular_tempo_coleta(ponto, funcionarios)  
                
                if tempo_coleta + self.tempo_atual > 480:  
                    break
                
                custo_mover = random.randint(1,5) 
                if custo_mover + self.tempo_atual > 480:
                    break
                
                print(f"{self.tempo_atual} min: Caminhão se move para o ponto {ponto}, custo {custo_mover} min.")
                self.tempo_atual += custo_mover
                
                print(f"{self.tempo_atual} min: Iniciando coleta no ponto {ponto}.")
                self.gerenciador_lixo.alocar_caminhao(ponto, self.tempo_atual)
                animais_recolhidos = self.gerenciador_animais.recolher_animais(ponto, self.tempo_atual)
                
                print(f"{self.tempo_atual} min: Animais recolhidos em {ponto}: {animais_recolhidos}")
                
                # Atualiza o tempo atual com o tempo gasto na coleta
                self.tempo_atual += tempo_coleta
                
                if (self.gerenciador_lixo.caminhoes[-1].volume_atual >= 
                    self.gerenciador_lixo.caminhoes[-1].capacidade_total and 
                    self.gerenciador_lixo.caminhoes[-1].compactacoes >= 
                    self.gerenciador_lixo.max_compactacoes):
                    print(f"{self.tempo_atual} min: Caminhão {len(self.gerenciador_lixo.caminhoes)} está cheio e vai ao aterro.")
                    # Aqui chamamos a função esvaziar para atualizar o total de lixo coletado.
                    self.gerenciador_lixo.caminhoes[-1].esvaziar()
                
                if self.gerenciador_lixo.pontos_coleta[ponto].volume_lixo > 0:
                    todos_visitados = False
            
            if todos_visitados or self.tempo_atual >= 480:
                break

class GeradorRelatorios:
    @staticmethod
    def gerar_relatorio(gerenciador_lixo, gerenciador_animais):
        global total_lixo_coletado
        global total_animais_recolhidos
        
        num_caminhoes = len(gerenciador_lixo.caminhoes)
        
        num_funcionarios = num_caminhoes * random.randint(3, 5)  

        relatorio = f"""Saída:
Seu programa deverá indicar os números mínimos de caminhões de lixo e funcionários necessários para recolher todo o lixo do bairro dentro de 8 horas.

Número mínimo de caminhões: {num_caminhoes}
Número mínimo de funcionários: {num_funcionarios}
Número de carrocinhas necessárias: {math.ceil(total_animais_recolhidos / 5)}
Total de lixo coletado: {total_lixo_coletado:.2f} m³
Total de animais recolhidos: {total_animais_recolhidos}"""

        with open("relatorio.txt", "w") as arquivo:
            arquivo.write(relatorio)

        return relatorio

class LeitorEntrada:
    @staticmethod
    def ler_arquivo(nome_arquivo):
        dados = {'pontos_coleta': {}}
        
        with open(nome_arquivo, 'r') as arquivo:
            num_pontos = int(arquivo.readline().strip())
            for _ in range(num_pontos):
                linha = arquivo.readline().strip().split()
                id_punto = int(linha[0])   # Corrigido para id_punto.
                volume_lixo = float(linha[1])   # Volume em metros cúbicos
                lixo_espalhado = linha[2] == '1'
                dados['pontos_coleta'][id_punto] = PontoColeta(id_punto, volume_lixo, lixo_espalhado)

        return dados

def main():
    dados_entrada = LeitorEntrada.ler_arquivo("entrada.txt")
    
    gerenciador_lixo = GerenciadorColetaLixo()
    gerenciador_animais = GerenciadorAnimaisRua()
    
    gerenciador_lixo.pontos_coleta = dados_entrada['pontos_coleta']
    gerenciador_animais.inicializar_animais(dados_entrada['pontos_coleta'])
    
    simulador = SimuladorBairro(gerenciador_lixo, gerenciador_animais)
    simulador.simular_dia()
    
    relatorio = GeradorRelatorios.gerar_relatorio(gerenciador_lixo, gerenciador_animais)
    
    # Exibir o relatório no console
    print(relatorio)

if __name__ == "__main__":
    main()