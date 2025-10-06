import yaml
import logging

logging.basicConfig(
    filename='app2.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

config = {
    "app" : {
        "name" : "Student Portal",
        "version" : 1.0

    },
    "database" : {
        "host" : "localhost",
        "port" : 3306,
        "user" : "root",
    }
}
# step 1
#write to yaml file
try :
    with open("config.yml", "w") as f:
        yaml.dump(config, f)
        logging.info('File saved successfully')

#reading the file
    with open("config.yml", "r") as f:
        data = yaml.safe_load(f)
        logging.info("Config loaded successfully.")

#2 : Extracting and printing connection
    config.get("database",{})
    host = config.get("database",{}).get("host","localhost")
    port = config.get("database",{}).get("port",3306)
    user = config.get("database",{}).get("user","root")

    if host and port and user:
        print(f"Connecting to {host}:{port} as {user}")

    else :
        print(f"Connection Failed to {host}:{port}")
        logging.warning("Connection Failed to {host}:{port}")

except FileNotFoundError :
    logging.warning("config.yaml not found.")
    print("ERROR - config.yaml not found.")