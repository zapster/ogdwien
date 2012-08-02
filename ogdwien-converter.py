#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Josef Eisl
#
# This file is part of ogdwien-converter
#
# ogdwien-converter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from xml.etree import ElementTree
from xml.dom import minidom
import re
import argparse


# line color map
colors = dict ({
  u'Radroute': u'ffff0000',
  u'Radfahren im Wald': u'ff00ff00',
  u'Markierte Anlagen': u'ff0099ff',
  u'Getrennte Führung': u'ff0000ff'
})

infile = None
outfile = None
kml_ns = 'http://www.opengis.net/kml/2.2'
only_whitespace = re.compile("^\s*$")

def changeColor(k,node):
  """
  Change the color of Placemark (or any other element which contains a LineStyle element.
  """
  if k in colors:
    ls = node.getElementsByTagNameNS(kml_ns, 'LineStyle')[0]
    if ls is None:
      return
    
    color = ls.getElementsByTagNameNS(kml_ns, 'color')[0]
    if color is None:
      return

    color.firstChild.data = colors[k]


def deleteEmptyTextNodes(node, indent=''):
  """
  Remove empty TextNodes because they lead to major formatting issues with
  Node.toprettyxml.
  """
  for element in node.childNodes:
    if element.nodeType == element.TEXT_NODE:
      if only_whitespace.match(element.data) is not None:
        node.removeChild(element)
        element.unlink()
  for element in node.childNodes:
    deleteEmptyTextNodes(element, indent = indent + '  ')


def run():
  """
  Main entery point.
  """
  dom = minidom.parse(infile)
  documents = dom.getElementsByTagNameNS(kml_ns,'Document')
  assert len(documents) == 1 # ensure that there is a kml:Document entry
  document = documents[0] 
  types = dict()

  deleteEmptyTextNodes(dom.documentElement) # remove empty TextNodes
  for placemark in dom.getElementsByTagNameNS(kml_ns,'Placemark'):
    descriptions = placemark.getElementsByTagNameNS(kml_ns,'description')
    assert len(descriptions) == 1
    description = descriptions[0]
    
    cdata = description.firstChild
    assert cdata.nodeType == minidom.Node.CDATA_SECTION_NODE

    # collect all the different bike routes
    desc_xml = minidom.parseString('<html><body>%s</body></html>' % cdata.data.encode('utf-8')) # wrap inline html
    dd = desc_xml.getElementsByTagName('dd')[0]
    t = dd.firstChild.data
    if t not in types:
      types[t] = []
    types[t].append(placemark)
    placemark.parentNode.removeChild(placemark)

    # delete description elements
    for d in placemark.getElementsByTagNameNS(kml_ns,'description'):
      d.parentNode.removeChild(d)
      d.unlink()
    
  #for k, v in types.iteritems():
  #  print k + ": " + str(len(v))
  
  # create Folders
  for k in types.iterkeys():
    data = dom.createTextNode(k)
    name = dom.createElementNS(kml_ns,'name')
    name.appendChild(data)
    f = dom.createElementNS(kml_ns,'Folder')
    f.appendChild(name)
    document.appendChild(f)

    # organize Placemarks in folders
    for n in types[k]:
      changeColor(k,n)
      f.appendChild(n)


  f = open(outfile, 'w')
  f.write(dom.toprettyxml(indent='  ', newl='\n', encoding='utf-8'))
  f.close()

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Reorganize ogdwien bicycle route kml file.')
  parser.add_argument('inputfile',  help='input kml file from ogdwien')
  parser.add_argument('outputfile', help='output file')

  args = parser.parse_args()
  infile = args.inputfile
  outfile = args.outputfile
  run()
