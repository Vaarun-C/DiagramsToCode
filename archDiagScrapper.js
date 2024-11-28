var mycount = temp0;
var myTable = temp1;
var NEXT_LINK = temp2;
var links_1 = []
function getLinks(){
	for (let lielem of myTable.children){
    links_1.push(
			lielem.getElementsByTagName('h2')[0].getElementsByTagName('a')[0].href
    );
	}
	let x = mycount.innerText.split(' ')
	if(x[0].split('-')[1] == x[1].replace('(', '').replace(')',''))return;
	NEXT_LINK.click();
	setTimeout(getLinks,500)
}
getLinks();

