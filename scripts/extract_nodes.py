from paraview.simple import *
import numpy as np
import os
import sys
import gc
import h5py

#
# Função para extrair as coordenadas dos nós de um arquivo XDMF
# @param file_path: Caminho do arquivo XDMF
# @return node_coords: Coordenadas dos nós
#

def ExtractNodeCoordinates(file_path: str):
    print(f"📂 Carregando arquivo XDMF: {file_path}")
    
    # 📂 Carregar arquivo XDMF
    xdmf_reader = XDMFReader(FileNames=[file_path])

    # Criar uma Render View
    renderView = GetActiveViewOrCreate("RenderView")
    renderView.Update()

    # Aplicar filtro "Merge Blocks"
    mergeBlocks1 = MergeBlocks(Input=xdmf_reader)

    # Aplicar filtro "Clean to Grid"
    cleanToGrid1 = CleantoGrid(Input=mergeBlocks1)

    # Extrair superfície
    extractSurface1 = ExtractSurface(Input=cleanToGrid1)

    # Criar Clip
    clip1 = Clip(Input=extractSurface1)
    clip1.ClipType = 'Box'
    clip1.ClipType.Position = [5.0, -5.0, -1.0]
    clip1.ClipType.Length = [15.0, 10.0, 2.0]

    # Atualizar a Render View
    renderView.Update()

    # Obter os dados do Clip
    data = servermanager.Fetch(clip1)

    if data.IsA("vtkMultiBlockDataSet") and data.GetNumberOfBlocks() > 0:
        print("MultiBlock encontrado, pegando primeiro bloco...")
        data = data.GetBlock(0)

    # Obter coordenadas dos nós
    points = data.GetPoints()
    node_coords = np.array([points.GetPoint(i) for i in range(points.GetNumberOfPoints())], dtype=np.float32)

    print(f"📍 Nós extraídos: {node_coords.shape[0]} coordenadas")

    # Liberar memória
    del xdmf_reader, mergeBlocks1, cleanToGrid1, extractSurface1, clip1, data, points
    gc.collect()

    return node_coords


if(len(sys.argv) < 4):
    print("Usage: python extract_nodes.py <dir_path> <prefix_file_name> <hdf5_file> [initial_time] [final_time]")
    sys.exit(1)
elif(len(sys.argv) == 4):
    initial_time = 1
    final_time = 1
else:
    initial_time = int(sys.argv[4])
    final_time = int(sys.argv[5])

dir_path          = sys.argv[1] # diretório onde estão os arquivos
prefix_file_name  = sys.argv[2] # prefixo do nome do arquivo xdmf 
hdf5_file         = sys.argv[3] # nome do arquivo csv de saida


# Criar/abrir arquivo HDF5
with h5py.File(hdf5_file, "a") as h5f:
    for time in range(initial_time, final_time + 1):
        file_path = f"{dir_path}tanque_{str(time).zfill(5)}.xmf"
        print(f"🔍 Processando: {file_path}")

        node_coords = ExtractNodeCoordinates(file_path)  # Extrai coordenadas

        if time == 1:
            # Salvar apenas a geometria do primeiro timestep
            if "nodes" not in h5f:
                h5f.create_dataset("nodes", data=node_coords, 
                                    compression="gzip",  # Aplica compressão
                                    compression_opts=4,    # Nível de compressão (1-9)
                                    chunks=True)           # Ativa chunking)
                print("Geometria inicial salva no HDF5.")
        else:
            # Verificar se as coordenadas mudaram
            saved_coords = h5f["nodes"][:]
            if not np.array_equal(saved_coords, node_coords):
                print(f"Alteração detectada no timestep {time}.")
            else:
                print(f"Geometria inalterada no timestep {time}.")

        del node_coords
        gc.collect()

