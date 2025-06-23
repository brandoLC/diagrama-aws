import json
import base64
import tempfile
import os
import sys
from io import BytesIO

def generar_diagrama(event, context):
    """
    Función Lambda que simula la generación de diagramas
    (para demo sin dependencias de Graphviz)
    """
    try:
        # Parsear el body del request
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        # Obtener el código del diagrama
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
                'body': json.dumps({
                    'error': 'El campo "codigo" es requerido'
                })
            }
        
        # Por ahora, devolver un placeholder hasta que resolvamos Graphviz
        # Crear una imagen simple de placeholder
        import io
        from PIL import Image, ImageDraw, ImageFont
        
        # Crear imagen de placeholder
        img = Image.new('RGB', (800, 600), color='white')
        draw = ImageDraw.Draw(img)
        
        # Dibujar texto
        try:
            # Intentar usar una fuente por defecto
            font = ImageFont.load_default()
        except:
            font = None
            
        draw.text((50, 50), "Diagrama Generado", fill='black', font=font)
        draw.text((50, 100), "Código recibido:", fill='black', font=font)
        
        # Mostrar las primeras líneas del código
        lines = codigo_diagrama.split('\n')[:10]
        y_pos = 150
        for line in lines:
            if len(line) > 80:
                line = line[:80] + "..."
            draw.text((50, y_pos), line, fill='blue', font=font)
            y_pos += 30
        
        draw.text((50, 500), "✅ API funcionando correctamente", fill='green', font=font)
        draw.text((50, 530), "🔧 Graphviz será agregado próximamente", fill='orange', font=font)
        
        # Convertir a bytes
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_bytes = img_buffer.getvalue()
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
                'mensaje': 'Placeholder generado exitosamente. Graphviz será agregado pronto.'
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
