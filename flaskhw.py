from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data storage
users = {}  # {"username": "password"}
movies = []

@app.route("/")
def home():
    return "Welcome to the Movie Theater API!"

# User registration endpoint
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    if username in users:
        return jsonify({"error": "User already exists"}), 400
    
    users[username] = password
    return jsonify({"message": "User registered successfully"}), 201

# User login endpoint
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    if users.get(username) != password:
        return jsonify({"error": "Invalid username or password"}), 401
    
    return jsonify({"message": "Login successful"}), 200

# Get movies list
@app.route("/movies", methods=["GET"])
def get_movies():
    return jsonify({"movies": movies}), 200

# Book tickets for a movie
@app.route("/book", methods=["POST"])
def book_tickets():
    data = request.json
    username = data.get("username")
    movie_id = data.get("movie_id")
    time = data.get("time")
    seats = data.get("seats")  # List of tuples [(row, col), ...]

    if not username or movie_id is None or not time or not seats:
        return jsonify({"error": "Invalid booking data"}), 400

    movie = next((m for m in movies if m["id"] == movie_id), None)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    if time not in movie["times"]:
        return jsonify({"error": "Invalid time"}), 400

    if time not in movie["tickets"]:
        movie["tickets"][time] = {"seats": [], "buyers": []}

    for seat in seats:
        if seat in movie["tickets"][time]["seats"]:
            return jsonify({"error": f"Seat {seat} is already booked"}), 400

    movie["tickets"][time]["seats"].extend(seats)
    movie["tickets"][time]["buyers"].append(username)

    return jsonify({"message": "Tickets booked successfully"}), 200

# Get ticket info for a user
@app.route("/tickets", methods=["POST"])
def get_tickets():
    data = request.json
    username = data.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400

    user_tickets = []
    for movie in movies:
        for time, details in movie["tickets"].items():
            if username in details["buyers"]:
                user_tickets.append({
                    "movie": movie["title"],
                    "time": time,
                    "seats": details["seats"],
                })

    return jsonify({"tickets": user_tickets}), 200


if __name__ == "__main__":
    app.run(debug=True)
