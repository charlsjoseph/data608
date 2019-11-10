/*
*    main.js
*    Mastering Data Visualization with D3.js
*    2.5 - Activity: Adding SVGs to the screen
*/
var presidentData = [];
d3.csv("data/presidents.csv").then(function(csv_data) {
  
  presidentData = csv_data;
  tabulate(presidentData, ["President Name", "Height", "Weight"], ["Name", "Height", "Weight"]);
});

function search() {
	var search = document.getElementById('name').value;
	var serachresult = presidentData.find(president => president.Name.toLowerCase().includes(search.toLowerCase()))
	var t = document.getElementById("searchTarget");
	console.log(serachresult)
	if (serachresult) {
    	t.innerHTML = "President Name: " + serachresult.Name + ", Height :" + serachresult.Height  + ", Weight: " + serachresult.Weight

	} else {
		t.innerHTML = 'Not found';
	}
}

function tabulate(data, display_columns, backend_columns) {
    var table = d3.select("#tableId").append("table")
            .attr("style", "margin-left: 20px"),
        thead = table.append("thead")
        tbody = table.append("tbody");
    thead.append("tr")
        .selectAll("th")
        .data(display_columns)
        .enter()
        .append("th")
            .text(function(column) { return column; });
    var rows = tbody.selectAll("tr")
        .data(data)
        .enter()
        .append("tr");
    var cells = rows.selectAll("td")
        .data(function(row) {
            return backend_columns.map(function(column) {
                return {column: column, value: row[column]};
            });
        })
        .enter()
        .append("td")
        .attr("style", "font-family: Courier") // sets the font style
            .html(function(d) { return d.value; });
    
}