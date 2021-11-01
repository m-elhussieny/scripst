import xml.etree.ElementTree as ET
import os
import sys
def genstnxml(filename, type="reference", slcdir="./data/slc", orbitdir="../data/orbits"):
    
    files = os.listdir(slcdir)
    time = files[0].split("_")[5]
    for file in files:
        if type == "reference":
            if time > file.split("_")[5]:
                time = file.split("_")[5]
        elif type == "secondary":
            if time < file.split("_")[5]:
                time = file.split("_")[5]
        else:
            print("you should specify your xml type reference of secondary ")
            sys.exit()
    slcdir = "../data/slc"
    slcfiles = []
    for file in files:
        if time in file:
            slcfiles.append(os.path.join(os.path.relpath(slcdir),file))
        
    root = ET.Element('component')
    root.set('name', type)
    root.text = "\n\t"

    safe = ET.Element('property')
    safe.set('name', 'safe')
    safe.text = str(slcfiles)
    safe.tail = "\n\t"
    root.append(safe)

    output = ET.Element('property')
    output.set('name', 'output directory')
    output.text = type
    output.tail = "\n\t"
    root.append(output)

    orbit = ET.Element('property')
    orbit.set('name', 'orbit directory')
    orbit.text = str(os.path.relpath(orbitdir))
    orbit.tail = "\n"
    root.append(orbit)

    tree = ET.ElementTree(root)

    with open(filename, "wb") as file:
        tree.write(file, encoding='utf-8', xml_declaration=True)


def genmodexml(filename, app="topsAPP", mode="topsinsar", sensor="SENTINEL1", 
                swath=[], rnglk=None, azmlk=None, area=[], refname='reference.xml', 
                secname='secondary.xml', unwrapp=False, unwrapp_method=""):
    root = ET.Element(app)
    root.text = "\n\t"

    comp = ET.Element('component')
    comp.set('name', mode)
    comp.text = "\n\t"
    comp.tail = "\n\t"
    root.append(comp)
    
    sens= ET.Element('property')
    sens.set('name', 'Sensor name')
    sens.text = sensor
    sens.tail = "\n\t"
    comp.append(sens)

    if swath:
        swth= ET.Element('property')
        swth.set('name', 'swath')
        swth.text = str(swath)
        swth.tail = "\n\t"
        comp.append(swth)

    if rnglk is not None:
        rnglks= ET.Element('property')
        rnglks.set('name', 'range looks')
        rnglks.text = str(rnglk)
        rnglks.tail = "\n\t"
        comp.append(rnglks)

    if azmlk is not None:
        azmlks= ET.Element('property')
        azmlks.set('name', 'azimuth looks')
        azmlks.text = str(azmlk)
        azmlks.tail = "\n\t"
        comp.append(azmlks)
    
    if area:
        rgn= ET.Element('property')
        rgn.set('name', 'region of interest')
        rgn.text = str(area)
        rgn.tail = "\n\t"
        comp.append(rgn)

    ref = ET.Element('component')
    ref.set('name', 'reference')
    ref.text = "\n\t\t"
    ref.tail = "\n\t"
    refcat = ET.Element("catalog")
    refcat.text = refname
    refcat.tail = "\n\t"
    ref.append(refcat)
    comp.append(ref)

    sec = ET.Element('component')
    sec.set('name', 'secondary')
    sec.text = "\n\t\t"
    sec.tail = "\n\t"
    seccat = ET.SubElement(sec, "catalog")
    seccat.text = secname
    seccat.tail = "\n\t"
    comp.append(sec)

    if unwrapp:
        if not unwrapp_method:
            print("you must spcifiy unwrappping method (i.e. icu, snaphu, snaphu_mcf)")
            import sys; sys.exit()

        unwrap = ET.Element('property')
        unwrap.set('name', 'do unwrap')
        unwrap.text = str(unwrapp)
        unwrap.tail = "\n\t"
        root.append(unwrap)
        mthd = ET.Element('property')
        mthd.set('name', 'unwrapper name')
        mthd.text = str(unwrapp_method)
        mthd.tail = "\n\t"
        comp.append(mthd)
    

    
    tree = ET.ElementTree(root)
    with open(filename, "wb") as file:
        tree.write(file, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    genstnxml("ref.xml", "reference")
    kwargs = {"unwrapp"        :True,
              "unwrapp_method" : "snaphu_mcf",
              "area"           : [118, 120, 39, 40],
              "rnglk"          : 7,
              "azmlk"          : 3,
              "swath"          : [1, 2, 3]
              }
    genmodexml("topsApp.xml", **kwargs)

  