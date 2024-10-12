import os
import shutil
import datetime
import tempfile
import zipfile

source_volume = "A:\\"
destination_path = r"\\GABONET\Gabo\Respaldos"

current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_filename = f"backup_{current_datetime}.zip"
backup_filepath = os.path.join(destination_path, backup_filename)

def compress_folders(source, output_file):
    print(f"Comprimiendo las carpetas de {source} en {output_file}...")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_zip_path = os.path.join(temp_dir, "backup_temp.zip")
        with zipfile.ZipFile(temp_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        if os.access(file_path, os.R_OK):
                            arcname = os.path.relpath(file_path, source)
                            zipf.write(file_path, arcname)
                        else:
                            print(f"Saltando archivo sin permiso: {file_path}")
                    except PermissionError as e:
                        print(f"Error de permiso al acceder al archivo {file_path}: {e}")
        shutil.move(temp_zip_path, output_file)
    print("Compresión completada.")

def main():
    compress_folders(source_volume, backup_filepath)
    print(f"Respaldo creado exitosamente en: {backup_filepath}")

if __name__ == "__main__":
    main()