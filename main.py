from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Connect to SQLite3 database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    price REAL
)
''')
conn.commit()


# CRUD operations

@app.post("/products/")
async def create_product(name: str = Form(...), description: str = Form(...), price: float = Form(...)):
    try:
        cursor.execute('''
        INSERT INTO products (name, description, price)
        VALUES (?, ?, ?)
        ''', (name, description, price))
        conn.commit()
        return {"message": "Product created successfully"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Error creating product") from e

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    try:
        cursor.execute('''
        SELECT * FROM products WHERE id=?
        ''', (product_id,))
        product = cursor.fetchone()
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"id": product[0], "name": product[1], "description": product[2], "price": product[3]}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Error retrieving product") from e

@app.put("/products/{product_id}")
async def update_product(product_id: int, name: str = Form(...), description: str = Form(...), price: float = Form(...)):
    try:
        cursor.execute('''
        UPDATE products SET name=?, description=?, price=? WHERE id=?
        ''', (name, description, price, product_id))
        conn.commit()
        return {"message": "Product updated successfully"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Error updating product") from e

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    try:
        cursor.execute('''
        DELETE FROM products WHERE id=?
        ''', (product_id,))
        conn.commit()
        return {"message": "Product deleted successfully"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Error deleting product") from e
    finally:
        conn.close()
