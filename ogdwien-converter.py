#! /usr/bin/env python
# -*- coding: utf-8 -*-

from xml.etree import ElementTree
from xml.dom import minidom
import re


colors = dict ({
  u'Radroute': u'ffff0000',
  u'Radfahren im Wald': u'ff00ff00',
  u'Markierte Anlagen': u'ff0099ff',
  u'Getrennte Führung': u'ff0000ff'
})

filename = 'test.kml'
outfile = 'test2.kml'
kml_ns = 'http://www.opengis.net/kml/2.2'

def changeColor(k,node):
  if k in colors:
    ls = node.getElementsByTagNameNS(kml_ns, 'LineStyle')[0]
    color = ls.getElementsByTagNameNS(kml_ns, 'color')[0]
    color.firstChild.data = colors[k]

only_whitespace = re.compile("^\s*$")

def deleteEmptyTextNodes(node, indent=''):
  for element in node.childNodes:
    if element.nodeType == element.TEXT_NODE:
      if only_whitespace.match(element.data) is not None:
        node.removeChild(element)
        element.unlink()
  for element in node.childNodes:
    deleteEmptyTextNodes(element, indent = indent + '  ')


def run2():
  dom = minidom.parse(filename)
  documents = dom.getElementsByTagNameNS(kml_ns,'Document')
  assert len(documents) == 1
  document = documents[0]
  types = dict()
  deleteEmptyTextNodes(dom.documentElement)
  for placemark in dom.getElementsByTagNameNS(kml_ns,'Placemark'):
    descriptions = placemark.getElementsByTagNameNS(kml_ns,'description')
    assert len(descriptions) == 1
    description = descriptions[0]
    cdata = description.firstChild
    assert cdata.nodeType == minidom.Node.CDATA_SECTION_NODE
    #print cdata.data
    desc_xml = minidom.parseString('<html><body>%s</body></html>' % cdata.data.encode('utf-8'))
    #dt = desc_xml.getElementsByTagName('dt')[0]
    #print dt.firstChild.data
    dd = desc_xml.getElementsByTagName('dd')[0]
    t = dd.firstChild.data
    if t not in types:
      types[t] = []
    types[t].append(placemark)
    placemark.parentNode.removeChild(placemark)

    for d in placemark.getElementsByTagNameNS(kml_ns,'description'):
      d.parentNode.removeChild(d)
      d.unlink()
    
  #for k, v in types.iteritems():
  #  print k + ": " + str(len(v))
  
  for k in types.iterkeys():
    data = dom.createTextNode(k)
    name = dom.createElementNS(kml_ns,'name')
    name.appendChild(data)
    f = dom.createElementNS(kml_ns,'Folder')
    f.appendChild(name)
    document.appendChild(f)

    for n in types[k]:
      changeColor(k,n)
      f.appendChild(n)


  f = open(outfile, 'w')
  f.write(dom.toprettyxml(indent='   ', newl='\n', encoding='utf-8'))
  #f.write(dom.toxml(encoding='utf-8'))
  #xml.dom.ext.PrettyPrint(dom, f, encoding='utf-8')
  f.close()

if __name__ == '__main__':
  run2()
