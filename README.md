
# Sistema de Coleta de Lixo e Controle de Animais

Este projeto implementa um sistema de gerenciamento de coleta de lixo e controle de animais em um bairro. O programa simula a operação de caminhões de lixo e carrocinhas para otimizar a coleta e o transporte de resíduos e animais.

## Requisitos

- **Python 3.x**
- **Bibliotecas:** `numpy`, `heapq`

## Instruções para Execução

### Clone o Repositório
```bash
git clone <URL do repositório>
cd <nome do diretório>
```

### Instale as Dependências
Certifique-se de que as bibliotecas necessárias estão instaladas:
```bash
pip install numpy
```

### Prepare o Arquivo de Entrada
Crie um arquivo chamado `entrada.txt` no mesmo diretório do script principal. O arquivo deve seguir o seguinte formato:

```plaintext
<número_de_pontos>
<id_aterro>
<id_zoonoses>
<lixo_ponto_0> <id_vizinho_1> <custo_1> <id_vizinho_2> <custo_2> ...
...
```

- **número_de_pontos:** Total de pontos de coleta.
- **id_aterro:** ID do ponto que representa o aterro sanitário.
- **id_zoonoses:** ID do ponto que representa o centro de zoonoses.
- **lixo_ponto_X:** Volume inicial de lixo no ponto X.
- **id_vizinho_Y e custo_Y:** IDs dos pontos vizinhos e custo para alcançá-los.

### Execute o Programa
Execute o script principal para iniciar a simulação:
```bash
python main.py
```

## Saída Esperada
O programa imprimirá uma linha do tempo detalhada das operações, incluindo:

- Coleta de lixo.
- Compactação.
- Movimentação de animais.
- Descarregamento no aterro ou centro de zoonoses.

### Relatório Final
Ao final da execução, será gerado um relatório indicando o número mínimo de caminhões e funcionários necessários para completar a operação dentro do limite de oito horas.

## Exemplo de `entrada.txt`
```plaintext
6
4
5
10 1 5 2 10
15 0 5 3 8
20 0 10 4 7
25 1 8 5 12
0
0
```

- Neste exemplo, há **seis pontos** no total.
- Os IDs **4** e **5** representam o aterro sanitário e o centro de zoonoses, respectivamente.
- Cada linha subsequente especifica:
  - O volume inicial de lixo em cada ponto.
  - Suas conexões com outros pontos.

## Considerações Finais

- Certifique-se de que todos os IDs dos pontos são válidos.
- As conexões devem representar caminhos **bidirecionais**.
- Ajuste os volumes e custos conforme necessário para simular diferentes cenários operacionais.
```