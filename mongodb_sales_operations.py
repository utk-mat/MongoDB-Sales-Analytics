"""
MongoDB Sales Data Operations
==============================
This script demonstrates storing and querying semi-structured sales data in MongoDB.
It includes CRUD operations, date range queries, and aggregation pipelines.
"""

import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from dateutil import parser
import json
from typing import List, Dict, Any


class MongoDBSalesOperations:
    """
    A class to handle MongoDB operations for sales data.
    Demonstrates NoSQL flexibility vs relational SQL model.
    """
    
    def __init__(self, connection_string: str = "mongodb://localhost:27017/", 
                 database_name: str = "amazon_sales_db"):
        """
        Initialize MongoDB connection.
        
        Args:
            connection_string: MongoDB connection string
            database_name: Name of the database to use
        """
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db["orders"]
        print(f"Connected to MongoDB database: {database_name}")
    
    def transform_csv_to_json(self, csv_file_path: str) -> List[Dict[str, Any]]:
        """
        Transform CSV data into nested JSON documents.
        
        Structure:
        {
            "order_id": "...",
            "date": ISODate(...),
            "status": "...",
            "customer": {
                "city": "...",
                "state": "...",
                "postal_code": "...",
                "country": "..."
            },
            "product": {
                "style": "...",
                "sku": "...",
                "category": "...",
                "size": "...",
                "asin": "..."
            },
            "region": {
                "city": "...",
                "state": "...",
                "postal_code": "...",
                "country": "..."
            },
            "sales": {
                "channel": "...",
                "fulfilment": "...",
                "service_level": "...",
                "quantity": ...,
                "currency": "...",
                "amount": ...,
                "b2b": bool
            },
            "fulfillment": {
                "fulfilled_by": "...",
                "courier_status": "..."
            },
            "promotions": [...]
        }
        
        This nested structure demonstrates NoSQL flexibility:
        - All related data in one document (no joins needed)
        - Easy to add new fields without schema changes
        - Natural representation of hierarchical data
        """
        print(f"Reading CSV file: {csv_file_path}")
        df = pd.read_csv(csv_file_path)
        
        documents = []
        for _, row in df.iterrows():
            # Parse date
            try:
                order_date = parser.parse(str(row['Date']))
            except:
                order_date = datetime.now()
            
            # Build nested document structure
            document = {
                "order_id": str(row.get('Order ID', '')),
                "date": order_date,
                "status": str(row.get('Status', '')),
                
                # Customer information (nested)
                "customer": {
                    "city": str(row.get('ship-city', '')),
                    "state": str(row.get('ship-state', '')),
                    "postal_code": str(row.get('ship-postal-code', '')),
                    "country": str(row.get('ship-country', ''))
                },
                
                # Product information (nested)
                "product": {
                    "style": str(row.get('Style', '')),
                    "sku": str(row.get('SKU', '')),
                    "category": str(row.get('Category', '')),
                    "size": str(row.get('Size', '')),
                    "asin": str(row.get('ASIN', ''))
                },
                
                # Region information (nested - same as customer for this dataset)
                "region": {
                    "city": str(row.get('ship-city', '')),
                    "state": str(row.get('ship-state', '')),
                    "postal_code": str(row.get('ship-postal-code', '')),
                    "country": str(row.get('ship-country', ''))
                },
                
                # Sales information (nested)
                "sales": {
                    "channel": str(row.get('Sales Channel ', '')),
                    "fulfilment": str(row.get('Fulfilment', '')),
                    "service_level": str(row.get('ship-service-level', '')),
                    "quantity": int(row.get('Qty', 0)) if pd.notna(row.get('Qty')) else 0,
                    "currency": str(row.get('currency', '')),
                    "amount": float(row.get('Amount', 0)) if pd.notna(row.get('Amount')) else 0.0,
                    "b2b": str(row.get('B2B', 'FALSE')).upper() == 'TRUE'
                },
                
                # Fulfillment information (nested)
                "fulfillment": {
                    "fulfilled_by": str(row.get('fulfilled-by', '')),
                    "courier_status": str(row.get('Courier Status', ''))
                },
                
                # Promotions (array)
                "promotions": []
            }
            
            # Parse promotions if available
            if pd.notna(row.get('promotion-ids')) and str(row.get('promotion-ids')).strip():
                promotions_str = str(row.get('promotion-ids'))
                document["promotions"] = [p.strip() for p in promotions_str.split(',') if p.strip()]
            
            documents.append(document)
        
        print(f"Transformed {len(documents)} rows into JSON documents")
        return documents
    
    def insert_orders(self, documents: List[Dict[str, Any]], batch_size: int = 1000):
        """
        INSERT operation (Create in CRUD).
        Insert orders into MongoDB collection.
        
        In SQL, this would require:
        - INSERT INTO orders, customers, products, regions tables
        - Multiple foreign key relationships
        - Transaction management for consistency
        
        In MongoDB:
        - Single insert operation
        - All related data in one document
        - Atomic operation per document
        """
        print(f"\n=== INSERT OPERATION (CREATE) ===")
        print(f"Inserting {len(documents)} documents...")
        
        # Clear existing collection (optional - for clean start)
        # self.collection.delete_many({})
        
        # Insert in batches for better performance
        inserted_count = 0
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            result = self.collection.insert_many(batch)
            inserted_count += len(result.inserted_ids)
            print(f"Inserted batch: {inserted_count}/{len(documents)} documents")
        
        print(f"Successfully inserted {inserted_count} orders")
        return inserted_count
    
    def read_all_orders(self, limit: int = 10):
        """
        READ operation (Read in CRUD).
        Retrieve all orders with optional limit.
        
        In SQL: SELECT * FROM orders JOIN customers JOIN products...
        In MongoDB: Simple find() - no joins needed
        """
        print(f"\n=== READ OPERATION ===")
        print(f"Retrieving {limit} orders...")
        
        orders = list(self.collection.find().limit(limit))
        print(f"Found {len(orders)} orders")
        
        for order in orders[:3]:  # Show first 3
            print(f"\nOrder ID: {order.get('order_id')}")
            print(f"  Date: {order.get('date')}")
            print(f"  Customer: {order.get('customer', {}).get('city')}, {order.get('customer', {}).get('state')}")
            print(f"  Product: {order.get('product', {}).get('category')} - {order.get('product', {}).get('style')}")
            print(f"  Amount: {order.get('sales', {}).get('amount')} {order.get('sales', {}).get('currency')}")
        
        return orders
    
    def query_orders_by_date_range(self, start_date: str, end_date: str):
        """
        Query orders within a specific date range.
        
        In SQL:
        SELECT * FROM orders 
        WHERE date BETWEEN 'start_date' AND 'end_date'
        JOIN customers, products, regions...
        
        In MongoDB:
        Simple query with date range - all data already in document
        """
        print(f"\n=== QUERY: Orders in Date Range ===")
        print(f"Date Range: {start_date} to {end_date}")
        
        start = parser.parse(start_date)
        end = parser.parse(end_date)
        
        query = {
            "date": {
                "$gte": start,
                "$lte": end
            }
        }
        
        orders = list(self.collection.find(query))
        total_amount = sum(order.get('sales', {}).get('amount', 0) for order in orders)
        total_quantity = sum(order.get('sales', {}).get('quantity', 0) for order in orders)
        
        print(f"Found {len(orders)} orders in date range")
        print(f"Total Amount: {total_amount:,.2f}")
        print(f"Total Quantity: {total_quantity}")
        
        # Show sample results
        if orders:
            print("\nSample orders:")
            for order in orders[:5]:
                print(f"  {order.get('order_id')}: {order.get('date')} - {order.get('sales', {}).get('amount')} {order.get('sales', {}).get('currency')}")
        
        return orders
    
    def aggregate_sales_by_region(self):
        """
        Aggregation: Group sales by region (state).
        
        In SQL:
        SELECT state, SUM(amount) as total_sales, COUNT(*) as order_count
        FROM orders o
        JOIN regions r ON o.region_id = r.id
        GROUP BY state
        ORDER BY total_sales DESC
        
        In MongoDB:
        Aggregation pipeline - more flexible, can reshape data on the fly
        """
        print(f"\n=== AGGREGATION: Sales by Region (State) ===")
        
        pipeline = [
            {
                "$match": {
                    "sales.amount": {"$gt": 0}  # Only count orders with amount > 0
                }
            },
            {
                "$group": {
                    "_id": "$region.state",
                    "total_sales": {"$sum": "$sales.amount"},
                    "order_count": {"$sum": 1},
                    "total_quantity": {"$sum": "$sales.quantity"},
                    "avg_order_value": {"$avg": "$sales.amount"}
                }
            },
            {
                "$sort": {"total_sales": -1}
            },
            {
                "$limit": 10  # Top 10 states
            }
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        print(f"\nTop 10 States by Sales:")
        print(f"{'State':<25} {'Total Sales':<15} {'Orders':<10} {'Avg Order Value':<15}")
        print("-" * 70)
        
        for result in results:
            state = result.get('_id', 'Unknown')
            total = result.get('total_sales', 0)
            count = result.get('order_count', 0)
            avg = result.get('avg_order_value', 0)
            print(f"{state:<25} {total:>12,.2f} INR {count:>8} {avg:>12,.2f} INR")
        
        return results
    
    def aggregate_sales_by_category(self):
        """
        Aggregation: Group sales by product category.
        
        In SQL:
        SELECT category, SUM(amount) as total_sales, COUNT(*) as order_count
        FROM orders o
        JOIN products p ON o.product_id = p.id
        GROUP BY category
        ORDER BY total_sales DESC
        
        In MongoDB:
        Aggregation pipeline with nested field access
        """
        print(f"\n=== AGGREGATION: Sales by Category ===")
        
        pipeline = [
            {
                "$match": {
                    "sales.amount": {"$gt": 0}
                }
            },
            {
                "$group": {
                    "_id": "$product.category",
                    "total_sales": {"$sum": "$sales.amount"},
                    "order_count": {"$sum": 1},
                    "total_quantity": {"$sum": "$sales.quantity"},
                    "avg_order_value": {"$avg": "$sales.amount"},
                    "unique_products": {"$addToSet": "$product.sku"}
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "total_sales": 1,
                    "order_count": 1,
                    "total_quantity": 1,
                    "avg_order_value": 1,
                    "unique_product_count": {"$size": "$unique_products"}
                }
            },
            {
                "$sort": {"total_sales": -1}
            }
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        print(f"\nSales by Category:")
        print(f"{'Category':<20} {'Total Sales':<15} {'Orders':<10} {'Products':<10} {'Avg Value':<15}")
        print("-" * 80)
        
        for result in results:
            category = result.get('_id', 'Unknown')
            total = result.get('total_sales', 0)
            count = result.get('order_count', 0)
            products = result.get('unique_product_count', 0)
            avg = result.get('avg_order_value', 0)
            print(f"{category:<20} {total:>12,.2f} INR {count:>8} {products:>8} {avg:>12,.2f} INR")
        
        return results
    
    def aggregate_sales_by_region_and_category(self):
        """
        Complex aggregation: Sales by region AND category.
        Demonstrates MongoDB's flexible aggregation capabilities.
        
        In SQL: Requires multiple JOINs and GROUP BY with multiple columns
        In MongoDB: Single aggregation pipeline with $group on multiple fields
        """
        print(f"\n=== AGGREGATION: Sales by Region AND Category ===")
        
        pipeline = [
            {
                "$match": {
                    "sales.amount": {"$gt": 0}
                }
            },
            {
                "$group": {
                    "_id": {
                        "state": "$region.state",
                        "category": "$product.category"
                    },
                    "total_sales": {"$sum": "$sales.amount"},
                    "order_count": {"$sum": 1}
                }
            },
            {
                "$sort": {"total_sales": -1}
            },
            {
                "$limit": 15
            }
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        print(f"\nTop 15 State-Category Combinations:")
        print(f"{'State':<20} {'Category':<20} {'Total Sales':<15} {'Orders':<10}")
        print("-" * 70)
        
        for result in results:
            state = result.get('_id', {}).get('state', 'Unknown')
            category = result.get('_id', {}).get('category', 'Unknown')
            total = result.get('total_sales', 0)
            count = result.get('order_count', 0)
            print(f"{state:<20} {category:<20} {total:>12,.2f} INR {count:>8}")
        
        return results
    
    def update_order_status(self, order_id: str, new_status: str):
        """
        UPDATE operation (Update in CRUD).
        Update order status.
        
        In SQL: UPDATE orders SET status = 'new_status' WHERE order_id = '...'
        In MongoDB: updateOne() with filter and update document
        """
        print(f"\n=== UPDATE OPERATION ===")
        print(f"Updating order {order_id} status to {new_status}")
        
        result = self.collection.update_one(
            {"order_id": order_id},
            {"$set": {"status": new_status}}
        )
        
        if result.matched_count > 0:
            print(f"Successfully updated {result.modified_count} order(s)")
        else:
            print(f"Order {order_id} not found")
        
        return result
    
    def delete_order(self, order_id: str):
        """
        DELETE operation (Delete in CRUD).
        Delete an order.
        
        In SQL: DELETE FROM orders WHERE order_id = '...'
               (May need to handle foreign key constraints)
        In MongoDB: deleteOne() - removes entire document
        """
        print(f"\n=== DELETE OPERATION ===")
        print(f"Deleting order {order_id}")
        
        result = self.collection.delete_one({"order_id": order_id})
        
        if result.deleted_count > 0:
            print(f"Successfully deleted order {order_id}")
        else:
            print(f"Order {order_id} not found")
        
        return result
    
    def compare_nosql_vs_sql(self):
        """
        Compare NoSQL (MongoDB) flexibility vs Relational SQL model.
        """
        print(f"\n{'='*80}")
        print("COMPARISON: NoSQL (MongoDB) vs Relational SQL Model")
        print(f"{'='*80}\n")
        
        print("1. DATA STRUCTURE:")
        print("   SQL: Normalized across multiple tables (orders, customers, products, regions)")
        print("   MongoDB: Denormalized nested documents (all data in one document)\n")
        
        print("2. SCHEMA:")
        print("   SQL: Fixed schema, requires ALTER TABLE for changes")
        print("   MongoDB: Flexible schema, can add fields without migration\n")
        
        print("3. QUERIES:")
        print("   SQL: JOINs required to combine related data")
        print("   MongoDB: No JOINs needed, all data in document\n")
        
        print("4. AGGREGATIONS:")
        print("   SQL: GROUP BY with JOINs, complex for nested data")
        print("   MongoDB: Flexible aggregation pipeline, can reshape data dynamically\n")
        
        print("5. PERFORMANCE:")
        print("   SQL: JOINs can be expensive, but optimized with indexes")
        print("   MongoDB: Single document read, but larger document size\n")
        
        print("6. USE CASES:")
        print("   SQL: Best for structured data, complex relationships, ACID transactions")
        print("   MongoDB: Best for semi-structured data, rapid iteration, horizontal scaling\n")
        
        print("7. EXAMPLE - Query with date range and region:")
        print("   SQL: SELECT o.*, c.*, p.* FROM orders o")
        print("        JOIN customers c ON o.customer_id = c.id")
        print("        JOIN products p ON o.product_id = p.id")
        print("        WHERE o.date BETWEEN '...' AND '...' AND c.state = '...'")
        print("   MongoDB: db.orders.find({")
        print("              'date': {$gte: start, $lte: end},")
        print("              'region.state': '...'")
        print("            })\n")
    
    def get_collection_stats(self):
        """Get statistics about the collection."""
        print(f"\n=== COLLECTION STATISTICS ===")
        
        total_docs = self.collection.count_documents({})
        print(f"Total Orders: {total_docs:,}")
        
        # Count by status
        status_pipeline = [
            {"$group": {"_id": "$status", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        status_counts = list(self.collection.aggregate(status_pipeline))
        print(f"\nOrders by Status:")
        for status in status_counts:
            print(f"  {status['_id']}: {status['count']:,}")
        
        # Date range
        date_pipeline = [
            {"$group": {
                "_id": None,
                "min_date": {"$min": "$date"},
                "max_date": {"$max": "$date"}
            }}
        ]
        date_range = list(self.collection.aggregate(date_pipeline))
        if date_range:
            print(f"\nDate Range:")
            print(f"  From: {date_range[0]['min_date']}")
            print(f"  To: {date_range[0]['max_date']}")
        
        return {
            "total_documents": total_docs,
            "status_counts": status_counts,
            "date_range": date_range[0] if date_range else None
        }
    
    def close_connection(self):
        """Close MongoDB connection."""
        self.client.close()
        print("\nMongoDB connection closed")


def main():
    """
    Main function to demonstrate all MongoDB operations.
    """
    # Initialize MongoDB operations
    mongo_ops = MongoDBSalesOperations()
    
    try:
        # Step 1: Transform CSV to JSON documents
        csv_file = "Amazon Sale Report(in).csv"
        documents = mongo_ops.transform_csv_to_json(csv_file)
        
        # Step 2: Insert orders (CREATE)
        # Uncomment to insert data
        # mongo_ops.insert_orders(documents)
        
        # Step 3: Read orders (READ)
        mongo_ops.read_all_orders(limit=5)
        
        # Step 4: Query orders by date range
        mongo_ops.query_orders_by_date_range("2022-04-01", "2022-04-30")
        
        # Step 5: Aggregation - Sales by region
        mongo_ops.aggregate_sales_by_region()
        
        # Step 6: Aggregation - Sales by category
        mongo_ops.aggregate_sales_by_category()
        
        # Step 7: Complex aggregation - Sales by region AND category
        mongo_ops.aggregate_sales_by_region_and_category()
        
        # Step 8: Update operation (UPDATE)
        # Get a sample order ID first
        sample_order = mongo_ops.collection.find_one()
        if sample_order:
            mongo_ops.update_order_status(sample_order['order_id'], "Updated Status")
        
        # Step 9: Delete operation (DELETE)
        # Uncomment to test delete
        # mongo_ops.delete_order(sample_order['order_id'])
        
        # Step 10: Collection statistics
        mongo_ops.get_collection_stats()
        
        # Step 11: Comparison with SQL
        mongo_ops.compare_nosql_vs_sql()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        mongo_ops.close_connection()


if __name__ == "__main__":
    main()

