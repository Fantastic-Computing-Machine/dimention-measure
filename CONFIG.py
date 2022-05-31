import urllib


MONGO = (
    'dimDB',
    'dimCollection',
    "mongodb+srv://dimention:" + urllib.parse.quote_plus(
        "measurement") + "@clusterd.wie7f.mongodb.net/dimDB?retryWrites=true&w=majority"
)


# mongodb+srv://dimention:measurement@clusterd.wie7f.mongodb.net/dimDB?authSource=admin&replicaSet=atlas-u1i7np-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true
