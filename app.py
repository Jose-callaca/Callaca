#Author: Gabriel Callaca

# Importar el framework flask
from flask import Flask, jsonify, request

# Importar el modulo para convertir textos en slug (url amigables)
from slugify import slugify

app =  Flask(__name__)


# Importar archivo que simula la base de daros /lista de productos
from products import products

#Ruta para hacer ping al server
@app.route('/ping')
def ping():
    return jsonify({'message': 'pong!'})


# Ruta para listar productos
@app.route('/products')
def getProducts():
    return jsonify(products)

# Ruta para buscar producto por slug
@app.route('/products/<string:slug>')
def getProduct(slug):
    productsFound = [product for product in products if product['slug'] == slug]

    if (len(productsFound) > 0) :
        return jsonify(productsFound[0])
    
    return jsonify({'message': 'Product not found'})


# Ruta para guardar producto
@app.route('/products', methods=['POST'])
def addProduct():
    nameProduct = request.json['name']
    newProduct = {
        'name': nameProduct,
        'slug': slugify(nameProduct).lower(),
        'price': request.json['price'],
        'quantity': request.json['quantity']
    }

    products.append(newProduct)

    return jsonify({'message': 'Product posted succesfully!'})


# Ruta para actualizar producto
@app.route('/products/<string:slug>', methods=['PUT'])
def updateProduct(slug):
    productsFound = [product for product in products if product['slug'] == slug]

    if (len(productsFound) > 0) :

        
        newNameProducto = request.json['name']

        productsFound[0]['name'] = newNameProducto
        productsFound[0]['slug'] = slugify(newNameProducto).lower()
        productsFound[0]['price'] = request.json['price']
        productsFound[0]['quantity'] = request.json['quantity']

        print(productsFound[0])

        return jsonify({'message': 'Product updated!'})
    
    return jsonify({'message': 'Product not found'})
        


# Ruta para eliminar producto
@app.route('/products/<string:slug>', methods=['DELETE'])
def deleteProduct(slug):
    productsFound = [product for product in products if product['slug'] == slug]

    if (len(productsFound) > 0) :

        products.remove(productsFound[0])
        return jsonify({'message': 'Product deleted!'})
    
    return jsonify({'message': 'Product not found'})





# Abrir puerto y correr el servidor python
if __name__ == '__main__':
    app.run(debug=True, port=4000)