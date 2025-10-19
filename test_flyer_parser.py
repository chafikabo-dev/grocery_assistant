from flyer_parser import parse_flyer_image

results = parse_flyer_image("farmboy_flyer.png", store_name="Farm Boy")

print("\n🥬 Farm Boy Flyer Results:")
for item in results:
    print(f"- {item['store']}: ${item['price']} ({item['name']})")
