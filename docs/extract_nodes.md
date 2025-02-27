# Documentação do Script `extract_nodes.py`

## 📌 Descrição
Este script processa arquivos XDMF e extrai as coordenadas dos nós dentro de uma região definida por um **Clip**. A geometria extraída no primeiro timestep é salva em um arquivo HDF5 (`.h5`). Nos timesteps subsequentes, o script verifica se houve alteração nas coordenadas.

## 🛠️ Requisitos
- Python
- ParaView (`paraview.simple`)
- NumPy
- Biblioteca `gc` para gerenciamento de memória
- Biblioteca `h5py` para armazenamento eficiente em HDF5

## 🚀 Como Executar
O script pode ser executado da seguinte forma:
```bash
python extract_nodes.py <dir_path> <prefix_file_name> <hdf5_file> [initial_time] [final_time]
```

### 📌 Exemplo de Uso:
```bash
python extract_nodes.py /dados/simulacao/ tanque TANQUE_NODES.h5 1 50
```
📌 Isso processará os arquivos `tanque_00001.xmf` até `tanque_00050.xmf` e salvará a geometria inicial no arquivo `TANQUE_NODES.h5`.

## 🔹 Estrutura do Script
### 1️⃣ `ExtractNodeCoordinates(file_path: str)`
Função responsável por carregar um arquivo XDMF e extrair as coordenadas dos nós dentro da área do **Clip**.

#### 🔹 Parâmetros:
- `file_path` (str): Caminho para o arquivo XDMF.

#### 🔹 Retorno:
- `node_coords` (numpy array): Coordenadas dos nós extraídos.

#### 🔹 Processo:
1. Carrega o arquivo XDMF.
2. Aplica os filtros:
   - `MergeBlocks`
   - `CleanToGrid`
   - `ExtractSurface`
   - `Clip` (define a região de interesse)
3. Obtém as coordenadas dos nós filtrados.
4. Retorna um array NumPy com as coordenadas.

### 2️⃣ Processamento dos Timesteps
- O script lê os argumentos `initial_time` e `final_time`.
- Para cada timestep:
  1. Carrega o arquivo correspondente (`tanque_XXXXX.xmf`).
  2. Extrai os nós usando `ExtractNodeCoordinates()`.
  3. Se for o primeiro timestep, **salva as coordenadas no HDF5**.
  4. Para os demais timesteps, **verifica se houve mudanças na geometria**.

### 3️⃣ Armazenamento no HDF5
- O arquivo HDF5 é aberto/criado com `h5py.File(hdf5_file, "a")`.
- Se o dataset `nodes` não existir, ele será criado no primeiro timestep.
- Em timesteps subsequentes, os dados são comparados com os armazenados:
  - Se forem diferentes, uma mensagem de **alteração detectada** será exibida.
  - Se forem iguais, o script informa que a **geometria não mudou**.

## 📂 Saída
- O script gera um arquivo `.h5` contendo a geometria inicial:
```bash
TANQUE_NODES.h5
```
Os dados podem ser carregados no Python com:
```python
import h5py
with h5py.File("TANQUE_NODES.h5", "r") as f:
    print(f["nodes"].shape)  # Exibe a forma dos dados
```


