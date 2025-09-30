import os
from dotenv import load_dotenv
from app import app

load_dotenv()

env = os.getenv("APP_ENV", "development").lower()
port = 4587

if __name__ == "__main__":
    
    if env == "production":
        from waitress import serve
        serve(app, host="0.0.0.0", port=port)
    else:
        app.run(debug=True, host="0.0.0.0", port=port)
