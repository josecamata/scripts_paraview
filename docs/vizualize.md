# Documentação do Script `vizualize.py`

## 📌 Descrição
Este script lê dados de **coordenadas de nós** e **valores de deposição** de arquivos **HDF5 (`.h5`)** e gera uma visualização gráfica utilizando **Matplotlib**. O resultado é salvo como uma imagem `.png` representando a deposição em um determinado **timestep**.

## 🛠️ Requisitos
- Python
- Biblioteca `h5py` para manipulação de arquivos HDF5
- Biblioteca `NumPy` para manipulação de dados
- Biblioteca `Matplotlib` para visualização

## 🚀 Como Executar
O script pode ser executado da seguinte forma:
```bash
python vizualize.py <coord_file.h5> <dataset_file.h5> <time_step>
```

### 📌 Exemplo de Uso:
```bash
python vizualize.py nodes.h5 deposition_data.h5 10
```
📌 Isso carregará os arquivos `nodes.h5` e `deposition_data.h5`, extraindo os dados para o **timestep 10** e gerando uma visualização da deposição.

## 🔹 Estrutura do Script
### 1️⃣ `vizualize(coord_file: str, dataset_file: str, time_step: int)`
Esta função carrega os arquivos HDF5 e gera um **mapa de deposição** a partir dos dados.

#### 🔹 Parâmetros:
- `coord_file` (str): Caminho do arquivo HDF5 contendo as **coordenadas dos nós**.
- `dataset_file` (str): Caminho do arquivo HDF5 contendo os **dados de deposição**.
- `time_step` (int): Índice do timestep a ser visualizado.

#### 🔹 Processo:
1. **Abrir os arquivos HDF5**
   - Verifica se os arquivos foram carregados corretamente.
   - Se não existirem, o script encerra com erro.
2. **Verificar a existência dos datasets necessários**
   - O dataset `nodes` deve estar presente no arquivo de coordenadas.
   - O dataset `data` deve estar presente no arquivo de deposição.
3. **Extrair os dados**
   - Obtém os **valores das coordenadas** X e Y dos nós.
   - Obtém os **valores de deposição** para o timestep desejado.
4. **Gerar o gráfico de deposição**
   - Utiliza `matplotlib.pyplot.tricontourf()` para criar um **mapa de contorno colorido**.
   - Usa a coloração `rainbow` para melhor visualização dos níveis de deposição.
   - Adiciona uma **barra de cores** para referência.
   - Define **título, eixos X e Y**.
5. **Salvar a imagem gerada**
   - O gráfico é salvo como `deposition_<time_step>.png` no diretório atual.
6. **Fechar os arquivos HDF5**
   - O script fecha corretamente os arquivos ao final do processamento.

## 📂 Saída
O script gera uma **imagem `.png`** contendo a visualização da deposição para o timestep escolhido:
```bash
deposition_10.png
```

### **Exemplo de Saída**:
```
📂 Carregando arquivo HDF5: deposition_data.h5
Arquivo nodes.h5 aberto com sucesso
Arquivo deposition_data.h5 aberto com sucesso
Dimensões de 'nodes': (1000, 3)
Dimensões de 'data': (1000, 50)
✅ Imagem salva como deposition_10.png
```


