import traceback
import asyncio
import time


Limit = asyncio.Semaphore(2000)

def default_payload():
    r=b"GET / HTTP/1.1\r\nHost:test\r\n\r\n"
    return r

async def fetch(ip, port, payload=default_payload()):
    async  with Limit:
        start = time.perf_counter()
        try:
            reader,writer = await asyncio.open_connection(ip,port)
            writer.write(payload)
            await writer.drain()
            await reader.read(1024)
            writer.close()
            await writer.wait_closed()
            res = time.perf_counter()-start
            return res
        except Exception as e:
            print(f"Ex {e} \n {traceback.print_exc()}")
            return None
        

async def run_batch(ip, port, total_requests):
    x = lambda: asyncio.create_task(fetch(ip,port))
    y = lambda: range(total_requests)
    tasks = [ x() for _ in y() ]
    start = time.perf_counter()
    results = await asyncio.gather(*tasks)
    end = time.perf_counter()

    successes = [r for r in results if r is not None]
    failed = total_requests - len(successes)
    total_time = end - start

    if successes:
        avg_latency = sum(successes) / len(successes)
    else:
        avg_latency = 0

    print(f"\n == Test: {total_requests} requests")
    print(f"Total time: {total_time:.3f}s")
    print(f"Avg latency: {avg_latency*1000:2f} ms")
    print(f"Req/sec: {total_requests/total_time:.2f}")
    print(f"Failed: {failed}")
    

async def main():
    ip = "127.0.0.1"
    port = 8080

    for count in [10,1000,10000]:
        await run_batch(ip, port, count)


if __name__ == "__main__":
    asyncio.run(main())






