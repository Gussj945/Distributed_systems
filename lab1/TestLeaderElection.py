import asyncio
# Import your Proxy class (adjust import path as needed)
from Server.AsyncBoardProxy import storage as BoardProxy
# Import your corrected LeaderElection class
from Server.LeaderElection import election 

async def main():
    print("--- Setting up Test Environment ---")
    
    # 1. Create Proxies for 3 potential servers (Ports 10000, 10001, 10002)
    # We assume Server 0 is port 10000, Server 1 is 10001, etc.
    proxies = [
        BoardProxy(10000, 0),
        BoardProxy(10001, 1),
        BoardProxy(10002, 2)
    ]

    # 2. Create an instance of the election class
    # We pretend WE are Server 1 (ID=1)
    my_id = 1
    my_election_module = election(proxies, my_id)

    print("\n--- Test 1: callAreYouAlive ---")
    # Try to reach Server 0
    alive_0 = await my_election_module.callAreYouAlive(0)
    print(f"Is Server 0 Alive? {alive_0}")
    
    # Try to reach Server 2 (If you didn't start it, this should be False)
    alive_2 = await my_election_module.callAreYouAlive(2)
    print(f"Is Server 2 Alive? {alive_2}")

    print("\n--- Test 2: callElection ---")
    # Call election on Server 0
    resp = await my_election_module.callElection(0)
    print(f"Call Election on Server 0 result: {resp}")

    print("\n--- Test 3: callSetCoordinator ---")
    # Tell Server 0 that Server 1 is the new boss
    success = await my_election_module.callSetCoordinator(0, 1)
    print(f"Set Coordinator on Server 0 success: {success}")

    print("\n--- Test 4: callSetCoordinatorInAllServers ---")
    # This should update local state and call remote servers concurrently
    await my_election_module.callSetCoordinatorInAllServers(1)
    print(f"Local Coordinator ID is now: {my_election_module.coordinatorID}")

    # clean up connections
    for p in proxies:
        await p.close()

if __name__ == "__main__":
    asyncio.run(main())