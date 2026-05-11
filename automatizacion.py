import boto3
from datetime import datetime, timedelta, timezone

REGION = "us-east-1"

ec2 = boto3.client("ec2", region_name=REGION)
cloudwatch = boto3.client("cloudwatch", region_name=REGION)
s3 = boto3.client("s3", region_name=REGION)
autoscaling = boto3.client("autoscaling", region_name=REGION)


def listar_instancias_ec2():
    print("\n========== INSTANCIAS EC2 ==========")

    response = ec2.describe_instances()

    if not response["Reservations"]:
        print("No se encontraron instancias EC2.")
        return

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance.get("InstanceId", "N/A")
            instance_type = instance.get("InstanceType", "N/A")
            state = instance.get("State", {}).get("Name", "N/A")

            print(f"ID: {instance_id} | Tipo: {instance_type} | Estado: {state}")


def reporte_cpu_ec2():
    print("\n========== REPORTE CPU EC2 ULTIMAS 24 HORAS ==========")

    response = ec2.describe_instances(
        Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["running"]
            }
        ]
    )

    instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append(instance["InstanceId"])

    if not instances:
        print("No hay instancias EC2 en ejecución para consultar CPU.")
        return

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=24)

    for instance_id in instances:
        metrics = cloudwatch.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[
                {
                    "Name": "InstanceId",
                    "Value": instance_id
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=["Average"]
        )

        datapoints = metrics.get("Datapoints", [])

        print(f"\nInstancia: {instance_id}")

        if not datapoints:
            print("No hay métricas disponibles todavía.")
        else:
            datapoints_ordenados = sorted(datapoints, key=lambda x: x["Timestamp"])
            for punto in datapoints_ordenados:
                timestamp = punto["Timestamp"]
                average = punto["Average"]
                print(f"{timestamp} | CPU promedio: {average:.2f}%")


def listar_buckets_s3():
    print("\n========== BUCKETS S3 Y OBJETOS ==========")

    response = s3.list_buckets()
    buckets = response.get("Buckets", [])

    if not buckets:
        print("No se encontraron buckets S3.")
        return

    for bucket in buckets:
        bucket_name = bucket["Name"]
        print(f"\nBucket: {bucket_name}")

        try:
            objects = s3.list_objects_v2(Bucket=bucket_name)

            if "Contents" not in objects:
                print("  Sin objetos.")
            else:
                for obj in objects["Contents"]:
                    print(f"  Objeto: {obj['Key']} | Tamaño: {obj['Size']} bytes")
        except Exception as e:
            print(f"  No se pudieron listar objetos: {e}")


def listar_auto_scaling_groups():
    print("\n========== AUTO SCALING GROUPS ==========")

    response = autoscaling.describe_auto_scaling_groups()
    groups = response.get("AutoScalingGroups", [])

    if not groups:
        print("No se encontraron grupos de Auto Scaling.")
        return

    for group in groups:
        name = group.get("AutoScalingGroupName", "N/A")
        min_size = group.get("MinSize", "N/A")
        max_size = group.get("MaxSize", "N/A")
        desired = group.get("DesiredCapacity", "N/A")

        print(f"Grupo: {name} | Min: {min_size} | Max: {max_size} | Deseada: {desired}")


if __name__ == "__main__":
    print("Iniciando automatización AWS con boto3...")
    listar_instancias_ec2()
    reporte_cpu_ec2()
    listar_buckets_s3()
    listar_auto_scaling_groups()
    print("\nAutomatización finalizada.")
