
import h5py
import numpy as np
import sys

def compare_hdf5(file1, file2):
    """
    Compara dois arquivos HDF5 e exibe as diferenças nos datasets.
    """
    with h5py.File(file1, 'r') as f1, h5py.File(file2, 'r') as f2:
        datasets1 = set(f1.keys())
        datasets2 = set(f2.keys())

        # Comparar nomes dos datasets
        if datasets1 != datasets2:
            print("⚠️ Os arquivos possuem conjuntos de dados diferentes!")
            print("Presentes apenas em", file1, ":", datasets1 - datasets2)
            print("Presentes apenas em", file2, ":", datasets2 - datasets1)
        else:
            print("✅ Ambos os arquivos contêm os mesmos conjuntos de dados.")

        # Comparar conteúdo dos datasets
        for dataset in datasets1.intersection(datasets2):
           

            data1 = f1[dataset][:]
            data2 = f2[dataset][:]

            print(f"Dimensões em '{file1}': {data1.shape}")
            print(f"Dimensões em '{file2}': {data2.shape}")

            if data1.shape != data2.shape:
                print(f"❌ Dataset '{dataset}' possui dimensões diferentes!")

    
            if np.array_equal(data1[:,:2], data2[:,:2]):
                print(f"✅ Dataset '{dataset}' é idêntico nos dois arquivos.")
            else:
                print(f"❌ Dataset '{dataset}' possui diferenças!")
                print(f"Diferença máxima: {np.max(np.abs(data1[:,:2] - data2[:,:2]))}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("❌ Uso incorreto! Execute: python compare_hdf5.py <arquivo1.h5> <arquivo2.h5>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    compare_hdf5(file1, file2)
