import urllib


MONGO = (
    'dimDB',
    'dimCollection',
    "mongodb+srv://dimention:" + urllib.parse.quote_plus(
        "measurement") + "@clusterd.wie7f.mongodb.net/dimDB?retryWrites=true&w=majority"
)


DATABASE = (
    '0.tcp.in.ngrok.io',
    15968,
    'root',
    'adiagarwal',
    'dimention_db'
)


SECRET_KEY = 'fantasticcomputingmachine'

DATABASE_URI = 'mysql+pymysql://root:adiagarwal@localhost/dimention_db'
