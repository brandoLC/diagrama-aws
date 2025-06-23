import json
import base64
import tempfile
import os
import sys
import subprocess

# Añade al PATH los binarios de Graphviz
os.environ["PATH"] = "/opt/bin:" + os.environ.get("PATH", "")
# Añade al PYTHONPATH la carpeta python/lib/python3.9/site-packages de la capa
sys.path.append('/opt/python/lib/python3.9/site-packages')

def generar_diagrama(event, context):
    try:
        # Parsear body JSON
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        codigo_diagrama = body.get('codigo', '')
        
        if not codigo_diagrama:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': json.dumps({'error': 'El campo "codigo" es requerido'})
            }
        
        # Crear directorio temporal para trabajar
        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = os.path.join(tmpdir, "script.py")
            output_path = os.path.join(tmpdir, "diagram.png")
            
            # Guardar el código recibido en script.py
            with open(script_path, "w") as f:
                f.write(codigo_diagrama)
            
            # Ejecutar el script para generar diagram.png
            subprocess.check_call([sys.executable, script_path], cwd=tmpdir)
            
            # Verificar si se generó la imagen
            if not os.path.isfile(output_path):
                return {
                    'statusCode': 500,
                    'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'error': 'No se generó la imagen del diagrama'})
                }
            
            with open(output_path, "rb") as img_file:
                img_bytes = img_file.read()
            
            imagen_base64 = base64.b64encode(img_bytes).decode('utf-8')
        
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
                'formato': 'png',
                'contentType': 'image/png',
                'tamaño': len(img_bytes),
                'mensaje': 'Diagrama generado exitosamente.'
            })
        }
    
    except subprocess.CalledProcessError as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': f'Error al ejecutar el script: {e}'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': f'Error interno: {str(e)}'})
        }


def preflight_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        },
        'body': ''
    }
