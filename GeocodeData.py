# 地理编码类
class Geocodes:
    def __init__(self, formatted_address, country, province, citycode, city, district, adcode, location, level, township=None, neighborhood=None, building=None, street=None, number=None):
        self.formatted_address = formatted_address
        self.country = country
        self.province = province
        self.citycode = citycode
        self.city = city
        self.district = district
        self.adcode = adcode
        self.location = location
        self.level = level
        self.township = township
        self.neighborhood = neighborhood
        self.building = building
        self.street = street
        self.number = number

    def __str__(self):
        return f"Geocodes(formatted_address={self.formatted_address}, country={self.country}, province={self.province}, citycode={self.citycode}, city={self.city}, district={self.district}, adcode={self.adcode}, location={self.location}, level={self.level}, township={self.township}, neighborhood={self.neighborhood}, building={self.building}, street={self.street}, number={self.number})"


class GeocodeData:
    def __init__(self, json_data):
        status = json_data['status']
        info = json_data['info']
        infocode = json_data['infocode']
        count = json_data['count']
        geocodes = json_data['geocodes']
        self.status = status
        self.info = info
        self.infocode = infocode
        self.count = count
        self.geocodes = [Geocodes(formatted_address=geocode['formatted_address'],
                                  country=geocode['country'],
                                  province=geocode['province'],
                                  citycode=geocode['citycode'],
                                  city=geocode['city'],
                                  district=geocode['district'],
                                  adcode=geocode['adcode'],
                                  location=geocode['location'],
                                  level=geocode['level'],
                                  township=geocode.get('township'),
                                  neighborhood=geocode.get('neighborhood'),
                                  building=geocode.get('building'),
                                  street=geocode.get('street'),
                                  number=geocode.get('number')) for geocode in geocodes]

    def __str__(self):
        return f"GeocodeData(status={self.status}, info={self.info}, infocode={self.infocode}, count={self.count}, geocodes=[{', '.join([str(geocode) for geocode in self.geocodes])}])"