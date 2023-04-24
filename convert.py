from python_gedcom_2.element.element import Element
from python_gedcom_2.element.family import FamilyElement
from python_gedcom_2.element.individual import IndividualElement
from python_gedcom_2.parser import Parser
from python_gedcom_2.tags import *
import os
import sys

if (len(sys.argv) < 3):
    exit('Missing file arguments for input and output - must be a .ged files')
input_file = sys.argv[1]
output_file = sys.argv[2]

gedcom_parser = Parser()
gedcom_parser.parse_file(input_file)
root_child_elements = gedcom_parser.get_root_child_elements()

for element in root_child_elements:

    children = element.get_child_elements()
    children_indicies_to_delete = []

    if isinstance(element, Element):
        if element.get_tag() == 'HEAD':
            for head_child_element in children:
                if head_child_element.get_tag() == GEDCOM_TAG_GEDCOM:
                    print('adding FORM LINEAGE-LINKED')
                    head_child_element.new_child_element(GEDCOM_TAG_FORMAT, '', 'LINEAGE-LINKED')
                if head_child_element.get_tag() == GEDCOM_TAG_CHARACTER:
                    print('setting CHAR to ANSEL')
                    head_child_element.set_value('ANSEL')
                if head_child_element.get_tag() == GEDCOM_TAG_LANGUAGE:
                    has_lang = True
            print('setting LANG to English')
            element.new_child_element(GEDCOM_TAG_LANGUAGE, value='English')
            print('adding SUBM')
            element.new_child_element(GEDCOM_TAG_SUBMITTER, value='@U1@')
            root_child_elements.insert(1, Element(0, '@U1@', GEDCOM_TAG_SUBMITTER, ''))
            root_child_elements[1].new_child_element(GEDCOM_TAG_NAME, value=os.getlogin())
        if element.get_tag() == GEDCOM_TAG_NOTE:
            if children[0].get_tag() == GEDCOM_TAG_NOTE:
                print('converting 1 NOTE to 1 CONC from ' + element.get_pointer())
                children_indicies_to_delete.append(0)
                element.new_child_element(GEDCOM_TAG_CONCATENATION, value=children[0].get_value())


    if isinstance(element, IndividualElement):
        for idx, individual_child_element in enumerate(children):
            (first, last) = element.get_name()
            if individual_child_element.get_tag() == GEDCOM_TAG_ADDRESS:
                print('removing ADDR from ' + first + ' ' + last)
                children_indicies_to_delete.append(idx)
            elif individual_child_element.get_tag() == 'EMAL':
                print('removing EMAL from ' + first + ' ' + last)
                children_indicies_to_delete.append(idx)
            elif individual_child_element.get_tag() == 'NAMR':
                print('removing NAMR from ' + first + ' ' + last)
                children_indicies_to_delete.append(idx)
            elif individual_child_element.get_tag() == 'MILI':
                print('converting MILI to NOTE from ' + first + ' ' + last)
                children_indicies_to_delete.append(idx)
                element.new_child_element('NOTE', value=individual_child_element.get_value())

    elif isinstance(element, FamilyElement):
        for idx, family_child_element in enumerate(children):
            if family_child_element.get_tag() == GEDCOM_TAG_ADDRESS:
                print('removing ADDR from ' + element.get_pointer())
                children_indicies_to_delete.append(idx)
            elif family_child_element.get_tag() == 'CLAW':
                print('converting CLAW to MARR TYPE from ' + element.get_pointer())
                children_indicies_to_delete.append(idx)
                marriage_child_element = element.new_child_element(GEDCOM_TAG_MARRIAGE)
                marriage_child_element.new_child_element(GEDCOM_TAG_TYPE, value='Common Law')

    for idx in children_indicies_to_delete:
        del(children[idx])

gedcom_parser.save_gedcom(open(output_file, 'w'))

# Strip blank lines
# For some reason, the method above adds a blank line after every real line
result = ''
with open(output_file, 'r+') as f:
    for line in f:
        if not line.isspace():
            result += line

    f.seek(0)
    f.write(result)
    f.truncate()
