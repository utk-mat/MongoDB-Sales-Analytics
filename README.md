# MongoDB Sales Data Analysis Project

## Overview

This project demonstrates storing and querying semi-structured sales data in MongoDB using Python (PyMongo). It showcases the flexibility of NoSQL databases compared to traditional relational SQL models.

## Project Goals

- ✅ Store order data as nested JSON documents (customer, product, region)
- ✅ Perform CRUD operations (Create, Read, Update, Delete)
- ✅ Query orders within specific date ranges
- ✅ Use aggregation pipelines to group sales by region and category
- ✅ Compare NoSQL flexibility vs relational SQL model

## Tech Stack

- **MongoDB**: NoSQL database for storing JSON documents
- **Python 3.7+**: Programming language
- **PyMongo**: MongoDB driver for Python
- **Pandas**: Data processing and CSV handling
- **Jupyter Notebook**: Interactive development environment

## Project Structure

```
Week7_MongoDB/
├── Amazon Sale Report(in).csv          # Source data file
├── mongodb_sales_operations.py         # Python script version
├── mongodb_sales_analysis.ipynb        # Jupyter notebook version
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## Prerequisites

1. **MongoDB Installation**
   - Install MongoDB Community Edition from [mongodb.com](https://www.mongodb.com/try/download/community)
   - Or use MongoDB Atlas (cloud) - free tier available
   - Ensure MongoDB is running on your system

2. **Python Environment**
   - Python 3.7 or higher
   - pip package manager

## Installation

1. **Clone or navigate to the project directory**

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start MongoDB** (if using local installation)
   ```bash
   # On macOS/Linux
   mongod
   
   # On Windows
   mongod.exe
   ```

## Usage

### Option 1: Jupyter Notebook (Recommended)

1. **Start Jupyter Notebook**
   ```bash
   jupyter notebook
   ```

2. **Open `mongodb_sales_analysis.ipynb`**

3. **Run cells sequentially** to:
   - Connect to MongoDB
   - Load and transform CSV data
   - Perform CRUD operations
   - Run queries and aggregations
   - View comparisons with SQL

### Option 2: Python Script

1. **Run the Python script**
   ```bash
   python mongodb_sales_operations.py
   ```

2. **Note**: The script has insert operations commented out by default. Uncomment to insert data.

## Data Structure

The CSV data is transformed into nested JSON documents with the following structure:

```json
{
  "order_id": "405-8078784-5731545",
  "date": ISODate("2022-04-30"),
  "status": "Shipped",
  "customer": {
    "city": "MUMBAI",
    "state": "MAHARASHTRA",
    "postal_code": "400081",
    "country": "IN"
  },
  "product": {
    "style": "SET389",
    "sku": "SET389-KR-NP-S",
    "category": "Set",
    "size": "S",
    "asin": "B09KXVBD7Z"
  },
  "region": {
    "city": "MUMBAI",
    "state": "MAHARASHTRA",
    "postal_code": "400081",
    "country": "IN"
  },
  "sales": {
    "channel": "Amazon.in",
    "fulfilment": "Merchant",
    "service_level": "Standard",
    "quantity": 1,
    "currency": "INR",
    "amount": 647.62,
    "b2b": false
  },
  "fulfillment": {
    "fulfilled_by": "Easy Ship",
    "courier_status": "Shipped"
  },
  "promotions": []
}
```

## Features Demonstrated

### 1. CRUD Operations

#### CREATE
- Insert orders from CSV into MongoDB
- Batch insertion for performance
- Nested document structure

#### READ
- Retrieve all orders
- Query with filters (amount, status, etc.)
- Access nested fields directly

#### UPDATE
- Update order status
- Modify nested fields using `$set`

#### DELETE
- Delete orders by order_id
- Single document deletion

### 2. Date Range Queries

Query orders within a specific date range:
```python
query = {
    "date": {
        "$gte": start_date,
        "$lte": end_date
    }
}
orders = collection.find(query)
```

**SQL Equivalent:**
```sql
SELECT * FROM orders 
WHERE date BETWEEN 'start_date' AND 'end_date'
JOIN customers, products, regions...
```

**MongoDB Advantage:**
- No JOINs needed - all data in one document
- Simpler query syntax
- Faster for read-heavy workloads

### 3. Aggregation Pipelines

#### Sales by Region
Group sales by state/region with totals and averages:
```python
pipeline = [
    {"$match": {"sales.amount": {"$gt": 0}}},
    {"$group": {
        "_id": "$region.state",
        "total_sales": {"$sum": "$sales.amount"},
        "order_count": {"$sum": 1}
    }},
    {"$sort": {"total_sales": -1}}
]
```

#### Sales by Category
Group sales by product category:
```python
pipeline = [
    {"$match": {"sales.amount": {"$gt": 0}}},
    {"$group": {
        "_id": "$product.category",
        "total_sales": {"$sum": "$sales.amount"},
        "unique_products": {"$addToSet": "$product.sku"}
    }}
]
```

#### Complex Aggregation
Group by multiple fields (region AND category):
```python
{"$group": {
    "_id": {
        "state": "$region.state",
        "category": "$product.category"
    },
    "total_sales": {"$sum": "$sales.amount"}
}}
```

## NoSQL vs SQL Comparison

| Aspect | SQL (Relational) | MongoDB (NoSQL) |
|--------|------------------|-----------------|
| **Data Structure** | Normalized across tables | Denormalized nested documents |
| **Schema** | Fixed schema, requires ALTER TABLE | Flexible schema, add fields easily |
| **Queries** | JOINs required | No JOINs, all data in document |
| **Aggregations** | GROUP BY with JOINs | Flexible pipeline, reshape on fly |
| **Performance** | JOINs can be expensive | Single document read, larger size |
| **Use Cases** | Structured data, complex relationships | Semi-structured data, rapid iteration |

### Example Query Comparison

**SQL:**
```sql
SELECT o.*, c.*, p.* 
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN products p ON o.product_id = p.id
WHERE o.date BETWEEN '2022-04-01' AND '2022-04-30'
  AND c.state = 'MAHARASHTRA'
```

**MongoDB:**
```python
collection.find({
    "date": {"$gte": start, "$lte": end},
    "region.state": "MAHARASHTRA"
})
```

## MongoDB Connection

### Local MongoDB
```python
connection_string = "mongodb://localhost:27017/"
```

### MongoDB Atlas (Cloud)
```python
connection_string = "mongodb+srv://username:password@cluster.mongodb.net/"
```

Update the connection string in the notebook/script accordingly.

## Screenshots and Outputs

After running the notebook/script, you can:

1. **MongoDB Compass** (GUI):
   - Connect to your MongoDB instance
   - Browse the `amazon_sales_db` database
   - View the `orders` collection
   - Run queries and aggregations visually

2. **MongoDB Shell**:
   ```bash
   mongo
   use amazon_sales_db
   db.orders.find().limit(5)
   db.orders.aggregate([...])
   ```

3. **Jupyter Notebook Output**:
   - All query results are displayed in cells
   - Aggregation results formatted as tables
   - Statistics and comparisons shown

## Performance Considerations

- **Batch Insert**: Documents are inserted in batches of 1000 for better performance
- **Indexes**: Consider creating indexes on frequently queried fields:
  ```python
  collection.create_index("date")
  collection.create_index("region.state")
  collection.create_index("product.category")
  collection.create_index("sales.amount")
  ```

## Troubleshooting

1. **Connection Error**
   - Ensure MongoDB is running
   - Check connection string
   - Verify network/firewall settings

2. **Import Errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version (3.7+)

3. **Memory Issues**
   - For large CSV files, process in chunks
   - Use batch insertion
   - Consider using MongoDB Atlas for cloud storage

## Next Steps

- Add indexes for better query performance
- Implement data validation
- Create visualization dashboards
- Add more complex aggregations
- Implement data export functionality
- Add unit tests

## License

This project is for educational purposes.

## Author

Created as part of Week 7 MongoDB project demonstrating NoSQL database operations.

## References

- [MongoDB Documentation](https://docs.mongodb.com/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [MongoDB Aggregation Pipeline](https://docs.mongodb.com/manual/core/aggregation-pipeline/)

