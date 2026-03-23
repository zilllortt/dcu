import asyncio
import aiohttp
import time

# Configuration
URL = "https://api.aifiesta.ai"
CONCURRENT_WORKERS = 9999999  # Exactly 5 requests at a time

async def worker(session, worker_id):
    """
    A worker that sends GET requests one after another 
    as fast as the server can respond.
    """
    print(f"Worker {worker_id} started.")
    
    while True:  # Infinite loop for 'constant' requests
        try:
            start_time = time.perf_counter()
            
            async with session.get(URL) as response:
                status = response.status
                # We consume the response body to ensure the connection is freed
                await response.release() 
                
                end_time = time.perf_counter()
                latency = (end_time - start_time) * 1000
                
                print(f"[Worker {worker_id}] Status: {status} | Latency: {latency:.2f}ms")

        except Exception as e:
            print(f"[Worker {worker_id}] Error: {e}")
            # Wait a second if there's an error to avoid a rapid-fire crash loop
            await asyncio.sleep(1)

async def main():
    print(f"🚀 Initializing {CONCURRENT_WORKERS} constant workers...")
    
    # We use one session for all workers to keep it efficient
    async with aiohttp.ClientSession() as session:
        # Create 5 worker tasks
        tasks = []
        for i in range(1, CONCURRENT_WORKERS + 1):
            tasks.append(asyncio.create_task(worker(session, i)))

        # Wait for the workers to run (they will run forever)
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user.")
