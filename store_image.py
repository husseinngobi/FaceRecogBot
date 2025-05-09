import sqlite3

# Open the image as binary data
def convert_image_to_binary(image_path):
    with open(image_path, "rb") as file:
        return file.read()

# Connect to SQLite database
conn = sqlite3.connect("faces.db")
cursor = conn.cursor()

# Path to your image
image_path = r"C:\Users\HP\OneDrive\Documents\GitHub\database images\CEO-image.jpg"

# Convert image to binary
image_data = convert_image_to_binary(image_path)

# Insert into the database
cursor.execute("INSERT INTO faces (name, age, gender, title, image) VALUES (?, ?, ?, ?, ?)", 
               ("Hussein Ngobi", 25, "Male", "CEO", image_data))

conn.commit()
conn.close()

print("✅ Image successfully added to database!")