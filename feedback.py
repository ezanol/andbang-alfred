from xml.etree import ElementTree as ET

def feedback(items):
    feedback = ET.Element("items")
    
    def processItem(item):
        itemToAdd = ET.SubElement(feedback, "item")

        data = item

        for (k, v) in data["attrib"].iteritems():
            if v is None:
                continue
            itemToAdd.set(k, v)

        for (k, v) in data["content"].iteritems():
            if v is None:
                continue
            if k != "fileIcon" and k != "fileType":
                child = ET.SubElement(itemToAdd, k)
                child.text = v
            if k == "icon":
                if "fileIcon" in data["content"].keys():
                    if data["content"]["fileIcon"] == True:
                        child.set("type", "fileicon")
                if "fileType" in data["content"].keys():
                    if data["content"]["fileType"] == True:
                        child.set("type", "filetype")

    if isinstance(items, list):
        for anItem in items:
            processItem(anItem)
    else:
        processItem(items)

    print ET.tostring(feedback, encoding="utf-8")

def convert_item(data):
    content = {
        "title": data['title'],
        "subtitle": data['subtitle'],
        "icon": data['icon'],
        "fileIcon": data['fileIcon'],
        "fileType": data['fileType']
    }
    attrib = {
        "uid": data['uid'],
        "valid": data['valid'],
    }
    if data['autocomplete']:
        attrib["autocomplete"] = data['autocomplete']
    if data['arg']:
        if "\n" in data['arg']:
            content["arg"] = data['arg']
        else:
            attrib["arg"] = data['arg']
    if data['type']:
        attrib["type"] = data['type']

    data = {"attrib": attrib, "content": content}

    return data

def item(**kwargs):
    data = {}
    data['title'] = kwargs.pop("title", "")
    data['subtitle'] = kwargs.pop("subtitle", "")
    data['uid'] = kwargs.pop("uid", None)
    if "valid" in kwargs.keys():
        if kwargs["valid"] == True:
            data['valid'] = "yes"
        elif kwargs["valid"] == False:
            data['valid'] = "no"
        else:
            data['valid'] = kwargs["valid"]
        kwargs.pop("valid")
    else:
        data['valid'] = None
    data['autocomplete'] = kwargs.pop("autocomplete", None)
    data['icon'] = kwargs.pop("icon", "icon.png")
    data['fileIcon'] = kwargs.pop("fileIcon", False)
    data['fileType'] = kwargs.pop("fileType", False)
    data['arg'] = kwargs.pop("arg", None)
    data['type'] = kwargs.pop("type", None)
    return convert_item(data)

