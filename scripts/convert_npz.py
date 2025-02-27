import h5py
import numpy as np
import sys

def convert_to_npz(hdf5_file: str, dataset:str):

    with h5py.File(hdf5_file, 'r') as f:
        if dataset not in f:
            print(f"❌ Dataset '{dataset}' não encontrado!")
            sys.exit(1)

        data = f[dataset][:]

        npz_file_name = hdf5_file.split(".")[0] + ".npz"

        # Salvar arquivo NPZ compressionado
        np.savez_compressed(f"{npz_file_name}.npz", data=data)

        print(f"✅ Arquivo '{npz_file_name}.npz' salvo com sucesso!")

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("❌ Uso incorreto! Execute: python convert_npz.py <arquivo.h5> <dataset>")
        sys.exit(1)

    hdf5_file = sys.argv[1]
    dataset = sys.argv[2]

    convert_to_npz(hdf5_file, dataset)

# Usage: python convert_npz.py <arquivo.h5> <dataset>
# Exemplo: python convert_npz.py arquivo.h5 data    
