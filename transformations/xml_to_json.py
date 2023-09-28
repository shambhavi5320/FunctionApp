def xml_to_dict(element):
    result = {}
    stack = [(element, result)]

    while stack:
        current_element, current_dict = stack.pop()
        tag = current_element.tag.split('}', 1)[-1]

        if tag in current_dict:
            if not isinstance(current_dict[tag], list):
                current_dict[tag] = [current_dict[tag]]  # Convert to a list if it's not
            current_dict[tag].append({})

            # Push child elements onto the stack
            for child in current_element:
                stack.append((child, current_dict[tag][-1]))
        else:
            if len(current_element) == 0:
                current_dict[tag] = current_element.text
            else:
                current_dict[tag] = {}

                # Push child elements onto the stack
                for child in current_element:
                    stack.append((child, current_dict[tag]))

    return result

# This is working for post complaints
# def xml_to_dict(element):
#     stack = [(element, {})]  # Initialize a stack with the root element and an empty dictionary
#     result = {}

#     while stack:
#         current_element, current_dict = stack.pop()

#         tag = current_element.tag.split('}', 1)[-1]

#         if tag in current_dict:
#             if not isinstance(current_dict[tag], list):
#                 current_dict[tag] = [current_dict[tag]]  # Convert to a list if it's not
#             current_dict[tag].append(current_element.text)
#         else:
#             current_dict[tag] = current_element.text if len(current_element) == 0 else {}

#         for child in current_element:
#             stack.append((child, current_dict[tag]))  # Add child elements to the stack

#         if current_element is element:
#             result = current_dict  # Update the result when we reach the root element

#     return result

# def xml_to_dict(element):
#     result = {}
#     if len(element) == 0:
#         return element.text
#     tag = element.tag.split('}', 1)[-1]

#     # Check if the tag already exists in the result dictionary and ensure it's a dictionary
#     if tag in result:
#         if not isinstance(result[tag], list):
#             result[tag] = [result[tag]]  # Convert to a list if it's not
#         result[tag].append(xml_to_dict(element))
#     else:
#         # If it's a single child, treat it as a dictionary
#         if len(element) == 1 and element[0].tag.split('}', 1)[-1] == tag:
#             result[tag] = xml_to_dict(element[0])
#         else:
#             result[tag] = xml_to_dict(element)

#     return result if result else element.text

# def xml_to_dict(element):
#     result = {}

#     # Remove namespace prefix from the tag
#     tag = element.tag.split('}', 1)[-1]

#     # Check if the element has child elements
#     if len(element) > 0:
#         for child in element:
#             child_data = xml_to_dict(child)
#             if child_data:
#                 # Handle elements with namespaces
#                 child_tag = child.tag.split('}', 1)[-1]
#                 result[child_tag] = child_data
#     else:
#         # If no child elements, use the element's text content
#         result[tag] = element.text if element.text else ""

#     return result

# def remove_empty_dicts(data):
#     if isinstance(data, dict):
#         return {key: remove_empty_dicts(value) for key, value in data.items() if value}
#     elif isinstance(data, list):
#         return [remove_empty_dicts(item) for item in data if item]
#     else:
#         return data




    # for child in element:
    #     child_data = xml_to_dict(child)
    #     child_tag = child.tag
    #     if '}' in child_tag:
    #         child_tag = child_tag.split('}', 1)[1]  # Remove namespace prefix
    #     if child_tag in result:
    #         if type(result[child_tag]) is list:
    #             result[child_tag].append(child_data)
    #         else:
    #             result[child_tag] = [result[child_tag], child_data]
    #     else:
    #         result[child_tag] = child_data

    # return result

# def xml_to_dict(element):
#     result = {}
#     if len(element) == 0:
#         return element.text

#     for child in element:
#         child_data = xml_to_dict(child)
#         child_tag = child.tag
#         if '}' in child_tag:
#             child_tag = child_tag.split('}', 1)[1]  # Remove namespace prefix
#         if child_tag in result:
#             if type(result[child_tag]) is list:
#                 result[child_tag].append(child_data)
#             else:
#                 result[child_tag] = [result[child_tag], child_data]
#         else:
#             result[child_tag] = child_data

#     return result

# def xml_to_json(element):
#     if len(element) == 0:
#         return element.text
#     result = {}
#     for child in element:
#         child_data = xml_to_json(child)
#         if child.tag in result:
#             if type(result[child.tag]) is list:
#                 result[child.tag].append(child_data)
#             else:
#                 result[child.tag] = [result[child.tag], child_data]
#         else:
#             result[child.tag] = child_data
#     return result  # Change this line to return the result directly


# def xml_to_json(element):
#     if len(element) == 0:
#         return element.text

#     result = {}
#     for child in element:
#         child_data = xml_to_json(child)
#         # Remove namespace information from the child tag
#         child_tag = child.tag.split('}')[-1]
#         if child_tag in result:
#             if type(result[child_tag]) is list:
#                 result[child_tag].append(child_data)
#             else:
#                 result[child_tag] = [result[child_tag], child_data]
#         else:
#             result[child_tag] = child_data

#     return result