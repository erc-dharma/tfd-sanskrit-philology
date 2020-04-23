<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" indent="yes"/>

<!--<xsl:template match="*/text()[normalize-space()]">
    <xsl:value-of select="normalize-space()"/>
</xsl:template>

<xsl:template match="*/text()[not(normalize-space())]" />
-->

<xsl:template match="/">
<body>
<link rel="stylesheet" href="style_wrap.css"/>
       <xsl:apply-templates/>
<br/><br/><br/><br/>
</body>
</xsl:template>




<xsl:template match="TEXT">
	<xsl:apply-templates />
</xsl:template>    

<xsl:template match="PTEXT">
<!-- <font size="3" color="black"> -->
 &#160;&#160;&#160;<ptext><xsl:apply-templates /></ptext>
<!--</font>-->
</xsl:template>    


<xsl:template match="mainwrap">
<div class="tooltip-wrap"> 
<!-- <font size="3" color="black"> -->
	<versewrap><p><xsl:apply-templates /></p></versewrap>
<!--</font>-->
</div>
</xsl:template>    


<xsl:template match="apparatuswrap">
<div class="tooltip-content"> 
<!-- <font size="3" color="black"> -->
	<p><xsl:apply-templates /></p>
<!--</font>-->
</div>
</xsl:template>    


<xsl:template match="APP">
 <app>      <p><xsl:apply-templates /></p></app>

</xsl:template>    



<xsl:template match="colophon">
<br/>
<colophon>||<xsl:apply-templates />||</colophon>
</xsl:template>  
  
<xsl:template match="TITLE">
<h1>
|<xsl:apply-templates />|
</h1>
</xsl:template>    

<xsl:template match="CHAPTER">
<h2>[<xsl:apply-templates/>]</h2>
</xsl:template>    

<xsl:template match="SUBCHAPTER">
<h3>[<xsl:apply-templates/>]</h3>
</xsl:template>    



<xsl:template match="PVAR">
       <pvar><p><xsl:apply-templates /></p></pvar>
</xsl:template>    


<xsl:template match="PARAL">
	 <paral><p><xsl:apply-templates /></p></paral>
</xsl:template>    


<xsl:template match="TR">
    <p><trs> <hr style="width:50%;text-align:left;margin-left:0;color:#e6e6e6"/> "<xsl:apply-templates />"</trs></p>
</xsl:template>    

<xsl:template match="NOTE">
   <p><note>Note: <xsl:apply-templates /></note></p>
</xsl:template>    


<xsl:template match="SKT">
<!--<details open="yes">-->
	<i><xsl:apply-templates /></i>
</xsl:template>    


<xsl:template match="LEM">
<lem><xsl:apply-templates /></lem> 
] 
</xsl:template>    

<xsl:template match="ms">
<ms><xsl:apply-templates /></ms> 
</xsl:template>    

<xsl:template match="corr">
<corr><xsl:apply-templates /></corr> 
</xsl:template>    


<xsl:template match="vsnum">
<vsnum><xsl:apply-templates /></vsnum>
</xsl:template>    

<xsl:template match="NEWCHAPTER">
<xsl:apply-templates />
</xsl:template>    

<xsl:template match="uvaca">
<xsl:apply-templates />
</xsl:template>    


</xsl:stylesheet>
