function reverse(){

    var t = document.getElementById("target");
    var word = document.getElementById('text').value;
    t.innerHTML = word.split("").reverse().join("");
}

function generateMultiples(num, len) {
	var arr = [];
	for (var i = 1; i <=len; i++) {
		arr.push(i*num)
	}
	return arr;
}


function render(){
    var t = document.getElementById("table");
    var num = document.getElementById('num').value;
    t.innerHTML = generateTables(num, 20);

}

function generateTables(num, len) {
  var	nums = generateMultiples(num, len);
	  // DRAW THE HTML TABLE
  var rowlen = 5, // 3 items per row
      html = "<table><tr>";

  // Loop through array and add table cells
  for (var i=0; i<nums.length; i++) {
    html += "<td>" + nums[i] + "</td>";
    // Break into next row
    var next = i+1;
    if (next%rowlen==0 && next!=nums.length) {
      html += "</tr><tr>";
    }
  }
  html += "</tr></table>";
  return html
}


