<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    version="2.0">
    <!-- Kopiert alle Inhalte standardmäßig -->
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- Match auf das TEI-Tag -->
    <xsl:template match="tei:TEI">
        <xsl:copy>
            <!-- Füge das xml:id mit dem Dateinamen hinzu -->
            <xsl:attribute name="xml:id">
                <xsl:value-of select="tokenize(base-uri(.), '/')[last()]"/>
            </xsl:attribute>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    
    <xsl:template match="/">
        <!-- Hier werden die XML Files, die im Ordner meine-xml-dateien gespeichert werden, abgefragt. Das script.xsl sollte auf gleicher Ebene wie meine-xml-dateien Ordner gespeichert werden -->
        <xsl:for-each select="collection('n?recurse=yes;select=*.xml')">
            <xsl:result-document href="{tokenize(base-uri(.), '/')[last()]}">
            <xsl:apply-templates></xsl:apply-templates>
            </xsl:result-document>    
        </xsl:for-each>
    </xsl:template>
    
</xsl:stylesheet>