import json
import random

def lambda_handler(event, context):
    mensajes = [
        "Despliegue DevOps ejecutado correctamente.",
        "Microservicio activo en AWS Lambda.",
        "Automatización completada con buenas prácticas DevOps.",
        "Soluciones Tecnológicas del Futuro opera en la nube.",
        "Pipeline CI/CD integrado con AWS y GitHub Actions.",
        "Monitoreo y seguridad aplicados en el entorno AWS."
    ]

    respuesta = {
        "mensaje": random.choice(mensajes),
        "servicio": "microservicio-devops"
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(respuesta)
    }
