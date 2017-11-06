import os
from fragforce import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    dbg = bool(os.environ.get('DEBUG', 'False'))
    listen = os.environ.get('LISTEN', '0.0.0.0')
    app.run(host=listen, port=port, debug=dbg)
