# Quick Start Guide

## Prerequisites Check

1. **MongoDB Installed?**
   ```bash
   mongod --version
   ```
   If not installed, download from [mongodb.com](https://www.mongodb.com/try/download/community)

2. **Python Installed?**
   ```bash
   python --version
   ```
   Should be Python 3.7 or higher

3. **MongoDB Running?**
   ```bash
   # Start MongoDB (if local)
   mongod
   ```
   Or use MongoDB Atlas (cloud) - no local installation needed

## Installation Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start MongoDB** (if using local)
   ```bash
   mongod
   ```

## Running the Project

### Option 1: Jupyter Notebook (Recommended for Learning)

```bash
# Start Jupyter
jupyter notebook

# Open mongodb_sales_analysis.ipynb
# Run cells sequentially
```

### Option 2: Python Script

```bash
# Run the main script
python mongodb_sales_operations.py
```

**Note**: The script has data insertion commented out by default. 
To insert data, uncomment the `insert_orders()` call in the `main()` function.

## First-Time Setup

1. **Load Data into MongoDB**
   - Open `mongodb_sales_analysis.ipynb`
   - Run cells 1-7 (up to CREATE operation)
   - This will insert all orders from CSV into MongoDB

2. **Create Indexes** (Optional but Recommended)
   ```bash
   python create_indexes.py
   ```

3. **Run Queries**
   - Continue running notebook cells
   - Or run the Python script

## MongoDB Shell Queries

To run queries in MongoDB shell:

```bash
# Start MongoDB shell
mongo

# Switch to database
use amazon_sales_db

# Run queries from file
load("mongodb_queries.js")

# Or run individual queries
db.orders.find().limit(5)
db.orders.countDocuments({})
```

## MongoDB Compass (GUI)

1. Download [MongoDB Compass](https://www.mongodb.com/products/compass)
2. Connect to `mongodb://localhost:27017/`
3. Browse `amazon_sales_db` database
4. View `orders` collection
5. Run queries and aggregations visually

## Common Issues

### "Connection refused"
- MongoDB is not running
- Start MongoDB: `mongod`

### "Module not found"
- Install dependencies: `pip install -r requirements.txt`

### "Port already in use"
- MongoDB is already running
- Or change MongoDB port in connection string

## Next Steps

1. ✅ Run the notebook/script
2. ✅ Explore queries in MongoDB Compass
3. ✅ Try modifying queries
4. ✅ Create your own aggregations
5. ✅ Compare with SQL queries

## Project Structure

```
Week7_MongoDB/
├── Amazon Sale Report(in).csv      # Source data
├── mongodb_sales_analysis.ipynb    # Jupyter notebook (START HERE)
├── mongodb_sales_operations.py     # Python script
├── mongodb_queries.js              # MongoDB shell queries
├── create_indexes.py               # Index creation script
├── requirements.txt                # Dependencies
├── README.md                       # Full documentation
└── QUICKSTART.md                   # This file
```

## Tips

- **Large Dataset**: The CSV has ~128K rows. Processing may take a few minutes.
- **Memory**: If you run out of memory, process data in smaller batches.
- **Indexes**: Create indexes after inserting data for better performance.
- **Screenshots**: Use MongoDB Compass to take screenshots of queries and results.

