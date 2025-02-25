from paraview.simple import *
import numpy as np
import os
import sys
import gc
import h5py

def ExtractDep(file_path: str):
    print(f"📂 Carregando arquivo XDMF: {file_path}")
    
    # 📂 Carregar arquivo XDMF
    xdmf_reader = XDMFReader(FileNames=[file_path])
    xdmf_reader.PointArrayStatus = ['s_dep_01            ']  # Campo de sedimento

    # 🟢 Criar uma Render View se não houver uma ativa
    renderView = GetActiveViewOrCreate("RenderView")
    renderView.Update()

    # get time steps
    timesteps = xdmf_reader.TimestepValues
    time = timesteps[0]

    # create a new 'Merge Blocks'
    mergeBlocks1 = MergeBlocks(Input=xdmf_reader)

    # apply clean to grid to remove any duplicate points
    cleanToGrid1 = CleantoGrid(Input=mergeBlocks1)

    #extract surface
    extractSurface1 = ExtractSurface(Input=cleanToGrid1)

    # create a new 'Clip'
    clip1 = Clip(Input=extractSurface1)
    clip1.ClipType = 'Box'
    clip1.Scalars = ['POINTS', 's_dep_01            ']
    # Properties modified on clip1.ClipType
    clip1.ClipType.Position = [5.0, -5.0, -1.0]
    clip1.ClipType.Length  = [15.0, 10.0, 2.0]

    # update the view to ensure updated data information
    renderView.Update()

    # extract s_dep_01  as a numpy array
    data = servermanager.Fetch(clip1)

    if data.IsA("vtkMultiBlockDataSet") and data.GetNumberOfBlocks() > 0:
        print("MultiBlock")
        data = data.GetBlock(0)


    points = data.GetPointData().GetArray('s_dep_01            ')
    s_dep_01 = np.array([points.GetValue(i) for i in range(points.GetNumberOfTuples())], dtype=np.float32)

    print(f"Processing time {time} - Máx s_dep_01: {np.max(s_dep_01)}")

    del xdmf_reader, mergeBlocks1, cleanToGrid1, extractSurface1, clip1, data, points
    gc.collect()

    return time, s_dep_01

if len(sys.argv) < 3:
    print("❌ Erro: Argumentos insuficientes! Use: python extrai_dep.py <initial_time> <final_time>")
    sys.exit(1)
    
initial_time = int(sys.argv[1])
final_time   = int(sys.argv[2])

# 🔹 Defina o caminho do arquivo XDMF (alterar se necessário)
dir_path  = "/media/camata/E4E02587E02560D2/DadosSimulacao/tanque_p1/"
hdf5_file = "TANQUE_P1_DEP.h5"

# Criar/abrir arquivo HDF5
with h5py.File(hdf5_file, "a") as h5f:
    for time in range(initial_time, final_time + 1):
        file_path = f"{dir_path}tanque_{str(time).zfill(5)}.xmf"
        print(f"🔍 Processando: {file_path}")

        time, s_dep = ExtractDep(file_path)  # Função para extrair os dados do arquivo XDMF

        # 🔹 Garantir que s_dep tenha formato (n, 1)
        s_dep = s_dep.reshape(-1, 1)

        # 🔹 Salvar de forma incremental
        if "data" in h5f:
            existing_data = h5f["data"]
            if existing_data.shape[0] == s_dep.shape[0]:
                new_data = np.hstack((existing_data[:], s_dep))
                del h5f["data"]  # Remove dataset antigo
                h5f.create_dataset("data", data=new_data)
            else:
                print(f" Tamanho incompatível no timestep {time}. Pulando...")
        else:
            h5f.create_dataset("data", data=s_dep)

        del s_dep
        gc.collect()

print(f"✅ Arquivo salvo com sucesso: {hdf5_file}")