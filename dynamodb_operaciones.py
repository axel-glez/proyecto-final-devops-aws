import boto3
from botocore.exceptions import ClientError

REGION = "us-east-1"
TABLE_NAME = "devops-tabla"

dynamodb = boto3.resource("dynamodb", region_name=REGION)
client = boto3.client("dynamodb", region_name=REGION)


def crear_tabla():
    try:
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    "AttributeName": "id",
                    "KeyType": "HASH"
                }
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "id",
                    "AttributeType": "S"
                }
            ],
            BillingMode="PAY_PER_REQUEST"
        )

        print(f"Creando tabla {TABLE_NAME}...")
        table.wait_until_exists()
        print("Tabla creada correctamente.")

    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print("La tabla ya existe, se continuará con las operaciones.")
        else:
            raise


def insertar_registro():
    table = dynamodb.Table(TABLE_NAME)

    table.put_item(
        Item={
            "id": "1",
            "nombre": "Soluciones Tecnologicas del Futuro",
            "status": "creado"
        }
    )

    print("Registro insertado correctamente.")


def actualizar_registro():
    table = dynamodb.Table(TABLE_NAME)

    table.update_item(
        Key={
            "id": "1"
        },
        UpdateExpression="SET #st = :nuevo_status",
        ExpressionAttributeNames={
            "#st": "status"
        },
        ExpressionAttributeValues={
            ":nuevo_status": "actualizado"
        }
    )

    print("Registro actualizado correctamente.")


def eliminar_registro():
    table = dynamodb.Table(TABLE_NAME)

    table.delete_item(
        Key={
            "id": "1"
        }
    )

    print("Registro eliminado correctamente.")


def describir_tabla():
    response = client.describe_table(TableName=TABLE_NAME)
    table = response["Table"]

    print("\nInformación de la tabla:")
    print(f"Nombre: {table['TableName']}")
    print(f"Estado: {table['TableStatus']}")
    print(f"Modo de facturación: {table.get('BillingModeSummary', {}).get('BillingMode', 'N/A')}")


if __name__ == "__main__":
    crear_tabla()
    describir_tabla()
    insertar_registro()
    actualizar_registro()
    eliminar_registro()
    print("Operaciones DynamoDB completadas.")
