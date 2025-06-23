import json
import base64
import tempfile
import os
import sys
import subprocess

# Agrega /opt/bin al PATH para que encuentre dot y neato de la capa
os.environ["PATH"] = "/opt/bin:" + os.environ.get("PATH", "")

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
            
            # Modifica el código para que guarde el diagrama en 'diagram.png' y no muestre ventana
            codigo_modificado = (
                "from diagrams import Diagram\n"
                "from diagrams.aws.compute import Lambda\n"
                "with Diagram('Diagram', filename='diagram', outformat='png', show=False):\n"
                "    lambda_func = Lambda('Function')\n"
            )
            # Opcional: usar el código recibido, pero mejor validar o sanitizar antes
            # Aquí simplemente usamos el código recibido, debes asegurarte que genera un archivo 'diagram.png'
            # Para este ejemplo, guardamos directamente el código recibido:
            with open(script_path, "w") as f:
                f.write(codigo_diagrama)
            
            # Ejecutar el script para que genere diagram.png
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
