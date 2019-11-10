
allspeciesURL = "https://cjmod5.herokuapp.com/get_species";

d3.json(allspeciesURL).then(function( counties){
	var countyOptions = document.getElementById('species');
	for (var i = 0 ; i<counties.length; i++) {
		countyOptions.options[i] = new Option(counties[i], counties[i]);
	}
	updateChart()

});

allboroughURL =  "https://cjmod5.herokuapp.com/get_boroughs";
d3.json(allboroughURL).then(function(boroughs){

	var boroughOption = document.getElementById('borough');

	for (var i = 0 ; i<boroughs.length; i++) {
		boroughOption.options[i] = new Option(boroughs[i], boroughs[i]);
	}
	updateChart()

});
// call to update the barchart 

function updateChart(){
	var boroughSelected = document.getElementById('borough').value;
	var speciesSelected = document.getElementById('species').value;
	var treedataURL = "https://cjmod5.herokuapp.com/fetch_tree_data?borough=" + boroughSelected + "&species=" + speciesSelected;
	
	d3.json(treedataURL).then(function(data){
		// d3 barchart

		var margin = { left:100, right:20, top:20, bottom:20 };

		var width = 300 - margin.left - margin.right,
		    height = 400 - margin.top - margin.bottom;
		d3.select("svg").remove();
    
		var g = d3.select("#barChart")
		    .append("svg")
		    .attr("width", width + margin.left + margin.right)
		    .attr("height", height + margin.top + margin.bottom)
		    .append("g")
		    .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");

    	// Y Label
		g.append("text")
    		.attr("y", -30)
    		.attr("x", -(height / 2))
    		.attr("font-size", "10px")
    		.attr("text-anchor", "middle")
    		.attr("transform", "rotate(-90)")
    		.text("health Ratio %");
   		data.forEach(function(d){
    		d.health_ratio = +d.health_ratio;
    	})
    	console.log(data)
    	var rectdata = g.selectAll("rect").data(data);
	    // X Scale
	    var x = d3.scaleBand()
	        .domain(["Good", "Fair" , "Poor"])
	        .range([0, width])


	    // Y Scale
	    var y = d3.scaleLinear()
	        .domain([0, 100])
	        .range([height, 0]);
    	// X Axis
	    var xAxisCall = d3.axisBottom(x);
	    g.append("g")
	        .attr("class", "x axis")
	        .attr("transform", "translate(0," + height +")")
	        .call(xAxisCall);

	    // Y Axis
	    var yAxisCall = d3.axisLeft(y)
	        .tickFormat(function(d){ return d; });
	    g.append("g")
	        .attr("class", "y axis")
	        .call(yAxisCall);

	    rectdata.enter()
        	.append("rect")
            .attr("y", function(d){ return y(d.health_ratio); })
            .attr("x", function(d){ return x(d.health) })
			.attr("height", function(d){ return height - y(d.health_ratio); })
            .attr("width", x.bandwidth)
            .attr("fill", function(d) {
    			 	color = "grey"
    			 	if (d.health == "Poor")
    			 		color = "red"
    			 	else if(d.health== "Fair")
    			 		color = "orange"
    			 	else if (d.health == "Good")
    			 		color ="green"

    			 	return color
    			 });  
	})
}