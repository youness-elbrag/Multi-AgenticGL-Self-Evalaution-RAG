
import os 
os.environ["DATA"] = "../engine/VectorDB//DATA/"

path = os.getenv("DATA")

print(os.listdir(path))
