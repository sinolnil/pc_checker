import logging, json, time, dotenv, os, sys, pathlib
from src.pc import Pc
from src.utils.pc_spec_parser import Patterns, find_match
from src.spreadsheet import Spreadsheet

bundle_dir = getattr(sys, '_MEIPASS', pathlib.Path(__file__).parent.absolute())
env_path = os.path.join(bundle_dir, '.env')
dotenv.load_dotenv(env_path)

logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def load_config():

    logger.debug("Load configuration")
    APP_CONFIG = os.getenv("APP_CONFIG")
    SPREADSHEET_API_CREDENTIAL = os.getenv("SPREADSHEET_API_CREDENTIAL")
    
    if APP_CONFIG == "" or SPREADSHEET_API_CREDENTIAL == "":
        raise Exception("Missing / Fail to load environment")

    with open("config.json","r") as f:
        try:
            config = json.load(f)
        except Exception as e:
            logger.debug(f"Fail to load config.json")

    environment = config.get(APP_CONFIG,{})


    if not environment:
        raise Exception(f"Invalid APP_CONFIG: '{APP_CONFIG}'")
    
    return environment, SPREADSHEET_API_CREDENTIAL

def main():

    start_time = time.time()

    environment, creds = load_config()
    ss = Spreadsheet(
        env = environment,
        creds=json.loads(creds))

    sheet_name = "titles"
    sheet_id = environment.get("spreadsheet_map",{}).get(sheet_name,"")   
    titles = ss._fetch_sheet(sheet_name=sheet_name,sheet_id=sheet_id)

    pc = Pc()

    print(f"Fetched tiltes:{len(titles)}")
    #print(json.dumps(pc.system_info,indent=4))
    print(json.dumps(pc.get_all_props,indent=4))
    print(f"runtime:{round(time.time() - start_time,2)} sec")
    input("Enter to close..")

if __name__ == "__main__":
    main()
#
#data = {
#        title[0]: {
#            "cpu": None,
#            "gpu":None,
#            "sys": None,
#            "disk": None,
#            "ram": None
#        }
#    for title in titles 
#}
#
#for title,specs in data.items():
#    cpu_match  = find_match(Patterns.CPU, title)
#    sys_match  = find_match(Patterns.SYS, title)
#    ram_match  = find_match(Patterns.RAM, title)
#    gpu_match  = find_match(Patterns.GPU, title)
#    dis_match  = find_match(Patterns.DIS, title)
#    if cpu_match: data[title]['cpu'] = cpu_match
#    if gpu_match: data[title]['gpu'] = gpu_match
#    if sys_match: data[title]['sys'] = sys_match
#    if ram_match: data[title]['ram'] = ram_match
#    if dis_match: data[title]['disk'] = dis_match
#
#with open("out.json","w") as f:
#    json.dump(data,f,indent=4)