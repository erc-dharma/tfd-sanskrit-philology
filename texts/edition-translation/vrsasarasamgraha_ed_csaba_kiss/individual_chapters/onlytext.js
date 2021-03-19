/* controls, i.e. switches on and off, the four panels */
function showonlytext() {

 	t = document.getElementById('translation');
	t.style.display = "none";
 	t.style.display = "none";	

 	n = document.getElementById('notes')
	n.style.display = "none";
 	n.style.display = "none";		

 	m = document.getElementById('mssimages');
	m.style.display = "none";
 	m.style.display = "none";		

 	s = document.getElementById('sanskrittext')
	s.style.width = "100%";
 	s.style.height = "100%";		
 	s.style.display = "block";
        s.style.padding = "20px";	

 	b = document.getElementById('showonlytext');
	b.style.backgroundColor  = "#cc8800";
	b.style.color  = "black";
 	b = document.getElementById('showtextandtranslation');
	b.style.backgroundColor  = "black";
	b.style.color  = "#cc8800";
 	b = document.getElementById('txttrnotes');
	b.style.backgroundColor  = "black";
	b.style.color  = "#cc8800";
 	b = document.getElementById('all');
	b.style.backgroundColor  = "black";
	b.style.color  = "#cc8800";
} 


function showtextandtranslation() {
 	n = document.getElementById('notes');
	n.style.display = "none";

 	m = document.getElementById('mssimages');
	m.style.display = "none";

 	s = document.getElementById('sanskrittext');
	s.style.width = "50%";
 	s.style.height = "100%";		
 	s.style.display = "block";	
        s.style.padding = "20px";	
	

 	t = document.getElementById('translation');
	t.style.width = "50%";
 	t.style.height = "100%";
 	t.style.left = "50%";		
 	t.style.top = "0%";
 	t.style.display = "block";	
        t.style.padding = "20px";

 	b = document.getElementById('showonlytext');
	b.style.backgroundColor  = "black";
	b.style.color  = "#cc8800";
 	b = document.getElementById('showtextandtranslation');
	b.style.color  = "black";
	b.style.backgroundColor  = "#cc8800";	
 	b = document.getElementById('txttrnotes');
	b.style.backgroundColor  = "black";
	b.style.color  = "#cc8800";
 	b = document.getElementById('all');
	b.style.backgroundColor  = "black";
	b.style.color  = "#cc8800";
		
} 

function showtexttrnotes() {
 	m = document.getElementById('mssimages');
	m.style.display = "none";
 	m.style.display = "none";		


 	s = document.getElementById('sanskrittext');
 	s.style.top = "0%";	
	s.style.width = "50%";
 	s.style.height = "100%";		
 	s.style.display = "block";	
        s.style.padding = "20px";	


 	n = document.getElementById('notes');
	n.style.display = "block";
 	n.style.height = "42%";	
 	n.style.width = "50%";	
 	n.style.top = "60%";	
 	n.style.left = "50%";	
        n.style.padding = "20px";	
	
 	t = document.getElementById('translation');
	t.style.width = "50%";
 	t.style.height = "100%";
 	t.style.left = "50%";		
 	t.style.top = "0%";
 	t.style.display = "block";	
        t.style.padding = "20px";	

 	b = document.getElementById('showonlytext');
	b.style.backgroundColor  = "black";
	b.style.color  = "#cc8800";
 	b = document.getElementById('showtextandtranslation');
	b.style.backgroundColor  = "black";
	b.style.color  = "#cc8800";
 	b = document.getElementById('txttrnotes');
	b.style.backgroundColor  = "#cc8800";
	b.style.color  = "black";
 	b = document.getElementById('all');
	b.style.backgroundColor  = "black";
	b.style.color  = "#cc8800";

} 

function showtextANDnotes() {


 	m = document.getElementById('mssimages');
	m.style.display = "none";
 	m.style.display = "none";		


 	s = document.getElementById('sanskrittext');
 	s.style.top = "0%";	
	s.style.width = "50%";
 	s.style.height = "100%";		
 	s.style.display = "block";	
        s.style.padding = "20px";	


 	n = document.getElementById('notes');
	n.style.display = "block";
 	n.style.height = "100%";	
 	n.style.width = "50%";	
 	n.style.top = "0%";	
 	n.style.left = "50%";	
        n.style.padding = "20px";	
	
 	t = document.getElementById('translation');
	t.style.width = "50%";
 	t.style.height = "100%";
 	t.style.left = "50%";		
 	t.style.top = "0%";
 	t.style.display = "none";	
        t.style.padding = "20px";	

 	b = document.getElementById('showonlytext');
	b.style.backgroundColor  = "black";
	b.style.color  = "#cc8800";
 	b = document.getElementById('showtextandtranslation');
	b.style.backgroundColor  = "black";
	b.style.color  = "#cc8800";
 	b = document.getElementById('txttrnotes');
	b.style.backgroundColor  = "#cc8800";
	b.style.color  = "black";
 	b = document.getElementById('all');
	b.style.backgroundColor  = "black";
	b.style.color  = "#cc8800";

} 




function showall() {
 	m = document.getElementById('mssimages');
	m.style.height = "40%";	
 	m.style.width = "47.5%";	
 	m.style.top = "60%";	
 	m.style.left = "0%";	
 	m.style.display = "block";
        m.style.padding = "20px";	

 	n = document.getElementById('notes');
	n.style.display = "block";
 	n.style.height = "42%";	
 	n.style.width = "50%";	
 	n.style.top = "60%";	
 	n.style.left = "50%";	
        n.style.padding = "20px";	

 	s = document.getElementById('sanskrittext');
	s.style.width = "50%";
 	s.style.height = "58%";		
 	s.style.display = "block";	
        s.style.padding = "20px";	

 	t = document.getElementById('translation');
	t.style.height = "60%";
 	t.style.width = "49%";
 	t.style.top = "0%";
 	t.style.left = "50%";		
 	t.style.display = "block";	
        t.style.padding = "20px";	
	
 	b = document.getElementById('showonlytext');
	b.style.backgroundColor  = "black";
	b.style.color  = "#cc8800";
 	b = document.getElementById('showtextandtranslation');
	b.style.backgroundColor  = "black";
	b.style.color  = "#cc8800";
 	b = document.getElementById('txttrnotes');
	b.style.backgroundColor  = "black";
	b.style.color  = "#cc8800";	
 	b = document.getElementById('all');
	b.style.backgroundColor  = "#cc8800";
	b.style.color  = "black";

} 



/* Pressing keys on the keyboard trigger events */
document.onkeypress=function(e){
 var e = window.event || e
 /* To check character codes */
 /*alert("CharCode value: "+e.charCode)
 alert("Character: "+String.fromCharCode(e.charCode)) */
 /* d for Devanagari and back */
 
 if (e.charCode === 100) {
 turnItDevnag();
 };
 
 /* s for Skt */
 if (e.charCode === 115) {
 showonlytext();
 }

 /* toggle Tr with 't'*/
 if (e.charCode === 116) {
   	t = document.getElementById('translation');
 	n = document.getElementById('notes');
   	if (t.style.display === "none" && n.style.display != "block") {
			showtextandtranslation();

   	}
   	else if (t.style.display === "block" && n.style.display != "none") {
			showtextANDnotes();

   	}
   	else if (t.style.display === "none" && n.style.display != "none") {
			showtexttrnotes();

   	}
   	else {
			showonlytext();
   	}
  }


 /* toggle notes with 'n'  */
 if (e.charCode === 110) {
 	n = document.getElementById('notes');
   	t = document.getElementById('translation');
   	/* tr is on but notes are not: show skt, tr, notes */
   	if (n.style.display != "block" && t.style.display !== "none") {
   				showtexttrnotes();
   	}
   	/* skt, tr, notes are on; swith off notes */
   	else if (n.style.display !== "none" && t.style.display === "block") {
			showtextandtranslation();
   	}
   	/* tr is off show skt and notes */
   	else if (n.style.display != "block" && t.style.display != "block") {
   				showtextANDnotes();
   	}
   	/* tr is off, skt is on, switch off notes */
   	else if (n.style.display != "none" && t.style.display != "block") {
   				showonlytext();
   	}
  }


 /* a for All incl. link to images */
 if (e.charCode === 97) {
 showall();
 }
 
 /* o for Open all apparatus entries */
 if (e.charCode === 111) {
 openallapp();
 }

}


