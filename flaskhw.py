from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock "database" using Python lists
users = []  # Stores user data as dictionaries
movies = [  # Pre-populated list of movies
    {"id": 1, "title": "Inception", "genre": "Sci-Fi"},
    {"id": 2, "title": "The Dark Knight", "genre": "Action"},
    {"id": 3, "title": "Interstellar", "genre": "Sci-Fi"}
]

# Endpoint for registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password required"}), 400
    
    # Check if user already exists
    if any(user['username'] == data['username'] for user in users):
        return jsonify({"error": "User already exists"}), 400
    
    users.append(data)
    return jsonify({"message": "User registered successfully!"}), 201

# Endpoint for login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Check credentials
    user = next((user for user in users if user['username'] == username and user['password'] == password), None)
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "Login successful!"}), 200

# Endpoint to get available movies
@app.route('/movies', methods=['GET'])
def get_movies():
    return jsonify({"movies": movies}), 200

if __name__ == "__main__":
    app.run(debug=True)
