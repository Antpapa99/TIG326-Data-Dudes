from server import server
from layout import app
import callbacks  # ensure callbacks are registered

if __name__ == '__main__':
    server.run(debug=True, port=9000)