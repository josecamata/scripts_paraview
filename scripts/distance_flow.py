from paraview.simple import *
import numpy as np
import sys

def GetDataFromXDMFFile(file_path: str):

    print(f"Carregando arquivo XDMF: {file_path}")

    # 📂 Carregar arquivo XDMF
    xdmf_reader = XDMFReader(FileNames=[file_path])
    xdmf_reader.PointArrayStatus = ['s_dep_01            ']  # Campo de sedimento

    # get time steps
    timesteps = xdmf_reader.TimestepValues
    time = timesteps[0]


    # 🟢 Criar uma Render View se não houver uma ativa
    renderView = GetActiveViewOrCreate("RenderView")
    renderView.Update()

    # 🟢 Aplicar filtro "Extract Surface"
    extract_surface = ExtractSurface(Input=xdmf_reader)

    # 🟢 Aplicar filtro "Calculator" para calcular distância X
    calculator_x = Calculator(Input=extract_surface)
    calculator_x.ResultArrayName = 'distance_x'
    calculator_x.Function = 'coordsX*("s_dep_01            ">0.0005?1:0)'

    # 🟢 Aplicar filtro "Calculator" para calcular distância X
    calculator_y = Calculator(Input=extract_surface)
    calculator_y.ResultArrayName = 'distance_y'
    calculator_y.Function = 'coordsY*("s_dep_01            ">0.0005?1:0)'

    # 🔹 Atualizar a cena para garantir que os dados estão processados
    renderView.Update()

    # 🔹 Obtém os dados para análise
    data_x = servermanager.Fetch(calculator_x)

    max_distance_x_all = []

    for i in range(data_x.GetNumberOfBlocks()):
        
        data_x_block = data_x.GetBlock(i)

        if not data_x_block:
            continue

        # 🟢 Obtém o campo "distance_x"
        points_x = data_x_block.GetPointData().GetArray('distance_x')

        # 🏁 Calcula a distância máxima da frente do escoamento
        max_distance_x = np.max([points_x.GetValue(i) for i in range(points_x.GetNumberOfTuples())])

        max_distance_x_all.append(max_distance_x)


    # 🔹 Obtém os dados para análise
    data_y = servermanager.Fetch(calculator_y)

    max_distance_y_all = []
    min_distance_y_all = []

    for i in range(data_y.GetNumberOfBlocks()):
        
        data_y_block = data_y.GetBlock(i)

        if not data_y_block:
            continue

        # 🟢 Obtém o campo "distance_x"
        points_y = data_y_block.GetPointData().GetArray('distance_y')

        # 🏁 Calcula a distância máxima da frente do escoamento
        max_distance_y = np.max([points_y.GetValue(i) for i in range(points_y.GetNumberOfTuples())])
        min_distance_y = np.min([points_y.GetValue(i) for i in range(points_y.GetNumberOfTuples())])
  
        max_distance_y_all.append(max_distance_y)
        min_distance_y_all.append(min_distance_y)

    # obter o máximo de max_distance_x
    max_distance_x = max(max_distance_x_all)
    # Exibe o resultado final
    print(f" Distância máxima da frente do escoamento: {max_distance_x}")
    max_distance_y = max(max_distance_y_all)
    min_distance_y = min(min_distance_y_all)
    largura        = max_distance_y - min_distance_y
    print(f" Largura máxima do escoamento: {largura}")

    # 🔹 Atualizar a visualização
    renderView.Update()

    return time, max_distance_x, largura

if(len(sys.argv) < 4):
    print("Usage: pypython distance_flow.py <dir_path> <prefix_file_name> <csv_file>")
    sys.exit(1)

dir_path         = sys.argv[1] # diretório onde estão os arquivos
prefix_file_name = sys.argv[2] # prefixo do nome do arquivo xdmf 
csv_file         = sys.argv[3] # nome do arquivo csv de saida

# write a csv file
with open(csv_file, 'w') as f:
    f.write("time,distance_x,largura_y\n")
initial_time = 1
final_time   = 41
for time in range(initial_time, final_time + 1):
    file_path = f"{dir_path}{prefix_file_name}_{str(time).zfill(5)}.xmf"
    print(file_path)
    time, distance_x, largura_y = GetDataFromXDMFFile(file_path)
    # write a csv file
    with open(csv_file, 'a') as f:
        f.write(f"{time},{max_distance_x},{largura}\n")

