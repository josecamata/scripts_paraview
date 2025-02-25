# Script `extract_deposition.py`

## Descrição
Este script processa arquivos XDMF e extrai dados do campo de sedimento (`s_dep_01`). Os dados extraídos são armazenados incrementalmente em um arquivo HDF5 (`.h5`), permitindo análise ao longo de vários timesteps.

## Requisitos
- Python
- ParaView (`paraview.simple`)
- NumPy
- Biblioteca `gc` para gerenciamento de memória
- Biblioteca `h5py` para armazenamento eficiente em HDF5

## Como Executar
O script deve ser chamado com dois argumentos correspondentes ao tempo inicial e final:
```bash
pvpython extract_deposition.py <initial_time> <final_time>
```
Exemplo de execução:
```bash
pvpython extract_deposition.py 1 10
```

**Importante:** Para simulaçãoes com muitos passos de tempo, é necessário executar o scripts por etapas. Por exemplo, para simulação com 50 timesteps, execute usando três chamadas. Isso evitará possivels *crash* da execução devido ao consumo de memória. 

Exemplo de execução:
```bash
pvpython extract_deposition.py 1 15
pvpython extract_deposition.py 16 30
pvpython extract_deposition.py 31 50

```

## Estrutura do Script
### 1. `ExtractDep(file_path: str)`
Função responsável por carregar o arquivo XDMF e extrair os dados do campo `s_dep_01`.

#### Parâmetros:
- `file_path` (str): Caminho para o arquivo XDMF.

#### Retorno:
- `time` (float): Tempo do timestep processado.
- `s_dep_01` (numpy array): Dados extraídos do campo `s_dep_01`.

#### Processo:
1. Carrega o arquivo XDMF.
2. Aplica filtros `MergeBlocks`, `CleanToGrid`, `ExtractSurface` e `Clip` para refinar os dados.
3. Obtém os valores do campo `s_dep_01` e os retorna como um array NumPy.
4. Libera memória removendo objetos grandes.

### 2. Processamento dos Timesteps
- O script lê os argumentos `initial_time` e `final_time`.
- Para cada timestep:
  1. Carrega o arquivo correspondente (`tanque_XXXXX.xmf`).
  2. Extrai os dados usando `ExtractDep()`.
  3. Converte os dados para `float32` para reduzir o consumo de memória.
  4. Salva os resultados incrementalmente em um arquivo `.h5`.

### 3. Uso do HDF5 para Armazenamento Eficiente
- O script usa `h5py` para armazenar os dados de forma eficiente sem necessidade de realocação de memória.
- Se o arquivo já existir, ele atualiza os dados sem recriá-lo.
- Se os tamanhos forem compatíveis, os novos dados são adicionados como colunas no dataset `data`.

### 4. Otimização de Memória
- O script usa `gc.collect()` após processar cada timestep para liberar memória.
- Objetos são explicitamente removidos com `del`.

## Saída
O script gera um arquivo `.h5` contendo os dados extraídos:
```bash
TANQUE_P1_DEP.h5
```
Os dados podem ser carregados no Python com:
```python
import h5py
with h5py.File("TANQUE_P1_DEP.h5", "r") as f:
    print(f["data"].shape)  # Exibe a forma dos dados
```


