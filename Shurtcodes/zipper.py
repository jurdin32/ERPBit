# -*- coding: utf-8 -*-
import os
import zipfile

# zippea una carpeta completa
def zipperFolder(path_out,path_folder_source):
    try:
        fantasy_zip = zipfile.ZipFile(path_out+'.zip', 'w')
        for folder, subfolders, files in os.walk(path_folder_source):
            for file in files:
                fantasy_zip.write(os.path.join(folder, file),
                                  os.path.relpath(os.path.join(folder, file), path_out),
                                  compress_type=zipfile.ZIP_DEFLATED)

        fantasy_zip.close()
        print("El proceso se completo con exito..!!")
    except Exception as error:
        print("error: ",error)

#zipea un unico archivo
def zipperOneFile(paht_out,path_source):
    try:
        jungle_zip = zipfile.ZipFile(paht_out+'.zip', 'w')
        jungle_zip.write(path_source, compress_type=zipfile.ZIP_DEFLATED)
        jungle_zip.close()
        print("El proceso se completo con exito..!!")
    except Exception as error:
        print("error: ", error)

# extraccion de archivos:
def ExtractDocs(path_out,path_file_zip):
    try:
        fantasy_zip = zipfile.ZipFile(path_file_zip)
        fantasy_zip.extractall(path_out)
        fantasy_zip.close()
        print("El proceso se completo con exito..!!")
    except Exception as error:
        print("error: ", error)


# zipperOneFile("E:\\Escritorio\\archivo","E:\\Escritorio\\REGLAMENTO INTERNO.pdf")
# zipperFolder("E:\\Escritorio\\Documentos","E:\\Escritorio\\Documentos")
ExtractDocs("E:\\Escritorio\\Documentos2","E:\\Escritorio\\docs2.zip")