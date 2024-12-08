from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# In-memory data storage
users = {}  # {"username": "password"}
movies = []
otchet = {}  # {"username": [{"movie": movie_id, "time": time, "seats": [(row, col), ...]}, ...]}
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

# # Get movies list
@app.route("/movies", methods=["GET"])
def get_movies():
    return jsonify({"movies": movies}), 200


@app.route("/book", methods=["POST"])
def book_tickets():
    try:
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

        # Store booking in otchet
        if username not in otchet:
            otchet[username] = []

        otchet[username].append({
            "movie": movie_id,
            "time": time,
            "seats": seats
        })

        movie["tickets"][time]["seats"].extend(seats)
        movie["tickets"][time]["buyers"].append(username)

        return jsonify({"message": "Tickets booked successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Assuming static hosting, generate public URL
    file_url = f"/{UPLOAD_FOLDER}/{file.filename}"
    return jsonify({"url": file_url}), 200

@app.route("/add_movie", methods=["POST"])
def add_movie():
    data = request.json
    title = data.get("title")
    image_url = data.get("image")
    background_url = data.get("background")  # Add this field

    if not title or not image_url or not background_url:
        return jsonify({"error": "Movie title, image, and background are required"}), 400

    new_movie = {
        "id": len(movies) + 1,
        "title": title,
        "image": image_url,
        "background": background_url,
        "times": ["12:00", "14:00", "16:30", "20:00"],
        "tickets": {}
    }
    movies.append(new_movie)

    return jsonify({"message": "Movie added successfully"}), 200

@app.route("/get_booked_seats", methods=["GET"])
def get_booked_seats():
    movie_id = int(request.args.get("movie_id"))
    time = request.args.get("time")

    movie = next((m for m in movies if m["id"] == movie_id), None)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    if time not in movie["tickets"]:
        return jsonify({"booked_seats": []}), 200

    booked_seats = movie["tickets"][time]["seats"]
    return jsonify({"booked_seats": booked_seats}), 200


@app.route("/delete_movie/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    # Поиск фильма по ID
    movie = next((movie for movie in movies if movie["id"] == movie_id), None)

    if movie is None:
        return jsonify({"error": "Movie not found"}), 404

    # Удаление фильма из списка
    movies.remove(movie)

    return jsonify({"message": "Movie deleted successfully", "movie": movie}), 200

if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
    