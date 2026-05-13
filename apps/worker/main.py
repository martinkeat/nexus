import asyncio
import logging

logging.basicConfig(level=logging.INFO, format='[Nexus Worker] %(message)s')

async def main():
    logging.info("Worker started.")
    while True:
        # TODO: Implement download monitoring and transcoding triggers
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
