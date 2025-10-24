import subprocess
import time
import requests
import os

def ensure_backend_running():
    try:
        requests.get("http://127.0.0.1:5000/healthcheck", timeout=2)
        print("✅ Flask backend already running.")
    except requests.exceptions.RequestException:
        print("🔄 Starting Flask backend...")
        log_path = os.path.join(os.getcwd(), "flask_log.txt")
        flask_path = os.path.join(os.getcwd(), "grocery_api.py")  # Update if needed
        try:
            subprocess.Popen(
                ["python", flask_path],
                stdout=open(log_path, "w"),
                stderr=subprocess.STDOUT,
                cwd=os.getcwd(),
                creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0
            )
            time.sleep(3)
            requests.get("http://127.0.0.1:5000/healthcheck", timeout=5)
            print("✅ Flask backend is now running.")
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            print("📄 Check flask_log.txt for details.")
            exit(1)

def query_price(city, item):
    try:
        response = requests.get("http://127.0.0.1:5000/price", params={"city": city, "item": item})
        data = response.json()

        if isinstance(data, list):
            if not data:
                return f"⚠️ No results found for '{item}' in {city}."

            # Fuzzy match: look for "egg" in product name
            matches = [d for d in data if "egg" in d["name"].lower()]
            if matches:
                lines = [f"- {d['name']} — ${d['price']} at {d['store']}" for d in matches]
                return "\n".join(lines)
            else:
                fallback = [f"- {d['name']} — ${d['price']} at {d['store']}" for d in data]
                return f"🔍 No exact match for '{item}', but here are related results:\n" + "\n".join(fallback)

        elif isinstance(data, dict) and "error" in data:
            return f"⚠️ Error: {data['error']}"
        else:
            return f"⚠️ Unexpected response format:\n{data}"
    except Exception as e:
        return f"❌ Request failed: {e}"

def main():
    ensure_backend_running()
    while True:
        user_input = input("🛒 What are you shopping for today? (Type 'exit' to quit)\n> ")
        if user_input.lower() == "exit":
            break
        if "price of" in user_input and "in" in user_input:
            parts = user_input.split("in")
            item = parts[0].split("price of")[-1].strip()
            city = parts[1].strip()
            print(query_price(city, item))
        else:
            print("💡 Try asking: 'What is the price of eggs in Ottawa?'")

if __name__ == "__main__":
    main()
print(f"Parsed item: {item_name}")
print(f"Parsed location: {location}")
print(f"Available items: {list_of_items}")
print(f"Available locations: {list_of_locations}")
