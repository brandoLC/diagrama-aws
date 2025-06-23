import json
import base64
import tempfile
import os
import sys
from io import BytesIO

# Agregar la ruta de la capa a sys.path
sys.path.insert(0, '/opt/python')

def generar_diagrama(event, context):
    """
    Función Lambda que recibe código Python para generar diagramas
    y devuelve la imagen generada en base64
    """
    try:
        # Parsear el body del request
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        # Obtener el código del diagrama
        codigo_diagrama = body.get('codigo', '')
        formato_salida = body.get('formato', 'png')  # png, svg, pdf
        
        if not codigo_diagrama:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': json.dumps({
                    'error': 'El campo "codigo" es requerido'
                })
            }
        
        # Crear directorio temporal
        with tempfile.TemporaryDirectory() as temp_dir:
            # Cambiar al directorio temporal
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Configurar variables de entorno para Graphviz
                os.environ['PATH'] = '/opt/graphviz/bin:' + os.environ.get('PATH', '')
                os.environ['LD_LIBRARY_PATH'] = '/opt/graphviz/lib:' + os.environ.get('LD_LIBRARY_PATH', '')
                
                # Crear el namespace para ejecutar el código
                namespace = {
                    '__name__': '__main__',
                    '__file__': 'diagram.py'
                }
                
                # Importar las librerías necesarias en el namespace
                exec("""
from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS, Lambda, EC2
from diagrams.aws.database import RDS, ElastiCache
from diagrams.aws.network import ELB, APIGateway, CloudFront
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS, SNS
from diagrams.onprem.database import MySQL, PostgreSQL, MongoDB
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
""", namespace)
                
                # Ejecutar el código del usuario
                exec(codigo_diagrama, namespace)
                
                # Buscar archivos generados
                archivos_imagen = []
                for archivo in os.listdir(temp_dir):
                    if archivo.lower().endswith(('.png', '.svg', '.pdf', '.jpg', '.jpeg')):
                        archivos_imagen.append(archivo)
                
                if not archivos_imagen:
                    return {
                        'statusCode': 500,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                        },
                        'body': json.dumps({
                            'error': 'No se generó ningún archivo de imagen. Asegúrate de usar with Diagram(...): en tu código.'
                        })
                    }
                
                # Tomar el primer archivo encontrado
                archivo_imagen = archivos_imagen[0]
                ruta_imagen = os.path.join(temp_dir, archivo_imagen)
                
                # Leer el archivo y convertir a base64
                with open(ruta_imagen, 'rb') as f:
                    imagen_bytes = f.read()
                    imagen_base64 = base64.b64encode(imagen_bytes).decode('utf-8')
                
                # Determinar el tipo MIME
                extension = archivo_imagen.split('.')[-1].lower()
                mime_types = {
                    'png': 'image/png',
                    'svg': 'image/svg+xml',
                    'pdf': 'application/pdf',
                    'jpg': 'image/jpeg',
                    'jpeg': 'image/jpeg'
                }
                content_type = mime_types.get(extension, 'application/octet-stream')
                
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Methods': 'POST, OPTIONS'
                    },
                    'body': json.dumps({
                        'success': True,
                        'imagen': imagen_base64,
                        'formato': extension,
                        'contentType': content_type,
                        'tamaño': len(imagen_bytes),
                        'mensaje': f'Diagrama generado exitosamente como {archivo_imagen}'
                    })
                }
                
            finally:
                # Restaurar directorio original
                os.chdir(original_cwd)
                
    except SyntaxError as e:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f'Error de sintaxis en el código: {str(e)}'
            })
        }
    except ImportError as e:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f'Error de importación: {str(e)}. Verifica que estés usando las librerías disponibles.'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f'Error interno: {str(e)}'
            })
        }


def preflight_handler(event, context):
    """Handler para peticiones OPTIONS (CORS preflight)"""
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        },
        'body': ''
    }
