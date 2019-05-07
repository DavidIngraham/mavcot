import xml.etree.ElementTree as ET
from mavcot.helpers import get_geoid_height

class CoTEvent:
    def __init__(self, uid, type=None):
        self.uid = str(uid)
        self.event_root = ET.Element('event')
        self.event_root.set('uid', self.uid)

        if type is not None:
            self.type = str(type)
            self.event_root.set('type', self.type)

        self.point = CoTPoint(self.event_root)
        self.detail = None


    def render_xml_string(self):
        ''' Creates a full xml string from the root of the cot message '''
        if self.event_root is None:
            return None
        
        header_string = '<?xml version="1.0" standalone="yes"?>'
        event_xml_string = ET.tostring(self.event_root)
        out_cot_xml = header_string + event_xml_string
        return out_cot_xml


class CoTSubElement:         
    def __init__(self, xml_root):
        self.xml_element = None
        self.xml_root = xml_root

    def get_tree_element(self):
        if self.xml_element is None:
            self.xml_element = ET.SubElement(self.xml_root, 'point')
        return self.xml_element

    def set_property(self, property, value):
        try:
            self.get_tree_element().set(property, str(value))
            return True
        except Exception as e:
            print ('Could not convert value to string', e)
            return False

class CoTPoint(CoTSubElement):    
    def set_point_hae(self, lat, lon, alt_hae):
        self.lat = lat
        self.lon = lon
        self.hae = alt_hae
        self.set_property('lat', self.lat)
        self.set_property('lon', self.lon)
        self.set_property('hae', self.hae)
        
    def set_point_msl(self, lat, lon, alt_msl):
        alt_hae = alt_msl + get_geoid_height(lat,lon)
        self.set_point_hae(lat, lon, alt_hae)

    def clear(self):
        self.xml_root.remove(self.xml_element)





if __name__ == '__main__':
    event1 = CoTEvent('test_uid')
    event1.point.set_point_msl(35,111,50)
    print(event1.render_xml_string())
    event1.point.clear()
    print(event1.render_xml_string())
    
    
