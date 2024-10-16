import os
import shutil
import datetime
import tempfile
import zipfile
from tqdm import tqdm

# Configuraciones iniciales
source_volume = "A:\\"  # Volumen del que se desea respaldar (puedes cambiarlo)
destination_path = r"\\GABONET\Gabo\Respaldos"  # Ruta de destino en la red

# Obtener la fecha y la hora actuales para usar en el nombre del archivo
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_filename = f"backup_{current_datetime}.zip"
backup_filepath = os.path.join(destination_path, backup_filename)

def compress_folders(source, output_file):
    """
    Comprime todas las carpetas del volumen especificado y crea un archivo ZIP.
    :param source: Volumen o carpeta a comprimir.
    :param output_file: Ruta completa del archivo ZIP de salida.
    """
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

        with zipfile.ZipFile(temp_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path, arcname in tqdm(files_to_compress, desc="Comprimiendo archivos", unit="archivo"):
                try:
                    zipf.write(file_path, arcname)
                except PermissionError as e:
                    print(f"Error de permiso al acceder al archivo {file_path}: {e}")
        shutil.move(temp_zip_path, output_file)
    print("Compresión completada.")

def main():
    # Crear el respaldo comprimido
    compress_folders(source_volume, backup_filepath)
    print(f"Respaldo creado exitosamente en: {backup_filepath}")

if __name__ == "__main__":
    main()