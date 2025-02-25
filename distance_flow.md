# Documentação do Script `distance_flow.py`

## Descrição
Este script processa arquivos XDMF e extrai informações sobre a distância máxima da frente do escoamento e a largura máxima do escoamento ao longo do tempo. Ele utiliza o ParaView para manipulação e extração de dados dos arquivos XDMF.

## Requisitos
- Python
- Paraview (Módulo `paraview.simple`)
- NumPy

## Como Executar
1. Ajuste o caminho do diretório e dos arquivos XDMF, caso necessário.
2. Execute o script no terminal:
   ```bash
   pvpython distance_flow.py
   ```
3. O script processará os arquivos e gerará um arquivo CSV com os resultados.

## Estrutura do Script
### 1. `GetDataFromXDMFFile(file_path: str)`
Esta função processa um arquivo XDMF e extrai informações sobre a distância da frente do escoamento.

#### Parâmetros:
- `file_path` (str): Caminho para o arquivo XDMF.

#### Retorno:
- `time` (float): Tempo do timestep processado.
- `max_distance_x` (float): Distância máxima da frente do escoamento.
- `largura` (float): Largura máxima do escoamento.

#### Processo:
1. Carrega o arquivo XDMF.
2. Aplica filtros para extrair superfície e calcular distâncias X e Y.
3. Obtém a distância máxima em X e a largura em Y.
4. Retorna os valores extraídos.

### 2. Loop Principal
- Define o diretório e o arquivo CSV de saída.
- Processa os arquivos XDMF dentro do intervalo de `initial_time` a `final_time`.
- Salva os resultados no arquivo `distance_block.csv`.

## Saída
- O script gera um arquivo CSV contendo:
  ```csv
  time,max_distance_x,largura_y
  1,12.5,5.3
  2,13.0,5.5
  ...
  ```


