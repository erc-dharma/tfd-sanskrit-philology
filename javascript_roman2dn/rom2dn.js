// written by Csaba Kiss
// 14 June 2020, Naples

let dic = [
   // space:
    [' ', ' '],
    // comma:
   //[',', ' , '],
    // initial vowels:
    ['A','अ'],
    ['Ā','आ'],
    ['I', 'इ'],
    ['Ī','ई'],
    ['U', 'उ'],
    ['Ū', 'ऊ'], 
    ['Ṛ', 'ऋ'],
    ['Ṝ', 'ॠ'],
    ['E', 'ए'],
    ['O', 'ओ'],
    ['Đ', 'ऐ'],
    ['Ő', 'औ'],
    ["'", 'ऽ'],
    ['Ó', 'ॐ'],
    //  conjunct vowels:
    ['a', ''], ['ā', 'ा' ], ['i', 'ि'], ['ī', 'ी'], ['u', 'ु'],
    ['ū', 'ू'], ['ṛ', 'ृ'], ['ṝ', 'ॄ'], ['ḷ', 'ॢ '], 	 ['ḹ', 'ॣ'],
    ['e', 'े'], ['o', 'ो'], ['đ', 'ै'], ['ő','ौ'], ['ṃ', 'ं'], ['ḥ', 'ः'],
    // virāma:
    ['V', '्'],
    // consonants: 	 		 	
    ['k', 'क'], ['K', 'ख'], ['g', 'ग'], ['G', 'घ'], ['ṅ', 'ङ'],
    //
    ['c', 'च'], ['C', 'छ'], ['j', 'ज'],  ['J', 'झ'], ['ñ', 'ञ'],
    //	 	 	 	
    ['ṭ', 'ट'], ['Ṭ', 'ठ'], ['ḍ', 'ड'], ['Ḍ', 'ढ'], ['ṇ', 'ण'],
    // 
    ['t', 'त'], ['T', 'थ'], ['d','द'], ['D', 'ध'], ['n', 'न'],
    // 
    ['p', 'प'], ['P', 'फ'], ['b', 'ब'], ['B', 'भ'], ['m', 'म'],
    //
    ['y','य'], ['r','र'], ['l','ल'], ['v','व'], ['ś', 'श'], ['ṣ', 'ष'],
    ['s', 'स'], ['h', 'ह'], ['0', '०'],
        ['1', '१'], ['2', '२'], ['3', '३'], ['4', '४'], ['5', '५'], ['6', '६'],
        ['7', '७'], ['8', '८'], ['9', '९'] ] 


let vowels = ["ṃ", "ḥ", 'a', 'i', 'u', 'ṛ', 'ḷ', 'ā', 'ī', 'ū', 'ṝ', 'ḹ', 'e', 'ai', 'o', 'au', 'đ', 'ő']

let consonants = ["k", "K", "g", "G", "ṅ", "c", "C", "j", "J", "ñ", "ṭ", "Ṭ", "ḍ", "Ḍ", "ṇ", "t", "T", "d", "D", "n", "p", "P", "b", "B", "m", "y", "r", "l", "v", "ś", "ṣ", "s", "h"]

let preprocessing = [['ai', 'đ'], ['au', 'ő'], ['kh', 'K'], ['gh', 'G'], ['ṭh', 'Ṭ'], ['ḍh', 'Ḍ'], ['th', 'T'], ['dh', 'D'], ['ph', 'P'], ['bh', 'B'], ['ch', 'C'], ['jh', 'J'], ['\|', ' |'], ['{ }', '']]





function changeLetters() {

// collect Roman and (empty) Devanagari lines:
let roman_elem = document.getElementsByTagName("l");
let dn_elem = document.getElementsByTagName("dnl");
let roman_prep = [];

// preprocess
for (let a = 0; a < roman_elem.length; a++) {
        let preprocessed_line = roman_elem[a].innerHTML;
	for (let b = 0; b < preprocessing.length; b++) {
	  preprocessed_line = preprocessed_line.split(preprocessing[b][0]).join(preprocessing[b][1]);
	}
		roman_prep[a] = preprocessed_line + " ";
}

// change
	for (let d = 0; d < roman_prep.length; d++) {
		let rsplit = roman_prep[d].split('');
		let conjunct = false;
		for (let l = 0; l < rsplit.length; l++) {
			 if (l < rsplit.length && consonants.includes(rsplit[l]) && consonants.includes(rsplit[l+1]) ) {
			rsplit[l] = rsplit[l] + 'V';
 			  }


                // space
          	if (rsplit[l] === " "){		
		conjunct = false ;
			  }

                // sandhi C + V
          	if (l < rsplit.length-2 && consonants.includes(rsplit[l]) && rsplit[l+1] === " " && vowels.includes(rsplit[l+2])){		
		rsplit[l+1] = '' ;
			  }

                // sandhi C + C
          	if (l < rsplit.length-2 && consonants.includes(rsplit[l]) && rsplit[l+1] === " " && consonants.includes(rsplit[l+2])){		
		rsplit[l+1] = 'V' ;
			  }

		// if it is an initial consonant
		if (conjunct === false && consonants.includes(rsplit[l])) {
			rsplit[l] = rsplit[l];
			conjunct = true;
			}

		// if it is an initial vowel
		if (conjunct === false && vowels.includes(rsplit[l])) {
			rsplit[l] = rsplit[l].toUpperCase();
			}

                // if it is a last consonant: put in virāma
          if (l < rsplit.length && consonants.includes(rsplit[l]) && rsplit[l+1] === " "){		rsplit[l] = rsplit[l] + 'V';
			  }


		// change all into Devanagari
	   	 for (let rmchar = 0; rmchar < dic.length; rmchar++) {
			if (rsplit[l] === dic[rmchar][0]) {			
			 	rsplit[l]  = dic[rmchar][1];
			}
			if (rsplit[l].length === 2 && rsplit[l][0] === dic[rmchar][0])  {			
			 	rsplit[l] = dic[rmchar][1] + '्';
			}
                 }
		}
		rjoin = rsplit.join('');
		dn_elem[d].innerHTML = rjoin;
	}	





}




// when page loads
function init() {
		texts = document.getElementsByTagName("l");
		for (let y = 0; y < texts.length; y++) {
			texts[y].style.display = "block";
			}
		texts = document.getElementsByTagName("dnl");
		for (let y = 0; y < texts.length; y++) {
			texts[y].style.display = "none";
			}


}





function turnItToDevnag() {

// main transformation
changeLetters();

// hiding and displaying text
let elem = document.getElementById("switchbutton");
		if (elem.textContent=="[Click to switch to Devanāgarī]") {elem.textContent = "[Click to switch to Roman]";
		texts = document.getElementsByTagName("l");
		for (let y = 0; y < texts.length; y++) {
			texts[y].style.display = "none";
			}
		texts = document.getElementsByTagName("dnl");
		for (let y = 0; y < texts.length; y++) {
			texts[y].style.display = "block";
			}
		}
		else {elem.textContent = "[Click to switch to Devanāgarī]";
		texts = document.getElementsByTagName("l");
		for (let y = 0; y < texts.length; y++) {
			texts[y].style.display = "block";
			}
		texts = document.getElementsByTagName("dnl");
		for (let y = 0; y < texts.length; y++) {
			texts[y].style.display = "none";
			}
		}

}




