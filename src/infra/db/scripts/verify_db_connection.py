# type: ignore
import asyncio

import aiomysql

DB_HOST = "dbfinance"
DB_PORT = 3306
DB_USER = "dev"
DB_PASSWORD = "dev123"
DB_NAME = "finance"


async def test_db_connection() -> None:
    try:
        print("Tentando conectar ao banco de dados...")
        conn = await aiomysql.connect(
            host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, db=DB_NAME
        )
        print("Conexão com o banco de dados bem-sucedida!")

        async with conn.cursor() as cur:
            await cur.execute("SHOW DATABASES;")
            databases = await cur.fetchall()
            print("Bases de dados disponíveis:")
            for db in databases:
                print(f" - {db[0]}")
                await cur.execute(f"USE {db[0]};")
                await cur.execute("SHOW TABLES;")
                tables = await cur.fetchall()
                for table in tables:
                    print(f"   - {table[0]}")

        conn.close()

    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")


if __name__ == "__main__":
    asyncio.run(test_db_connection())
