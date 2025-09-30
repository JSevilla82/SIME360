import os
from dotenv import load_dotenv
from app import app
load_dotenv()
mcCshMifTLxmBpSFCDIKBGokGPHmClgh = os.getenv("APP_ENV", "development").lower()
HiNyiAfDJvMebAUqsWNCNUFVLUlKljCY = 4587
if __name__ == "__main__":
    if mcCshMifTLxmBpSFCDIKBGokGPHmClgh == "production":
        from waitress import serve
        serve(app, host="0.0.0.0", HiNyiAfDJvMebAUqsWNCNUFVLUlKljCY=HiNyiAfDJvMebAUqsWNCNUFVLUlKljCY)
    else:
        app.run(debug=True, host="0.0.0.0", HiNyiAfDJvMebAUqsWNCNUFVLUlKljCY=HiNyiAfDJvMebAUqsWNCNUFVLUlKljCY)
