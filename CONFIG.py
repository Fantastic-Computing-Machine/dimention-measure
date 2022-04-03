import urllib


MONGO = (
    'dimDB',
    'dimCollection',
    "mongodb+srv://dimention:" + urllib.parse.quote_plus(
        "measurement") + "@clusterd.wie7f.mongodb.net/dimDB?retryWrites=true&w=majority"
)
