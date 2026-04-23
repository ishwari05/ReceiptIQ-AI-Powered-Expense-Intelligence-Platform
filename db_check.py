import asyncio
from sqlalchemy import text
from app.db.database import engine

async def check_db():
    print("Attempting to connect to the database...")
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            val = result.scalar()
            if val == 1:
                print("✅ Database connection successful!")
            else:
                print("❌ Connected but got unexpected result.")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_db())
