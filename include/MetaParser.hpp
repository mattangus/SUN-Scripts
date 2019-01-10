#pragma once
#include <libxml/xpath.h>

class MetaParser
{
private:
    std::string xmlStr;
public:
    void break_assert(bool cond, std::string statement)
    {
        if(!cond)
        {
            std::cout << statement << std::endl << "Terminating..." << std::endl;
            exit(1);
        }
    }

    void extract_imagesize(int xml_node)
    {
        //get image size
        // imagesizes = xml_node.xpathEval("//imagesize")
        // if len(imagesizes) == 0:
        //     #print("malformed document", xml_node)
        //     return None
        // break_assert(len(imagesizes) == 1, "found more than one image size")
        // imagesize = imagesizes[0]
        // all_rows = imagesize.xpathEval("nrows")
        // all_cols = imagesize.xpathEval("ncols")
        // break_assert(len(all_rows) == 1, "found more than one nrows")
        // break_assert(len(all_cols) == 1, "found more than one ncols")
        // rows = int(all_rows[0].content.strip())
        // cols = int(all_cols[0].content.strip())

        // return (rows, cols);
    }

    void extract_object(xmlXPathContextPtr xml_node)
    {
        //get name
        // names = xml_node.xpathEval("name")
        auto names = xmlXPathEval("name", xml_node);

        break_assert(len(names) == 1, "found more than one name")
        name = names[0].content.strip()

        //get the polygon
        polygons = xml_node.xpathEval("polygon")
        break_assert(len(polygons) == 1, "found more than one polygon")
        polygon = polygons[0]
        xs = polygon.xpathEval("pt/x")
        ys = polygon.xpathEval("pt/y")
        pts = [(int(x.content.strip()), int(y.content.strip())) for x,y in zip(xs,ys)]

        //get the username
        usernames = polygon.xpathEval("username")
        break_assert(len(usernames) == 1, "found more than one username")
        username = usernames[0].content.strip()

        // return name, pts, username
    }

    void processAnnot()
    {
        xmlDocPtr doc = xmlParseDoc(BAD_CAST xmlStr.c_str());
        xmlXPathContextPtr xpathCtx = xmlXPathNewContext(doc);
    }

    MetaParser(std::string xmlStr) : xmlStr(xmlStr)
    {
        //xmlStr.replace("\x1a", "");
    }
    ~MetaParser() { }
};