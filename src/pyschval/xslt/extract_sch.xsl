<?xml version="1.0" encoding="utf-8"?>
<!-- Adapted from https://github.com/TEIC/Stylesheets/blob/dev/odds/extract-sch.xsl -->
<xsl:stylesheet xmlns:teix="http://www.tei-c.org/ns/Examples"
                xmlns:xi="http://www.w3.org/2001/XInclude" xmlns:rng="http://relaxng.org/ns/structure/1.0"
                xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                xmlns="http://purl.oclc.org/dsdl/schematron" xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
                exclude-result-prefixes="tei rng teix sch xi xs #default">
    
    
    <xsl:output encoding="utf-8" indent="yes" method="xml"/>
    <xsl:param name="lang"/>
    
    <xsl:key name="NS" match="sch:ns" use="1"/>
    
    <xsl:key name="PATTERNS" match="sch:pattern" use="1"/>
    
    
    <xsl:template match="/">
        <schema queryBinding="xslt2">
            <title>Extracted Schematron Rules</title>
            <xsl:for-each select="key('NS', 1)">
                <xsl:choose>
                    <xsl:when test="ancestor::teix:egXML"/>
                    <xsl:when test="
                        ancestor::tei:constraintSpec/@xml:lang
                        and not(ancestor::tei:constraintSpec/@xml:lang = $lang)"/>
                    <xsl:otherwise>
                        <xsl:apply-templates select="."/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
            <xsl:for-each select="key('PATTERNS', 1)">
                <xsl:choose>
                    <xsl:when test="ancestor::teix:egXML"/>
                    <xsl:when test="
                        ancestor::tei:constraintSpec/@xml:lang
                        and not(ancestor::tei:constraintSpec/@xml:lang = $lang)"/>
                    <xsl:otherwise>
                        <xsl:apply-templates select="."/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
        </schema>
    </xsl:template>
    
    <xsl:template match="@* | text() | comment() | processing-instruction()">
        <xsl:copy-of select="."/>
    </xsl:template>
    
    
    <xsl:template match="sch:*">
        <xsl:element name="{local-name()}">
            <xsl:apply-templates select="* | @* | processing-instruction() | comment() | text()"/>
        </xsl:element>
    </xsl:template>
    
    
    <doc xmlns="http://www.oxygenxml.com/ns/doc/xsl">
        <desc>work out unique ID for generated Schematron</desc>
    </doc>
    <xsl:function name="tei:makePatternID" as="xs:string">
        <xsl:param name="context"/>
        <xsl:for-each select="$context">
            <xsl:variable name="num">
                <xsl:number level="any"/>
            </xsl:variable>
            <xsl:value-of select="(../ancestor::*[@ident]/@ident, 'constraint', ../@ident, $num)"
                          separator="-"/>
        </xsl:for-each>
    </xsl:function>
    
    
</xsl:stylesheet>
