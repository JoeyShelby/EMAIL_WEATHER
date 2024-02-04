class WeatherDataBase:
    def __init__(self, json_data):
        self.province = json_data['lives'][0]['province']
        self.city = json_data['lives'][0]['city']
        self.adcode = json_data['lives'][0]['adcode']
        self.weather = json_data['lives'][0]['weather']
        self.temperature = json_data['lives'][0]['temperature']
        self.winddirection = json_data['lives'][0]['winddirection']
        self.windpower = json_data['lives'][0]['windpower']
        self.humidity = json_data['lives'][0]['humidity']
        self.reporttime = json_data['lives'][0]['reporttime']
        self.temperature_float = float(json_data['lives'][0]['temperature_float'])
        self.humidity_float = float(json_data['lives'][0]['humidity_float'])


    def __str__(self):
        return f"WeatherDataBase(province={self.province}, city={self.city}, adcode={self.adcode}, weather={self.weather}, temperature={self.temperature}, winddirection={self.winddirection}, windpower={self.windpower}, humidity={self.humidity}, reporttime={self.reporttime}, temperature_float={self.temperature_float}, humidity_float={self.humidity_float})"
