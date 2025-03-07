# Documentação do Script `compare_hdf5.py`

## 📌 Descrição
Este script compara dois arquivos **HDF5 (`.h5`)** e verifica **diferenças nos datasets** presentes em cada um. Ele também compara os dados armazenados nos datasets comuns, identificando **diferenças dimensionais e numéricas**.

## 🛠️ Requisitos
- Python
- Biblioteca `h5py` para manipulação de arquivos HDF5
- Biblioteca `NumPy` para comparação de dados

## 🚀 Como Executar
O script pode ser executado da seguinte forma:
```bash
python compare_hdf5.py <arquivo1.h5> <arquivo2.h5>
```

### 📌 Exemplo de Uso:
```bash
python compare_hdf5.py dados1.h5 dados2.h5
```
📌 Isso comparará os arquivos `dados1.h5` e `dados2.h5`, exibindo as diferenças encontradas.

## 🔹 Estrutura do Script
### 1️⃣ `compare_hdf5(file1, file2)`
Esta função carrega os arquivos HDF5 e realiza a comparação entre os datasets.

#### 🔹 Parâmetros:
- `file1` (str): Caminho do primeiro arquivo HDF5.
- `file2` (str): Caminho do segundo arquivo HDF5.

#### 🔹 Processo:
1. **Carrega os arquivos HDF5**
   - Usa `h5py.File(file, 'r')` para abrir os arquivos somente leitura.
2. **Verifica a presença de datasets diferentes**
   - Identifica quais datasets estão presentes apenas em um dos arquivos.
3. **Compara os dados dos datasets comuns**
   - Exibe as **dimensões dos dados** em ambos os arquivos.
   - Verifica se as dimensões dos datasets são **idênticas**.
   - Compara a **primeira coluna** dos datasets usando `np.array_equal()`.
   - Caso os dados sejam diferentes, exibe a **diferença máxima** entre eles.

### 2️⃣ Verificação de Diferenças
- O script primeiro verifica **se ambos os arquivos contêm os mesmos datasets**.
- Se um dataset existir em ambos os arquivos, o script compara **dimensões e valores**.
- A diferença é calculada apenas na **primeira coluna** dos datasets.

## 📂 Saída
O script imprime mensagens indicando:
✅ Se os arquivos possuem os mesmos datasets.  
⚠️ Se existem datasets presentes apenas em um dos arquivos.  
❌ Se os datasets possuem **dimensões diferentes**.  
❌ Se há **diferenças nos valores armazenados**.  

### **Exemplo de Saída**:
```
✅ Ambos os arquivos contêm os mesmos conjuntos de dados.
Dimensões em 'dados1.h5': (100, 5)
Dimensões em 'dados2.h5': (100, 5)
✅ Dataset 'medidas' é idêntico nos dois arquivos.
❌ Dataset 'valores' possui diferenças!
Diferença máxima: 0.0021
```
