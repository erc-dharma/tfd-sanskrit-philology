
/* on click on the apparatus entry, close apparatus entry */
function hideFunction(id) {
 document.getElementById(id).style.display = "none";
  /* on click on line, also de-highlight translation*/
/* first change id format from e.g. '4.3cd' to 'tr4.3' */ 
    id = id.replace(/[a-z]/g, '');    
    var tr_id = 'tr' + id;
    var divid = document.getElementById(tr_id);
    divid.style.fontWeight = "normal";  
    divid.style.color = "#cc8800";
    

    var transl_class = 'trnsl' + id;
    var divclass = document.getElementsByClassName(transl_class);
    	for (let y = 0; y < divclass.length; y++) {
		divclass[y].style.fontWeight = 'normal';
		divclass[y].style.color = 'gray';}
 
} 

/* on click on line, open apparatus entry for line*/
function showApparatus(id) {
 document.getElementById(id).style.display = "block";
 /* on click on line, also highlight translation*/
/* first change id format from e.g. '4.3cd' to 'tr4.3' */ 
    id = id.replace(/[a-z]/g, '');    
    var tr_id = 'tr' + id;
    var divid = document.getElementById(tr_id);
    divid.scrollIntoView({block: "center"});  
    divid.style.fontWeight = "bold";  
    divid.style.color = "white";  
    
     var transl_class = 'trnsl' + id;
    var divclass = document.getElementsByClassName(transl_class);
    	for (let y = 0; y < divclass.length; y++) {
		divclass[y].style.fontWeight = 'bold';
		divclass[y].style.color = 'white';
			} 
} 

/* TO BE DELETED! Old function name; on click on line, open apparatus entry for line*/
function showFunction(id) {
 document.getElementById(id).style.display = "block";
 /* on click on line, also highlight translation*/
/* first change id format from e.g. '4.3cd' to 'tr4.3' */ 
    id = id.replace(/[a-z]/g, '');    
    var tr_id = 'tr' + id;
    var divid = document.getElementById(tr_id);
    divid.scrollIntoView({block: "center"});  
    divid.style.fontWeight = "bold";  
    divid.style.color = "white";  
    
     var transl_class = 'trnsl' + id;
    var divclass = document.getElementsByClassName(transl_class);
    	for (let y = 0; y < divclass.length; y++) {
		divclass[y].style.fontWeight = 'bold';
		divclass[y].style.color = 'white';
			} 
} 


/* on click on translation line, scroll to and highlight Skt*/
function showSkt(skt_class) {
 /* on click on line, also highlight translation*/
/* first change id format from e.g. '4.3cd' to 'tr4.3' */ 

/* Highlighting the Skt*/
    var divclass = document.getElementsByClassName(skt_class);
    var tr_class = skt_class.replace(/[a-z]/g, '');    
    var tr_class = 'trnsl' + tr_class; 
    var trclass =  document.getElementsByClassName(tr_class);

    	for (let y = 0; y < divclass.length; y++) {
    	
    	   if (divclass[y].style.fontWeight === 'bold') {
		divclass[y].style.fontWeight = 'normal';
		divclass[y].style.color = 'gray';
			/* Unhighlighting the translation on which you clicked*/
		    	for (let y = 0; y < trclass.length; y++) {
	        			trclass[y].style.fontWeight = 'normal';
				        trclass[y].style.color = 'gray';
                			}

                }
	   else {
		divclass[y].style.fontWeight = 'bold';
		divclass[y].style.color = 'white';
                 divclass[y].scrollIntoView({block: "center"});     
                 	/* Highlighting the translation on which you clicked*/  
		    	for (let y = 0; y < trclass.length; y++) {
	        			trclass[y].style.fontWeight = 'bold';
				        trclass[y].style.color = 'white';
                			}
		   }		
	
	}
} 



/* Experimental 
function rightclick(event, id) {
	if (event.button === 1) { */
		/* alert(event.button, id); */
	/*
		    var transl_class = 'trnsl' + id;
		    var divclass = document.getElementsByClassName(transl_class);
    		    for (let y = 0; y < divclass.length; y++) {
			divclass[y].style.fontWeight = 'bold';
			divclass[y].style.color = 'white';
	       	    }
	}
	event.preventDefault();
	return false;
}
*/

/* on load, close everything in apparatus */
function closeapp() {
	let t = document.getElementsByClassName('wrap-content');
	for (let y = 0; y < t.length; y++) {
		t[y].style.display = 'none';
	}
	/*also display only text */
	/*showonlytext();*/
	/* Change title of tab when page is loaded */
	t = document.getElementById('realtitle');
	document.getElementsByTagName('title')[0].innerHTML = t.innerHTML;
}

/* open all apparatus entries in one go, e.g. for searching; reverse of the above function with additional magnification etc. */
function openallapp() {
	let t = document.getElementsByClassName('wrap-content');
	let elem = document.getElementById("openallapp");
	if (elem.textContent=="Open all apparatus entries") {elem.textContent = "Close all apparatus entries";
		for (let y = 0; y < t.length; y++) {
		t[y].style.display = 'block';
		t[y].style.margin = '2em';
	}
	texts = document.getElementsByTagName("RMTEXT");
		for (let y = 0; y < texts.length; y++) {
			texts[y].style.fontSize = "120%";
			}	
	texts = document.getElementsByTagName("DNTEXT");
		for (let y = 0; y < texts.length; y++) {
			texts[y].style.fontSize = "120%";
			}	
		}
	else {elem.textContent = "Open all apparatus entries";
		for (let y = 0; y < t.length; y++) {
		t[y].style.display = 'none';
		t[y].style.margin = '0em';}
	texts = document.getElementsByTagName("RMTEXT");
		for (let y = 0; y < texts.length; y++) {
			texts[y].style.fontSize = "100%";
			}	
	texts = document.getElementsByTagName("DNTEXT");
		for (let y = 0; y < texts.length; y++) {
			texts[y].style.fontSize = "110%";
			}	

	}
}



function showNote(id) {
 /* on double click on line, scroll to note in note window*/
    var divid = document.getElementById(id);
    if (divid !== null) {
    divid.scrollIntoView(true);}
    /* Highlight translation */
    		    /* stip 'note' from id */
    		  /*    idscroll = id.replace(/[a-z]/g, '');    
		      var tr_id = 'tr' + idscroll;
		      var divid = document.getElementById(tr_id);
    	  	      divid.scrollIntoView({block: "center"});  
    		    var idstrip = id.slice(4);
		    var transl_class = 'trnsl' + idstrip;
		    var divclass = document.getElementsByClassName(transl_class)
		    
		   /* Toggle highligt and non-highlight translation */
    		 /*   for (let y = 0; y < divclass.length; y++) {
    		    	if (divclass[y].style.fontWeight == 'normal') {
				divclass[y].style.fontWeight = 'bold';
				divclass[y].style.color = 'white';
				}
	       	    	else {	divclass[y].style.fontWeight = 'normal';
				divclass[y].style.color = 'gray';
	       	    	}
	       	    }
*/
    return false;
}


function turnItDevnag() {

let elem = document.getElementById("switchbutton");
		if (elem.textContent=="Switch to Devanāgarī") {elem.textContent = "Switch to Roman";
		texts = document.getElementsByTagName("RMTEXT");
		for (let y = 0; y < texts.length; y++) {
			texts[y].style.display = "none";
			}
		texts = document.getElementsByTagName("DNTEXT");
		for (let y = 0; y < texts.length; y++) {
			texts[y].style.display = "inline";
			}
		texts = document.getElementsByTagName("DNLEM");
		for (let y = 0; y < texts.length; y++) {
			texts[y].style.display = "inline";
			}
		texts = document.getElementsByTagName("LEM");
		for (let y = 0; y < texts.length; y++) {
			texts[y].style.display = "none";
			}
		document.getElementById("sanskrittext").style.fontSize="130%";
		}
		else {elem.textContent = "Switch to Devanāgarī";
		texts = document.getElementsByTagName("RMTEXT");
		for (let y = 0; y < texts.length; y++) {
			texts[y].style.display = "inline";
			}
		texts = document.getElementsByTagName("DNTEXT");
		for (let y = 0; y < texts.length; y++) {
			texts[y].style.display = "none";
			}
		texts = document.getElementsByTagName("DNLEM");
		for (let y = 0; y < texts.length; y++) {
			texts[y].style.display = "none";
			}
		texts = document.getElementsByTagName("LEM");
		for (let y = 0; y < texts.length; y++) {
			texts[y].style.display = "inline";
			}
		document.getElementById("sanskrittext").style.fontSize="110%";		
		}

}




