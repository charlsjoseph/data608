function updatebarchart() {

// set the dimensions and margins of the graph
var margin = {top: 80, right: 30, bottom: 80, left: 250},
    barwidth = 900 - margin.left - margin.right,
    barheight = 500 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#topcounties")
  .append("svg")
    .attr("width", barwidth + margin.left + margin.right)
    .attr("height", barheight + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

	// X Label
svg.append("text")
    .attr("class", "x axis-label")
    .attr("x", barwidth / 2)
    .attr("y", barheight + 60)
    .attr("font-size", "15px")
    .attr("font-weight", "bold")
    .attr("text-anchor", "middle")
    .text("Top Polluted States/Counties: Based on number of times AQI crossed 200 limit (Very Un-Healthy)");

var topStates 
// Parse the Data
d3.json("http://localhost:5000/toppolutedcounties", function(data) {

var keys = [ 'NO2-AQI' ,'SO2-AQI' ,'CO-AQI', 'O3-AQI' ];

for (i = 0 ; i< data.length; i++) {
	t = 0;
	for (j = 0; j < keys.length; j++) 
		t = t +  data[i][keys[j]];
	data[i]['total'] = t
}
topstatescounties = data
              .map(p => p.State + '-' +  p.County )
              .filter((state, index, arr) => arr.indexOf(state) == index)
              .sort();

var stateDropdown = document.getElementById('state-county');

  for (var i = 0 ; i<topstatescounties.length; i++) {
    stateDropdown.options[i] = new Option(topstatescounties[i], topstatescounties[i]);
  }
stateDropdown.value = 'California-Los Angeles'
updateLineChart();

		data.total = t; 
		data =data.sort(function(a, b) { return b['total'] - a['total']; });

  console.log(data)
  // Add X axis
  var x = d3.scaleLinear()
    .domain([0, d3.max(data, function(d) { return d.total; })])
    .range([ 0, barwidth]);
  svg.append("g")
    .attr("transform", "translate(0," + barheight + ")")
    .call(d3.axisBottom(x).tickFormat(function(d){return d/1000 + "k"}))
    .selectAll("text")
      .attr("font-family", "sans-serif")
      .attr("font-size", "12px")
      .attr("text-anchor", "end")
	  .attr("transform", "rotate(-45)")

  // Y axis
  var y = d3.scaleBand()
    .range([ 0, barheight ])
    .domain(data.map(function(d) { return d.State.concat(" - ").concat(d.County); }))
    .padding(.2);
  svg.append("g")
    .call(d3.axisLeft(y))
    .selectAll("text")
      .attr("font-family", "sans-serif")
      .attr("font-size", "12px")
      .attr("text-anchor", "end")
	
var z = d3.scaleOrdinal()
    .range([ "#dfc27d", "#80cdc1", "#018571", "#a6611a"]);


  //Bars
  g= svg.append("g")
	.selectAll("g")
    .data(d3.stack().keys(keys)(data))
	.enter().append("g")
      .attr("fill", function(d) { return z(d.key); })
	.selectAll("rect")
		.data(function(d) { 
			console.log(d)
			return d; })
		.enter().append("rect")
			.attr("x", function(d) { 
			return x( d[0]); })
			.attr("y", function(d) { return y(d.data.State.concat(" - ").concat(d.data.County)); })
			.attr("width", function(d) { 
			return x(d[1] - d[0]); })
		.attr("height", y.bandwidth() )
	.on("mouseover", function(d) {      
    	d3.select(".tooltip").transition().duration(200).style("opacity", .9);      
			
			d3.select(".tooltip").html(Math.floor((d[1] - d[0])/1000) + "k")  
				.style("left", (d3.event.pageX) + "px")     
				.style("top", (d3.event.pageY - 28) + "px");
	})   

    // fade out tooltip on mouse out               
    .on("mouseout", function(d) {       
        d3.select(".tooltip").transition().duration(500).style("opacity", 0);      

    });
  
  var legend = svg.append("g")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
      .attr("text-anchor", "end")
    .selectAll("g")
    .data(keys.slice().reverse())
    .enter().append("g")
      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  legend.append("rect")
      .attr("x", barwidth - 5)
	  .attr("y", barheight - 100)
      .attr("width", 19)
      .attr("height", 19)
      .attr("fill", z);

  legend.append("text")
      .attr("x", barwidth - 10)
	  .attr("y", barheight - 90)
	  
      .attr("dy", "0.32em")
      .text(function(d) { return d; });

})

}