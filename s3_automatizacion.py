import boto3
from datetime import datetime

REGION = "us-east-1"

s3 = boto3.client("s3", region_name=REGION)


def crear_archivo_prueba():
    nombre_archivo = "archivo_prueba_s3.txt"
    contenido = f"Archivo de prueba generado para DevOps AWS - {datetime.now()}\n"

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)

    return nombre_archivo


def subir_archivo(bucket, archivo):
    key = f"pruebas/{archivo}"
    s3.upload_file(archivo, bucket, key)
    print(f"Archivo subido correctamente: s3://{bucket}/{key}")


def listar_objetos(bucket):
    print(f"\nObjetos dentro del bucket: {bucket}")
    response = s3.list_objects_v2(Bucket=bucket)

    if "Contents" not in response:
        print("El bucket no contiene objetos.")
        return

    for obj in response["Contents"]:
        print(
            f"Nombre: {obj['Key']} | "
            f"Tamaño: {obj['Size']} bytes | "
            f"Modificado: {obj['LastModified']}"
        )


if __name__ == "__main__":
    bucket_name = input("Ingresa el nombre del bucket S3: ").strip()

    archivo = crear_archivo_prueba()
    subir_archivo(bucket_name, archivo)
    listar_objetos(bucket_name)
