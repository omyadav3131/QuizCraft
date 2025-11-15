# main.py
from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Use 127.0.0.1 for local development. Change to 0.0.0.0 for LAN.
    app.run(debug=True, host='127.0.0.1', port=5000)
