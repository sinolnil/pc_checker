import unittest
import re
from src.utils.pc_spec_parser import Patterns, find_match


class TestPattern(unittest.TestCase):

    TEST_CASES = [
        {
            "title": "HP EliteOne 800 G2 23\" FHD AIO TOUCH RTX3050 SCREEN i5-6Gen 16GB 480GB SSD Win10 WiFi",
            "cpu" : ["i5-6Gen"],
            "ram" : ["16GB"],
            "disk": ["480GB SSD"],
            "sys" : ["Win10"],
            "gpu" : ["RTX3050"],
        },
        {
            "title": "Custom Gaming PC Desktop Computer i7 RTX 3050 8GB 32GB RAM 1TB SSD W10 PRO WIFI",
            "cpu" : ["i7"],
            "ram" : ["32GB RAM"],
            "disk": ["1TB SSD"],
            "sys" : ["W10"],
            "gpu" : ["RTX 3050"],
        },
        
        {
            "title": "Gaming PC Ultra Fast i7-12700K RTX 3070 8GB 16GB RAM 1TB SSD Liquid Cooled Win11 Pro WiFi6 Bluetooth ARGB Desktop Computer for Gaming Streaming Office",
            "cpu" : ["i7-12700K"],
            "ram" : ["16GB RAM"],
            "disk": ["1TB SSD"],
            "sys" : ["Win11"],
            "gpu" : ["RTX 3070"],
        },
        {
            "title": "New Cooler 11Gen Gaming PC i9-11900 Nvidia RTX 3060 12GB RAM 64GB 1TB NVME SSD Liquid Cooler Win11 WIFI Computer",
            "cpu" : ["i9-11900"],
            "ram" : ["12GB RAM","64GB"],
            "disk": ["1TB NVME SSD"],
            "sys" : ["Win11"],
            "gpu" : ["RTX 3060"],
        },
        {
            "title": "New Cooler 11Gen Gaming PC i9-11900 AMD RX 580 RAM 64GB 1TB NVME SSD Liquid Cooler Win11 WIFI Computer",
            "cpu" : ["i9-11900"],
            "ram" : ["64GB"],
            "disk": ["1TB NVME SSD"],
            "sys" : ["Win11"],
            "gpu" : ["RX 580"],
        },
        {
            "title":"Gaming PC Desktop i9 11900 32GB RAM 2TB SSD RTX 3060 Windows 11 PRO WIFI",
            "cpu" : ["i9 11900"],
            "ram" : ["32GB RAM"],
            "disk": ["2TB SSD"],
            "sys" : ["Windows 11"],
            "gpu" : ["RTX 3060"],
        },
        {
            "title":"Gaming-Pro Gaming PC Computer Intel i7 512GB SSD+500GB HDD RX550 32GB RAM WIFI WINDOWS 10",
            "cpu" : ["i7"],
            "ram" : ["32GB RAM"],
            "disk": ["512GB SSD","500GB HDD"],
            "sys" : ["WINDOWS 10"],
            "gpu" : ["RX550"],
        },
    ]

    def test_match_cpu(self):
        for test_case in self.TEST_CASES:
            result = find_match(Patterns.CPU, test_case["title"])
            self.assertEqual(test_case["cpu"], result)

    def test_match_ram(self):
        for test_case in self.TEST_CASES:
            result = find_match(Patterns.RAM, test_case["title"])
            self.assertEqual(test_case["ram"], result)

    def test_match_disk(self):
        for test_case in self.TEST_CASES:
            result = find_match(Patterns.DIS, test_case["title"])
            self.assertEqual(test_case["disk"], result)

    def test_match_gpu(self):
        for test_case in self.TEST_CASES:
            result = find_match(Patterns.GPU, test_case["title"])
            self.assertEqual(test_case["gpu"], result)

    def test_match_sys(self):
        for test_case in self.TEST_CASES:
            result = find_match(Patterns.SYS, test_case["title"])
            self.assertEqual(test_case["sys"], result)


if __name__ == "__main__":
    unittest.main()
