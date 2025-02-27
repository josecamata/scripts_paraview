import h5py
import numpy as np
import sys
import matplotlib.pyplot as plt

def vizualize(coord_file: str, dataset_file: str, time_step: int):
    """
    Visualiza os dados de um arquivo HDF5.
    """
    print(f"📂 Carregando arquivo HDF5: {dataset_file}")

    file1 =h5py.File(coord_file, 'r')
    # verifica se file1 esta aberto
    if file1:
        print(f"Arquivo {coord_file} aberto com sucesso")
    else:
        print(f"Erro ao abrir arquivo {coord_file}")
        sys.exit(1)

    file2 = h5py.File(dataset_file, 'r')
    # verifica se file2 esta aberto
    if file2:
        print(f"Arquivo {dataset_file} aberto com sucesso")
    else:
        print(f"Erro ao abrir arquivo {dataset_file}")
        sys.exit(1)

    # Verificar se o dataset existe
    if "nodes" not in file1:
        print("❌ Dataset 'nodes' não encontrado!")
        sys.exit(1)
    if "data" not in file2:
        print("❌ Dataset 'data' não encontrado!")
        sys.exit(1)

    # Obter os dados
    nodes = file1["nodes"][:]
    data = file2["data"][:]
    print(f"Dimensões de 'nodes': {nodes.shape}")
    print(f"Dimensões de 'data': {data.shape}")

    # obter primeira coluna de nodes
    x = nodes[:,0]
    y = nodes[:,1]

    # obter dados de deposicao
    s_dep = data[:,time_step]


    plt.figure(figsize=(10, 5))
    plt.tricontourf(x, y, s_dep, levels=40, cmap="rainbow")
    #plt.scatter(x, y, c=s_dep, cmap='viridis')
    plt.colorbar()
 

    plt.title(f"Deposição no passo de tempo {time_step}")
    plt.xlabel("X")
    plt.ylabel("Y")
    # plt.show()

    # salvar a imagem em formato png
    plt.savefig(f"deposition_{time_step}.png")

    # fechar os arquivos
    file1.close()
    file2.close()



if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("❌ Uso incorreto! Execute: python vizualize.py <coord_file.h5> <dataset_file.h5> <time_step>")
        sys.exit(1)

    coord_file = sys.argv[1]
    dataset_file = sys.argv[2]
    time_step = int(sys.argv[3])

    vizualize(coord_file, dataset_file, time_step)

