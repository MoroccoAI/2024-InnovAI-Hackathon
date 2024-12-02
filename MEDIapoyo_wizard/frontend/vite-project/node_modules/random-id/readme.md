#randomID

Generates a customisable random ID, for node and browsers.

##Installation

Node

	npm install random-id

Browsers

	<script type="text/javascript" src="randomID.js"></script>

##Usage

	//var randomID = require("random-id");

	var id = randomID(length, pattern);

##Options

- **length**: *(Number)* The length of the random String, default: 30

- **pattern**: *(String)* Specificies the possible characters to be used to generate the string, eg. `"aA"` would generate a string made out of lowercase and uppercase characters. Defaults to `aA0`;

	- any lowercase character: includes a-z
	- any uppercase character: includes A-Z
	- any number: includes 0-9
	- anything else: includes special characters (~!@#$%^&()_+-={}[];\',)


##Examples

	randomID(); 			//oOskDVlsS002iszDIcrWqdckY8aM8k
	randomID(10); 			//JcWtjGmfNN

	randomID(20,"a");		//ffeckzhgastisvtzuvcc
	randomID(20,"A");		//TZBUJIZNSSSBDSLBXRHI
	randomID(20,"aA");		//JENxBtFYMyUuphewMjRd
	
	randomID(20,"0")		//32730290429542918140
	
	randomID(20,"!")		//)_§Â%-(§Â-%:(.$??$=^ 
	
	randomID(20,"aA0!")		//A9!M`kKRu1)MgUN´UhpM 
	
	//increasing chances
	randomID(20,"aaaaa0")	//xujitsji9nxvouydkjkl

