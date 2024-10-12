import os
import shutil
import datetime
import tempfile
import zipfile
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

source_volume = "A:\\"
destination_path = r"\\GABONET\Gabo\Respaldos"

current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_filename = f"backup_{current_datetime}.zip"
backup_filepath = os.path.join(destination_path, backup_filename)

def compress_file(file_path, arcname, temp_zip_path):
    try:
        with zipfile.ZipFile(temp_zip_path, 'a', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path, arcname)
    except PermissionError as e:
        return f"Error de permiso al acceder al archivo {file_path}: {e}"
    return None

def compress_folders(source, output_file):
    print(f"Comprimiendo las carpetas de {source} en {output_file}...")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_zip_path = os.path.join(temp_dir, "backup_temp.zip")
        files_to_compress = []
        for root, dirs, files in os.walk(source):
            for file in files:
                file_path = os.path.join(root, file)
                if os.access(file_path, os.R_OK):
                    files_to_compress.append((file_path, os.path.relpath(file_path, source)))
                else:
                    print(f"Saltando archivo sin permiso: {file_path}")

        print("Cantidad de nucleos disponibles para compresion: ", multiprocessing.cpu_count())
        with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            futures = [executor.submit(compress_file, file_path, arcname, temp_zip_path) for file_path, arcname in files_to_compress]
            for future in tqdm(as_completed(futures), total=len(futures), desc="Comprimiendo archivos", unit="archivo"):
                error = future.result()
                if error:
                    print(error)

        shutil.move(temp_zip_path, output_file)
    print("Compresión completada.")

def main():
    compress_folders(source_volume, backup_filepath)
    print(f"Respaldo creado exitosamente en: {backup_filepath}")

if __name__ == "__main__":
    main()