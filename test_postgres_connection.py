"""
Test PostgreSQL connection using the Neon database credentials
This script tests the connection to the PostgreSQL database and provides
comprehensive information about the database state.
"""
import os
import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import sys

# Load environment variables if .env file exists
load_dotenv()

# Database connection parameters from environment variables
DATABASE_CONFIG = {
    "pooled": {
        "url": os.getenv('DATABASE_URL'),
        "host": os.getenv('PGHOST'),
        "database": os.getenv('PGDATABASE'),
        "user": os.getenv('PGUSER'),
        "password": os.getenv('PGPASSWORD'),
        "port": int(os.getenv('PGPORT', 5432)),
        "sslmode": "require"
    },
    "unpooled": {
        "url": os.getenv('DATABASE_URL_UNPOOLED'),
        "host": os.getenv('PGHOST_UNPOOLED'),
        "database": os.getenv('PGDATABASE'),
        "user": os.getenv('PGUSER'),
        "password": os.getenv('PGPASSWORD'),
        "port": int(os.getenv('PGPORT', 5432)),
        "sslmode": "require"
    }
}

def validate_env_vars():
    """Validate that all required environment variables are set"""
    required_vars = [
        'DATABASE_URL', 'DATABASE_URL_UNPOOLED', 'PGHOST', 'PGHOST_UNPOOLED',
        'PGDATABASE', 'PGUSER', 'PGPASSWORD'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("💡 Make sure you have a .env file with all PostgreSQL credentials")
        return False
    
    print("✅ All required environment variables are set")
    return True

def test_psycopg2_connection(config_name, config):
    """Test connection using psycopg2 directly"""
    print(f"\n🔄 Testing {config_name} connection with psycopg2...")
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=config["host"],
            database=config["database"],
            user=config["user"],
            password=config["password"],
            port=config["port"],
            sslmode=config["sslmode"]
        )
        
        print(f"✅ {config_name} connection successful!")
        
        # Get cursor
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"📊 PostgreSQL version: {version[0]}")
        
        # Check current database
        cursor.execute("SELECT current_database();")
        current_db = cursor.fetchone()
        print(f"🗄️  Current database: {current_db[0]}")
        
        # List all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"📋 Tables found: {[table[0] for table in tables]}")
        else:
            print("📋 No tables found (database is empty)")
        
        # Check database size
        cursor.execute("""
            SELECT pg_size_pretty(pg_database_size(current_database()));
        """)
        db_size = cursor.fetchone()
        print(f"💾 Database size: {db_size[0]}")
        
        # Check connection info
        cursor.execute("SELECT inet_server_addr(), inet_server_port();")
        server_info = cursor.fetchone()
        print(f"🌐 Connected to: {server_info[0]}:{server_info[1]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ {config_name} connection failed:")
        print(f"   Error code: {e.pgcode}")
        print(f"   Error message: {e.pgerror}")
        return False
    except Exception as e:
        print(f"❌ {config_name} connection failed with unexpected error:")
        print(f"   {str(e)}")
        return False

def test_sqlalchemy_connection(config_name, config):
    """Test connection using SQLAlchemy"""
    print(f"\n🔄 Testing {config_name} connection with SQLAlchemy...")
    try:
        # Create engine
        engine = create_engine(config["url"])
        
        # Test connection
        with engine.connect() as connection:
            # Test basic query
            result = connection.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()
            print(f"✅ {config_name} SQLAlchemy connection successful!")
            print(f"🧪 Test query result: {test_value[0]}")
            
            # Get schema information
            result = connection.execute(text("""
                SELECT count(*) as table_count
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            table_count = result.fetchone()
            print(f"📊 Total tables in public schema: {table_count[0]}")
            
        return True
        
    except Exception as e:
        print(f"❌ {config_name} SQLAlchemy connection failed:")
        print(f"   {str(e)}")
        return False

def create_test_table_and_data():
    """Create a test table and insert some data to verify write operations"""
    print(f"\n🔄 Testing database write operations...")
    try:
        conn = psycopg2.connect(
            host=DATABASE_CONFIG["pooled"]["host"],
            database=DATABASE_CONFIG["pooled"]["database"],
            user=DATABASE_CONFIG["pooled"]["user"],
            password=DATABASE_CONFIG["pooled"]["password"],
            port=DATABASE_CONFIG["pooled"]["port"],
            sslmode=DATABASE_CONFIG["pooled"]["sslmode"]
        )
        
        cursor = conn.cursor()
        
        # Create test table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS connection_test (
                id SERIAL PRIMARY KEY,
                test_message VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
          # Insert test data
        test_message = f"Connection test successful for user {os.getenv('USERNAME', 'unknown_user')}"
        cursor.execute("""
            INSERT INTO connection_test (test_message) 
            VALUES (%s)
        """, (test_message,))
        
        # Commit changes
        conn.commit()
        
        # Read back data
        cursor.execute("SELECT * FROM connection_test ORDER BY created_at DESC LIMIT 1")
        result = cursor.fetchone()
        
        print(f"✅ Test table created and data inserted successfully!")
        print(f"📝 Latest test record: ID={result[0]}, Message='{result[1]}', Created={result[2]}")
        
        # Clean up test table
        cursor.execute("DROP TABLE IF EXISTS connection_test")
        conn.commit()
        print(f"🧹 Test table cleaned up successfully!")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Database write operation failed:")
        print(f"   {str(e)}")
        return False

def main():
    """Main function to run all connection tests"""
    print("🚀 Starting PostgreSQL Connection Tests")
    print("=" * 50)
    
    # Validate environment variables first
    if not validate_env_vars():
        print("\n❌ Cannot proceed without required environment variables")
        print("💡 Please check your .env file and ensure all PostgreSQL credentials are set")
        return False
    
    # Check if required packages are installed
    try:
        import psycopg2
        import sqlalchemy
        print("✅ Required packages (psycopg2, sqlalchemy) are installed")
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("💡 Run: pip install psycopg2-binary sqlalchemy")
        sys.exit(1)
    
    results = []
    
    # Test both pooled and unpooled connections
    for config_name, config in DATABASE_CONFIG.items():
        # Test with psycopg2
        result1 = test_psycopg2_connection(config_name, config)
        results.append((f"{config_name}_psycopg2", result1))
        
        # Test with SQLAlchemy
        result2 = test_sqlalchemy_connection(config_name, config)
        results.append((f"{config_name}_sqlalchemy", result2))
    
    # Test write operations
    write_result = create_test_table_and_data()
    results.append(("write_operations", write_result))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name:25} - {status}")
    
    successful_tests = sum(1 for _, success in results if success)
    total_tests = len(results)
    
    print(f"\n🎯 Results: {successful_tests}/{total_tests} tests passed")
    
    if successful_tests == total_tests:
        print("🎉 All tests passed! Your PostgreSQL database connection is working perfectly!")
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")
    
    return successful_tests == total_tests

if __name__ == "__main__":
    main()
