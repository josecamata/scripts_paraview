from paraview.simple import *
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkPointData
from vtkmodules.vtkIOXML import vtkXMLPolyDataWriter
import numpy as np
import gc
import os
import sys


def ComputeDepositionSeries(file_path: str, output_dir="deposition_output"):
    print(f"📂 Lendo arquivo XDMF: {file_path}")

    # Criar pasta de saída
    os.makedirs(output_dir, exist_ok=True)

    # Abrir o leitor XDMF
    reader = XDMFReader(FileNames=[file_path])
    reader.PointArrayStatus = ['s_dep_01            ']
    timesteps = reader.TimestepValues
    print(f"📈 Total de timesteps: {len(timesteps)}")

    # Armazenar campos em cada tempo
    s_fields = []
    geometry = None

    for t in timesteps:

        print(f"⏳ Processando timestep: {t}")
        # Atualizar o pipeline para o timestep atual
        reader.UpdatePipeline(time=t)

        # Pipeline de extração
        merged  = MergeBlocks(Input=reader)
        clean   = CleantoGrid(Input=merged)
        surface = ExtractSurface(Input=clean)
        clip    = Clip(Input=surface)
        clip.ClipType = 'Box'
        clip.ClipType.Position = [5.0, -5.0, -1.0]
        clip.ClipType.Length = [15.0, 10.0, 2.0]
        clip.Scalars = ['POINTS', 's_dep_01            ']

        # Fetch para numpy
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

    # Calcular taxas e salvar arquivos VTK
    for i in range(len(timesteps) - 1):
        delta_t = timesteps[i+1] - timesteps[i]
        rate = (s_fields[i+1] - s_fields[i]) / delta_t

        # Criar PolyData
        polydata = vtkPolyData()
        from vtkmodules.vtkCommonCore import vtkPoints
        vtk_pts = vtkPoints()
        vtk_pts.SetNumberOfPoints(len(geometry))
        for j, pt in enumerate(geometry):
            vtk_pts.SetPoint(j, pt)
        polydata.SetPoints(vtk_pts)

        # Criar array escalar
        rate_array = vtkFloatArray()
        rate_array.SetName("deposition_rate")
        rate_array.SetNumberOfComponents(1)
        rate_array.SetNumberOfTuples(len(rate))
        for j, val in enumerate(rate):
            rate_array.SetValue(j, val)
        polydata.GetPointData().AddArray(rate_array)

        # Salvar arquivo
        writer = vtkXMLPolyDataWriter()
        filename = os.path.join(output_dir, f"deposition_t{i:04d}.vtp")
        writer.SetFileName(filename)
        writer.SetInputData(polydata)
        writer.Write()

        print(f"✅ Arquivo salvo: {filename}")

    print("🏁 Finalizado.")


if len(sys.argv) < 3:
    print("❌ Erro: Argumentos insuficientes! Use: pvpython deposition_rate.py <xdmf_file> <output_dir>")
    print("Exemplo: pvpython deposition_rate.py data.xdmf deposition_output")
    sys.exit(1)

xdmf_file = sys.argv[1]
output_dir = sys.argv[2]

ComputeDepositionSeries(xdmf_file, output_dir)

