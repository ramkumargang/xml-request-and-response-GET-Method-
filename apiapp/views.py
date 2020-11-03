from django.shortcuts import render,HttpResponse
import xml.etree.ElementTree as ET
def home(request):
    return render(request,'index.html')

def handle_xml_upload(request):     
    class XmlTree():
        def xml_compare(self, x1, x2, excludes=[]):
            """
            Compares two xml etrees
            :param x1: the first tree
            :param x2: the second tree
            :param excludes: list of string of attributes to exclude from comparison
            :return:
                True if both files match
            """

            if x1.tag != x2.tag:
                print('Tags do not match: %s and %s' % (x1.tag, x2.tag))
                return False
            for name, value in x1.attrib.items():
                if not name in excludes:
                    if x2.attrib.get(name) != value:
                        print('Attributes do not match: %s=%r, %s=%r'
                                    % (name, value, name, x2.attrib.get(name)))
                        return False
            for name in x2.attrib.keys():
                if not name in excludes:
                    if name not in x1.attrib:
                        print('x2 has an attribute x1 is missing: %s'
                                    % name)
                        return False
            if not self.text_compare(x1.text, x2.text):
                print('text: %r != %r' % (x1.text, x2.text))
                return False
            if not self.text_compare(x1.tail, x2.tail):
                print('tail: %r != %r' % (x1.tail, x2.tail))
                return False
            cl1 = x1.getchildren()
            cl2 = x2.getchildren()
            if len(cl1) != len(cl2):
                print('children length differs, %i != %i'
                            % (len(cl1), len(cl2)))
                return False
            i = 0
            for c1, c2 in zip(cl1, cl2):
                i += 1
                if not c1.tag in excludes:
                    if not self.xml_compare(c1, c2, excludes):
                        print('children %i do not match: %s'
                                    % (i, c1.tag))
                        return False
            return True

        def text_compare(self, t1, t2):
            """
            Compare two text strings
            :param t1: text one
            :param t2: text two
            :return:
                True if a match
            """
            if not t1 and not t2:
                return True
            if t1 == '*' or t2 == '*':
                return True
            return (t1 or '').strip() == (t2 or '').strip()

    xml1 = """<xml>
                <item>
                <receiverID>all</receiverID>
                <api_assign>https://track.spritle.com/get_data</api_assign>
                <api_post>https://track.spritle.com/receive_data</api_post>
                <api_ntp>API3</api_ntp>
                <api_ota>API4</api_ota>
                <no_beacon>99</no_beacon>
                <http_time>5</http_time>
                <rssi_max>99</rssi_max>
                <ssid>CIPL</ssid>
                <password>CIPL2016</password>
                    </item>
                    </xml>"""
    tree1=ET.fromstring(xml1)
    if request.method == 'GET':
        print("This is get method")
        data = request.GET['xmlfile']
        tree2 = ET.fromstring(data)         
        comparator = XmlTree()
        if comparator.xml_compare(tree1, tree2, []):
            return HttpResponse(data+"xml match", content_type='text/plain')
        else:
            return HttpResponse("xml not match", content_type='text/plain')
                
                