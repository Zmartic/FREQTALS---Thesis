#!/usr/bin/env python3
#import xml.parsers
#import xml.dom
import sys
#import xml.dom.minidom


"""

import org.w3c.dom.Document;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Vector;
import java.io.File;
import java.io.FileWriter;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Source;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;
"""
"""
 * Utility Class for formatting XML
 *
 * @author Pankaj
 *
"""
class XmlFormatter:

    sep = "\\"  #File.separator

    #format one xml file
    def format(self, inPath, outPath):
        try:
            f = open(str(inPath), "r")
            #BufferedReader br = new BufferedReader(new FileReader(inPath));
            fileContent = ""
            uniCode = u"\uFEFF"
            line = f.readline()
            if uniCode in line:
                line = line[1:]
            fileContent += line.strip()  #remove unnecessary space
            line = f.readline()
            while line:
                if len(line.strip()) != 0:
                    fileContent += line.strip()
                line = f.readline()

            """
            Transformer transformer = TransformerFactory.newInstance().newTransformer();
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty(OutputKeys.DOCTYPE_PUBLIC, "yes");
            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
            StringWriter stringWriter = new StringWriter();
            transformer.transform(
                    new StreamSource(new StringReader(fileContent)),
                    new StreamResult(stringWriter));
            """

            file = open(outPath)
            file.write(fileContent.strip())
            file.flush()
            file.close()
        except:
            e = sys.exc_info()[0]
            print("Exception while reading file " + inPath + "\n")
            print("Error: " + str(e) + "\n")
            raise