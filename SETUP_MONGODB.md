# MongoDB Setup Guide

## Option 1: MongoDB Atlas (Cloud - Recommended)

**No installation required!**

1. Go to https://www.mongodb.com/cloud/atlas/register
2. Create a free account
3. Create a free cluster (M0 - Free tier)
4. Get your connection string
5. Update the connection string in the code:

```python
# In mongodb_sales_operations.py or notebook
connection_string = "mongodb+srv://username:password@cluster.mongodb.net/"
```

## Option 2: Install MongoDB Locally

### macOS (using Homebrew)

```bash
# Install MongoDB
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB
brew services start mongodb-community

# Or run manually
mongod --config /opt/homebrew/etc/mongod.conf
```

### macOS (Manual Installation)

1. Download from: https://www.mongodb.com/try/download/community
2. Extract and move to `/usr/local/mongodb`
3. Create data directory: `mkdir -p /data/db`
4. Start MongoDB: `/usr/local/mongodb/bin/mongod`

### Linux

```bash
# Ubuntu/Debian
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
```

### Windows

1. Download MongoDB Community Server from: https://www.mongodb.com/try/download/community
2. Run the installer
3. MongoDB will start as a Windows service automatically

## Verify MongoDB is Running

```bash
# Check if MongoDB is running
mongosh

# Or check connection
mongo --eval "db.version()"
```

## Current Status

✅ **Dependencies Installed:**
- pymongo
- pandas
- python-dateutil
- jupyter
- ipykernel

❌ **MongoDB Not Running:**
- MongoDB needs to be started before running the script
- Or use MongoDB Atlas (cloud) - no installation needed

## Next Steps

1. **Choose an option above** (Atlas recommended for quick start)
2. **Update connection string** in the code if using Atlas
3. **Run the script again**: `python mongodb_sales_operations.py`
4. **Or use Jupyter**: `jupyter notebook mongodb_sales_analysis.ipynb`

## Quick Test

Once MongoDB is running, test the connection:

```python
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
print(client.server_info())
```

