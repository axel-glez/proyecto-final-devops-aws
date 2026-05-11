#!/bin/bash

LOG_DIR="/var/log"
DIAS=7

echo "Iniciando limpieza de logs mayores a $DIAS días en $LOG_DIR"

sudo find "$LOG_DIR" -type f -name "*.log" -mtime +$DIAS -print

sudo find "$LOG_DIR" -type f -name "*.log" -mtime +$DIAS -exec rm -f {} \;

echo "Limpieza de logs completada."
