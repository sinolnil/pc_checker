import logging, json, time, dotenv, os
from src.pc import Pc
from src.utils.pc_spec_parser import Patterns, find_match
from src.spreadsheet import Spreadsheet
dotenv.load_dotenv()

logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

APP_CONFIG = os.getenv("APP_CONFIG")
SPREADSHEET_API_CREDENTIAL = json.loads(os.getenv("SPREADSHEET_API_CREDENTIAL"))
pc = Pc()

with open("config.json","r") as f:
    config = json.load(f)

environment = config.get(APP_CONFIG,{})

if not environment:
    raise Exception(f"Invalid APP_CONFIG '{APP_CONFIG}'")

start_time = time.time()

ss = Spreadsheet(
    env = environment,
    creds=SPREADSHEET_API_CREDENTIAL)

sheet_name = "titles"
sheet_id = environment.get("spreadsheet_map",{}).get(sheet_name,"")   
titles = ss._fetch_sheet(sheet_name=sheet_name,sheet_id=sheet_id)
data = {
        title[0]: {
            "cpu": None,
            "gpu":None,
            "sys": None,
            "disk": None,
            "ram": None
        }
    for title in titles 
}

for title,specs in data.items():
    cpu_match  = find_match(Patterns.CPU, title)
    sys_match  = find_match(Patterns.SYS, title)
    ram_match  = find_match(Patterns.RAM, title)
    gpu_match  = find_match(Patterns.GPU, title)
    dis_match = find_match(Patterns.DIS, title)
    if cpu_match: data[title]['cpu'] = cpu_match
    if gpu_match: data[title]['gpu'] = gpu_match
    if sys_match: data[title]['sys'] = sys_match
    if ram_match: data[title]['ram'] = ram_match
    if dis_match: data[title]['dis'] = dis_match

result =json.dumps(dict(list(data.items()),indent=4))
print(result)