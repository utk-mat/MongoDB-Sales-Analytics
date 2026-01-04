// MongoDB Shell Queries
// Run these queries in MongoDB shell or MongoDB Compass
// Usage: mongo amazon_sales_db mongodb_queries.js

// Switch to the database
use amazon_sales_db;

print("=== MongoDB Sales Data Queries ===\n");

// 1. Count total documents
print("1. Total Orders:");
print(db.orders.countDocuments({}));
print();

// 2. Find sample orders
print("2. Sample Orders (first 3):");
db.orders.find().limit(3).pretty();
print();

// 3. Query orders in date range
print("3. Orders in Date Range (April 2022):");
db.orders.find({
    "date": {
        $gte: ISODate("2022-04-01"),
        $lte: ISODate("2022-04-30")
    }
}).limit(5).pretty();
print();

// 4. Aggregation: Sales by Region (State)
print("4. Top 10 States by Sales:");
db.orders.aggregate([
    {
        $match: {
            "sales.amount": { $gt: 0 }
        }
    },
    {
        $group: {
            _id: "$region.state",
            total_sales: { $sum: "$sales.amount" },
            order_count: { $sum: 1 },
            avg_order_value: { $avg: "$sales.amount" }
        }
    },
    {
        $sort: { total_sales: -1 }
    },
    {
        $limit: 10
    }
]);
print();

// 5. Aggregation: Sales by Category
print("5. Sales by Category:");
db.orders.aggregate([
    {
        $match: {
            "sales.amount": { $gt: 0 }
        }
    },
    {
        $group: {
            _id: "$product.category",
            total_sales: { $sum: "$sales.amount" },
            order_count: { $sum: 1 },
            total_quantity: { $sum: "$sales.quantity" }
        }
    },
    {
        $sort: { total_sales: -1 }
    }
]);
print();

// 6. Aggregation: Sales by Region AND Category
print("6. Top State-Category Combinations:");
db.orders.aggregate([
    {
        $match: {
            "sales.amount": { $gt: 0 }
        }
    },
    {
        $group: {
            _id: {
                state: "$region.state",
                category: "$product.category"
            },
            total_sales: { $sum: "$sales.amount" },
            order_count: { $sum: 1 }
        }
    },
    {
        $sort: { total_sales: -1 }
    },
    {
        $limit: 15
    }
]);
print();

// 7. Query orders by status
print("7. Orders by Status:");
db.orders.aggregate([
    {
        $group: {
            _id: "$status",
            count: { $sum: 1 }
        }
    },
    {
        $sort: { count: -1 }
    }
]);
print();

// 8. Find high-value orders
print("8. High-Value Orders (>1000 INR):");
db.orders.find({
    "sales.amount": { $gt: 1000 }
}).limit(5).pretty();
print();

// 9. Total sales statistics
print("9. Overall Sales Statistics:");
db.orders.aggregate([
    {
        $match: {
            "sales.amount": { $gt: 0 }
        }
    },
    {
        $group: {
            _id: null,
            total_sales: { $sum: "$sales.amount" },
            total_quantity: { $sum: "$sales.quantity" },
            avg_order_value: { $avg: "$sales.amount" },
            order_count: { $sum: 1 }
        }
    }
]);
print();

// 10. Date range of data
print("10. Date Range:");
db.orders.aggregate([
    {
        $group: {
            _id: null,
            min_date: { $min: "$date" },
            max_date: { $max: "$date" }
        }
    }
]);
print();

print("=== Queries Complete ===");

