import sys
from paraview.simple import *




def ComputeDepositionInBlocks(file_path: str, output_dir="deposition_output_vtu", start_index=1, end_index=2):

    from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkVertex
    from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints, vtkIdList
    from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
    import numpy as np
    import os, gc

    os.makedirs(output_dir, exist_ok=True)

    reader = XDMFReader(FileNames=[file_path])
    reader.PointArrayStatus = ['s_dep_01            ']
    timesteps = reader.TimestepValues

    N = len(timesteps)
    if( start_index < 0 or end_index > N or start_index >= end_index):
        raise ValueError("Índices inválidos para os timesteps. Verifique os valores de start_index e end_index.")
    if N < 2:
        raise ValueError("Arquivo deve conter pelo menos 2 timesteps.")

    print(f"📈 {N} timesteps encontrados.")
    geometry = None
    idx_out = 0

    block_size = end_index - start_index
    if block_size <= 0:
        raise ValueError("Tamanho do bloco deve ser maior que zero.")

    start_index = max(0, start_index)
    end_index   = min(N, end_index)

    times_block = timesteps[start_index:end_index]
    s_fields = []

    print(f"\n🔁 Processando bloco de t={times_block[0]:.3f} até t={times_block[-1]:.3f}")

    for t in times_block:
        print(f"⏳ Processando timestep: {t}")

        reader.UpdatePipeline(time=t)
        merged  = MergeBlocks(Input=reader)
        clean   = CleantoGrid(Input=merged)
        surface = ExtractSurface(Input=clean)
        clip    = Clip(Input=surface)
        clip.ClipType = 'Box'
        clip.ClipType.Position = [5.0, -5.0, -1.0]
        clip.ClipType.Length = [15.0, 10.0, 2.0]
        clip.Scalars = ['POINTS', 's_dep_01            ']

        data = servermanager.Fetch(clip)
        if data.IsA("vtkMultiBlockDataSet"):
            data = data.GetBlock(0)

        array = data.GetPointData().GetArray('s_dep_01            ')
        values = np.array([array.GetValue(i) for i in range(array.GetNumberOfTuples())], dtype=np.float32)
        s_fields.append(values)

        if geometry is None:
            geometry = np.array([data.GetPoint(i) for i in range(data.GetNumberOfPoints())])

        del merged, clean, surface, clip, data, array
        gc.collect()

    # Gera arquivos VTU para pares consecutivos
    index_out = start_index
    for k in range(len(s_fields) - 1):
        t0 = times_block[k]
        t1 = times_block[k + 1]
        delta_t = t1 - t0
        rate = (s_fields[k + 1] - s_fields[k]) / delta_t

        # Criar grid
        ug = vtkUnstructuredGrid()

        # Pontos
        pts = vtkPoints()
        pts.SetNumberOfPoints(len(geometry))
        for j, pt in enumerate(geometry):
            pts.SetPoint(j, pt)
        ug.SetPoints(pts)

        # Células (cada ponto vira uma célula tipo VERTEX)
        for j in range(len(geometry)):
            id_list = vtkIdList()
            id_list.InsertNextId(j)
            ug.InsertNextCell(vtkVertex().GetCellType(), id_list)

        # Campo de taxa
        rate_array = vtkFloatArray()
        rate_array.SetName("deposition_rate")
        rate_array.SetNumberOfComponents(1)
        rate_array.SetNumberOfTuples(len(rate))
        for j, val in enumerate(rate):
            rate_array.SetValue(j, val)
        ug.GetPointData().AddArray(rate_array)

        # # Campo de tempo
        # time_array = vtkFloatArray()
        # time_array.SetName("TimeValue")
        # time_array.SetNumberOfComponents(1)
        # time_array.SetNumberOfTuples(len(rate))
        # for j in range(len(rate)):
        #     time_array.SetValue(j, t1)
        # ug.GetPointData().AddArray(time_array)

            # Escrita
        filename = os.path.join(output_dir, f"deposition_idx_{index_out:04d}_t_{t1:.3f}.vtu")
        writer = vtkXMLUnstructuredGridWriter()
        writer.SetFileName(filename)
        writer.SetInputData(ug)
        writer.Write()

        print(f"✅ {filename}")
        index_out += 1


def generate_pvd_from_vtu(output_dir, pvd_filename="deposition_series.pvd"):
    import os
    import re

    # Regex para extrair timestep do nome do arquivo
    vtu_pattern = re.compile(r"deposition__t_(\d+\.\d+)_idx_(\d+)\.vtu")

    entries = []
    for filename in sorted(os.listdir(output_dir)):
        match = vtu_pattern.match(filename)
        if match:
            time_val = float(match.group(1))
            entries.append((time_val, filename))

    # Ordenar por tempo (opcional, mas recomendável)
    entries.sort()

    # Criar XML do PVD
    pvd_path = os.path.join(output_dir, pvd_filename)
    with open(pvd_path, "w") as f:
        f.write('<?xml version="1.0"?>\n')
        f.write('<VTKFile type="Collection" version="0.1" byte_order="LittleEndian">\n')
        f.write('  <Collection>\n')
        for time_val, filename in entries:
            f.write(f'    <DataSet timestep="{time_val}" group="" part="0" file="{filename}"/>\n')
        f.write('  </Collection>\n')
        f.write('</VTKFile>\n')

    print(f"📁 Arquivo .pvd gerado em: {pvd_path}")


if len(sys.argv) < 5:
    print("❌ Erro: Argumentos insuficientes! Use: pvpython deposition_rate.py <xdmf_file> <output_dir> <start_index> <end_index>")
    print("Exemplo: pvpython deposition_rate.py data.xdmf deposition_output 0 10")
    sys.exit(1)

xdmf_file = sys.argv[1]
output_dir = sys.argv[2]
start_index = int(sys.argv[3])
end_index = int(sys.argv[4])

ComputeDepositionInBlocks(xdmf_file, output_dir, start_index, end_index)
generate_pvd_from_vtu(output_dir)


