import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("faces.db")
cursor = conn.cursor()

# Retrieve the image data
cursor.execute("SELECT image FROM faces WHERE name=?", ("Hussein Ngobi",))
image_data = cursor.fetchone()[0]

if image_data:
    with open("retrieved_image.jpg", "wb") as file:
        file.write(image_data)
    print("✅ Image successfully retrieved! Check 'retrieved_image.jpg'")
else:
    print("⚠️ No image found for 'Hussein Ngobi'!")

conn.close()