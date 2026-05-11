#!/bin/bash

echo "Creando grupo devops_group si no existe..."
sudo groupadd devops_group 2>/dev/null || echo "El grupo devops_group ya existe."

echo "Creando usuario devops_user si no existe..."
sudo useradd -m -s /bin/bash devops_user 2>/dev/null || echo "El usuario devops_user ya existe."

echo "Agregando devops_user al grupo devops_group..."
sudo usermod -aG devops_group devops_user

echo "Asignando permisos temporales sobre ~/environment..."
sudo chown -R devops_user:devops_group ~/environment

echo "Mostrando usuario y grupo creados..."
id devops_user

echo "Restaurando permisos para ec2-user..."
sudo chown -R ec2-user:ec2-user ~/environment

echo "Script de usuarios completado correctamente."
