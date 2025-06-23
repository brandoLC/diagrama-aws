#!/bin/bash

echo "🔧 Creando capa de Graphviz para AWS Lambda..."

# Crear directorio para la capa
mkdir -p layers/graphviz-layer
cd layers/graphviz-layer

# Crear estructura de directorios
mkdir -p python/lib/python3.9/site-packages
mkdir -p graphviz/bin
mkdir -p graphviz/lib

echo "📦 Instalando dependencias Python..."
# Instalar las dependencias de Python
pip install diagrams==0.23.3 graphviz==0.20.1 -t python/lib/python3.9/site-packages/

echo "⬇️ Descargando binarios de Graphviz para Amazon Linux..."
# Descargar binarios precompilados de Graphviz para Amazon Linux 2
# Estos son binarios compatibles con el runtime de Lambda
wget -q https://github.com/awslabs/aws-lambda-container-image-converter/releases/download/v0.2.4/graphviz-2.40.1-amazon-linux-2.tar.gz
tar -xzf graphviz-2.40.1-amazon-linux-2.tar.gz -C graphviz/
rm graphviz-2.40.1-amazon-linux-2.tar.gz

# Alternativamente, usar binarios de un repositorio confiable
if [ ! -f "graphviz/bin/dot" ]; then
    echo "⚠️  Descarga alternativa de binarios..."
    # Crear un directorio temporal para compilar
    mkdir -p temp-build
    cd temp-build
    
    # Usar una imagen Docker de Amazon Linux para compilar
    docker run --rm -v $(pwd):/build amazonlinux:2 bash -c "
        yum update -y && \
        yum install -y graphviz graphviz-devel && \
        cp -r /usr/bin/dot /build/ && \
        cp -r /usr/bin/neato /build/ && \
        cp -r /usr/bin/twopi /build/ && \
        cp -r /usr/bin/circo /build/ && \
        cp -r /usr/bin/fdp /build/ && \
        cp -r /usr/bin/sfdp /build/ && \
        cp -r /usr/lib64/graphviz /build/lib/ && \
        cp /usr/lib64/libgvc.so.6 /build/ && \
        cp /usr/lib64/libcgraph.so.6 /build/ && \
        cp /usr/lib64/libcdt.so.5 /build/ && \
        cp /usr/lib64/libpathplan.so.4 /build/
    "
    
    # Copiar los archivos compilados
    cp dot neato twopi circo fdp sfdp ../graphviz/bin/
    cp -r lib/* ../graphviz/lib/
    cp *.so.* ../graphviz/lib/
    
    cd ..
    rm -rf temp-build
fi

echo "🗜️ Comprimiendo capa..."
# Crear el archivo ZIP de la capa
zip -r graphviz-layer.zip python/ graphviz/

echo "✅ Capa creada exitosamente: layers/graphviz-layer/graphviz-layer.zip"
echo "📁 Tamaño de la capa: $(du -h graphviz-layer.zip | cut -f1)"

cd ../..

echo "🚀 Para desplegar la API, ejecuta: npm run deploy"
