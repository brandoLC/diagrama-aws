#!/usr/bin/env python3
"""
Script de prueba para la API de diagramas
"""

import requests
import json
import base64
from datetime import datetime

# URL de la API (cambiar después del deploy)
API_URL = "https://tu-api-id.execute-api.us-east-1.amazonaws.com/dev/generar-diagrama"

# Código de ejemplo para generar diagrama
codigo_diagrama = """
from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS, Lambda
from diagrams.aws.database import RDS, ElastiCache
from diagrams.aws.network import ELB, APIGateway
from diagrams.aws.storage import S3

with Diagram("Aplicación de Microservicios", show=False):
    api = APIGateway("API Gateway")

    with Cluster("Servicios"):
        lb = ELB("Load Balancer")
        servicios = ECS("Microservicios")

    with Cluster("Base de Datos"):
        db_principal = RDS("MySQL")
        cache = ElastiCache("Redis")

    almacen = S3("Archivos")
    procesador = Lambda("Procesamiento")

    api >> lb >> servicios
    servicios >> db_principal
    servicios >> cache
    servicios >> procesador >> almacen
"""

def probar_api():
    """Prueba la API de generación de diagramas"""
    
    payload = {
        "codigo": codigo_diagrama,
        "formato": "png"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("🚀 Enviando petición a la API...")
        response = requests.post(API_URL, json=payload, headers=headers)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print("✅ Diagrama generado exitosamente!")
                print(f"📄 Formato: {data.get('formato')}")
                print(f"📐 Tamaño: {data.get('tamaño')} bytes")
                
                # Guardar la imagen
                imagen_base64 = data.get('imagen')
                imagen_bytes = base64.b64decode(imagen_base64)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"diagrama_{timestamp}.{data.get('formato')}"
                
                with open(filename, 'wb') as f:
                    f.write(imagen_bytes)
                
                print(f"💾 Imagen guardada como: {filename}")
                
            else:
                print("❌ Error en la generación del diagrama")
                print(f"Error: {data.get('error')}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {error_data.get('error')}")
            except:
                print(f"Respuesta: {response.text}")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    print("🧪 Probando API de Diagramas")
    print("=" * 50)
    probar_api()
