#!/bin/bash

echo "Actualizando paquetes..."
sudo yum update -y

echo "Instalando dependencias necesarias..."
sudo yum install -y python3-pip git vim docker cronie

echo "Instalando boto3..."
pip3 install boto3 --user

echo "Verificando versiones..."
git --version
python3 --version
docker --version
pip3 show boto3

echo "Setup completado correctamente."
