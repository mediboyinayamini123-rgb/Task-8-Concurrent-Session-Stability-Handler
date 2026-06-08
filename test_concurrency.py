import asyncio
import httpx

async def execute_race_test():
    base_url = "http://localhost:8000/api/sessions"
    
    async with httpx.AsyncClient() as client:
        print("1. Constructing sample interview data state inside local SQLite database...")
        bootstrap_res = await client.post(f"{base_url}/bootstrap")
        session_data = bootstrap_res.json()
        session_id = session_data["id"]
        version = session_data["version"]
        print(f"Session setup with ID: {session_id} | Starting Version: {version}\n")

        print("2. Dispatching 3 concurrent updates to the same version state at the same millisecond...")
        payloads = [
            {"notes": "Interviewer A notes", "status": "IN_PROGRESS", "currentVersion": version},
            {"notes": "Interviewer B notes", "status": "IN_PROGRESS", "currentVersion": version},
            {"notes": "Final submit payload", "status": "COMPLETED", "currentVersion": version}
        ]
        
        headers = {"x-session-id": session_id}
        
        # Fire all requests concurrently using asyncio.gather
        tasks = [
            client.put(f"{base_url}/{session_id}", json=p, headers=headers)
            for p in payloads
        ]
        responses = await asyncio.gather(*tasks)

        print("\n3. Testing execution matrix feedback:")
        for index, res in enumerate(responses):
            print(f"Request #{index + 1} Return Code: {res.status_code}")
            print(f"Payload Output: {res.text}\n")

if __name__ == "__main__":
    asyncio.run(execute_race_test())