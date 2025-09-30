import json, re

def find_match(pattern,string):
    return [ele.strip() for ele in re.findall(pattern,string)]

class Patterns:

    # SYS Pattern
    sys_pattern = r'(?:win|windows?)[ -]?\d{2}'
    one_letter_sys_pattern = r'W\d{2}'

    disk_pattern = r'\d{1,3}\s?(?:GB|TB)\s?(?:Solid State|M.2|NVME)?(?:\()?\s*(?:SSD|HDD|NVME|M.2)'

    # RAM Pattern
    ram_pattern = r'\d{1,3}\s?(?:GB)\s*(?:DDR\s*\d|RAM)'
    no_ram_pattern = r'\d{1,3}\s*(?:GB|TB)\s*(?=\d{1,3}(?:GB|TB)\s*(?:SSD|HDD|NVME|M.2))'

    # CPU Pattern
    intel_i_cpu_pattern = r'i[3579](?:[ -]\d+[a-z0-9]*(?!\s*(?:SSD|HHD|NVME|M.2)))?'
    intel_e_cpu_pattern = r'E\d-\d{3,5}\s?(?:V\d)?'
    amd_cpu_pattern     = r'Ryzen\s*\d\s*(?:[a-z0-9]*)?'

    # GPU Pattern
    nvidia_gpu_pattern = r'(?:RTX|GTX?)\s*[a-z0-9]*'
    amd_gpu_pattern = r'RX\s*[a-z0-9]*'

    def build_pattern(patterns=[]):
        return r'(?i)\b(' + '|'.join(patterns) + r')\b'

    CPU = build_pattern([intel_i_cpu_pattern, intel_e_cpu_pattern, amd_cpu_pattern])
    GPU = build_pattern([nvidia_gpu_pattern, amd_gpu_pattern])
    RAM = build_pattern([ram_pattern, no_ram_pattern])
    SYS = build_pattern([sys_pattern, one_letter_sys_pattern])
    DIS = build_pattern([disk_pattern])