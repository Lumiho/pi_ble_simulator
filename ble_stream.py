import asyncio
from bless import BlessServer
# pip install bless
async def main():
    server = BlessServer(name="MuscleMaxMock")
    await server.start()
    print("BLE server started. Advertising as 'MuscleMaxMock'.")

    # Keep the server running
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
