# E-commerce Dataset

Este directorio contiene un dataset sintético de e-commerce de alta calidad, diseñado para análisis de datos, machine learning y práctica de validación de datos. El dataset simula comportamiento realista de compras en línea, patrones de usuarios, interacciones con productos y tendencias de mercado.

**Fuente:** [Kaggle - E-commerce Dataset](https://www.kaggle.com/datasets/abhayayare/e-commerce-dataset) (CC BY-SA 4.0)  
**Generado con:** Python (Faker + NumPy + Pandas)

## 📁 Contenido del Dataset

| Archivo | Registros | Descripción |
|---------|-----------|-------------|
| `users.csv` | 1,000 | Perfiles de usuarios, demografía e información de registro |
| `products.csv` | 500 | Catálogo de productos con calificaciones y precios |
| `orders.csv` | 8,000 | Transacciones a nivel de pedido |
| `order_items.csv` | 16,800 | Items comprados por pedido (líneas de orden) |
| `reviews.csv` | 3,000 | Reseñas de productos escritas por clientes |

## 🔗 Relaciones entre Tablas

```
users (user_id) ──┬─< orders (user_id)
                  └─< reviews (user_id)

products (product_id) ──┬─< order_items (product_id)
                        └─< reviews (product_id)

orders (order_id) ─< order_items (order_id)
```

## 📋 Diccionario de Datos

### 1. users.csv

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `user_id` | String | Identificador único de usuario (formato: U000001) |
| `first_name` | String | Nombre del cliente |
| `last_name` | String | Apellido del cliente |
| `email` | String | Email sintético (no emails reales) |
| `signup_date` | Date | Fecha de creación de la cuenta |
| `country` | String | País de residencia |
| `city` | String | Ciudad de residencia |
| `postal_code` | String | Código postal |
| `age` | Integer | Edad del usuario |
| `gender` | String | Male / Female / Prefer not to say |
| `loyalty_tier` | String | Nivel de lealtad: None, Silver, Gold, Platinum |

### 2. products.csv

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `product_id` | String | Identificador único de producto (formato: P000001) |
| `title` | String | Título del producto |
| `brand` | String | Marca del producto |
| `category` | String | Categoría: Electronics, Clothing, Beauty, Home & Kitchen, Toys, Pet Supplies, Books |
| `price` | Float | Precio de venta en USD |
| `currency` | String | Moneda (USD) |
| `weight_g` | Integer | Peso del producto en gramos |
| `rating_avg` | Float | Calificación promedio del producto |
| `num_ratings` | Integer | Número de calificaciones recibidas |
| `inventory` | Integer | Cantidad en inventario |
| `created_at` | Date | Fecha de creación del producto |

### 3. orders.csv

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `order_id` | String | Identificador único de pedido (formato: O00000001) |
| `user_id` | String | Usuario que realizó el pedido |
| `order_datetime` | Timestamp | Marca de tiempo del pedido (ISO 8601) |
| `num_items` | Integer | Número de items en el pedido |
| `subtotal` | Float | Subtotal del pedido |
| `shipping_fee` | Float | Tarifa de envío |
| `tax` | Float | Impuestos |
| `discount_total` | Float | Descuentos aplicados |
| `total` | Float | Valor total del pedido (subtotal + shipping_fee + tax - discount_total) |
| `payment_method` | String | Credit Card, Debit Card, Paypal, UPI, COD, Gift Card |
| `order_status` | String | processing, shipped, cancelled, returned |
| `shipping_city` | String | Ciudad de envío |
| `shipping_country` | String | País de envío |

### 4. order_items.csv

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `order_id` | String | Pedido asociado |
| `product_id` | String | Producto comprado |
| `user_id` | String | Usuario que realizó la compra |
| `quantity` | Integer | Cantidad comprada |
| `unit_price` | Float | Precio por unidad |
| `discount` | Float | Descuento aplicado al item |
| `item_total` | Float | Total del item (quantity * unit_price - discount) |

### 5. reviews.csv

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `review_id` | String | Identificador único de reseña (formato: R00005420) |
| `order_id` | String | Pedido asociado a la reseña |
| `product_id` | String | Producto reseñado |
| `user_id` | String | Usuario que envió la reseña |
| `rating` | Integer | Calificación de 1 a 5 estrellas |
| `review_text` | String | Texto de la reseña sintética |
| `review_date` | Timestamp | Fecha de envío (ISO 8601) |

## 🎯 Casos de Uso

Este dataset es ideal para:

- **Validación de Datos**: Práctica de data quality checks usando Great Expectations y Pandera
- **Machine Learning**: Predicción de churn, análisis de sentimientos, sistemas de recomendación
- **Análisis de Negocio**: Market basket analysis, segmentación RFM, análisis de cohortes
- **Práctica de SQL**: Joins, funciones de ventana, agregaciones, CTEs
- **Feature Engineering**: Creación de características para modelos ML
- **A/B Testing**: Simulaciones de experimentos

## ⚠️ Notas Importantes

- **Datos Sintéticos**: Todo el dataset fue generado programáticamente. No contiene datos personales reales.
- **Calidad de Datos**: El dataset puede contener inconsistencias intencionales para práctica de limpieza y validación.
- **Inmutabilidad**: Los archivos CSV en este directorio no deben modificarse. Son la fuente de verdad para los ejercicios de validación.
- **Licencia**: CC BY-SA 4.0 - libre para uso en investigación, educación y proyectos comerciales con atribución.

## 📊 Características del Dataset

- **Realismo**: Simula patrones de comportamiento de usuarios reales
- **Variabilidad**: Incluye variación de demanda, retornos, cancelaciones
- **Timestamps**: Distribución temporal con patrones estacionales
- **Integridad Referencial**: Relaciones consistentes entre tablas (aunque pueden existir casos de prueba)
