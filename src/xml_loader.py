import xml.etree.ElementTree as ET


class XMLLoader:

    def __init__(self, file_path):
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()

    def get_h1(self):
        return self.root.findall(".//H0/H1")

    def get_jobcodes(self):
        return self.root.findall(".//Labor/JobCodes/J")

    def get_daily(self):
        return self.root.findall(".//TM0[@type='DAILY']/TM1")

    def get_shift(self):
        return self.root.findall(".//TM0[@type='SHIFT']/TM1")

    def get_weekly(self):
        return self.root.findall(".//TM0[@type='WEEKLY']/TM1")

    def get_pay_period(self):
        return self.root.findall(".//TM0[@type='PAY_PERIOD']/TM1")