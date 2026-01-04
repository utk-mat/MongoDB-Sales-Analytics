"""
Create indexes for MongoDB collection to improve query performance.
Run this script after inserting data.
"""

from pymongo import MongoClient, ASCENDING, DESCENDING

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["amazon_sales_db"]
collection = db["orders"]

print("Creating indexes for better query performance...\n")

# Create indexes
indexes = [
    ("date", ASCENDING),  # For date range queries
    ("region.state", ASCENDING),  # For region-based queries
    ("product.category", ASCENDING),  # For category-based queries
    ("sales.amount", DESCENDING),  # For sorting by amount
    ("status", ASCENDING),  # For status filtering
    ("order_id", ASCENDING),  # For unique lookups
]

created_indexes = []
for field, direction in indexes:
    try:
        result = collection.create_index([(field, direction)])
        created_indexes.append(f"{field} ({'ASC' if direction == 1 else 'DESC'})")
        print(f"✓ Created index on: {field}")
    except Exception as e:
        print(f"✗ Error creating index on {field}: {e}")

print(f"\n✓ Created {len(created_indexes)} indexes")
print("\nIndexes created:")
for idx in created_indexes:
    print(f"  - {idx}")

# List all indexes
print("\nAll indexes on collection:")
for index in collection.list_indexes():
    print(f"  - {index['name']}: {index.get('key', {})}")

client.close()
print("\n✓ Index creation complete")

