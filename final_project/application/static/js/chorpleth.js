function updatemap(year, baseUrl){

url = baseUrl.concat(year)

//Width and height of map
var width = 900;
var height = 600;


var projection = d3.geoAlbersUsa()
				   .scale([800])        // scale things down so see entire US
				   .translate([width/2, height/2])    // translate to center of screen

var path = d3.geoPath()
      .projection(projection);
		
//var legendText = ["Cities Lived", "States Lived", "States Visited", "Nada"];
var legendText = [ "0-50(Good) ", "51-100(Moderate)", "101-150(Unhealthy for sensitive group) ", "151-200(Unhealthy)", "201-300(Very Unhealthy)", "301-500(Hazardous)", "Not Available"]                            

//Create SVG element and append map to the SVG
var svg = d3.select("#statesvg")
        
// Append Div for tooltip to SVG

			
var color = d3.scaleThreshold()
				.domain([ 0, 50, 100 , 150, 200, 300, 500])
				.range(["grey", "green", "yellow" , "orange" , "red" , "purple", "brown"]);

				
  var ext_color_domain = [ 0 , 50, 100 , 150, 200, 300, -1]
  var legend_labels = ["0-50(Good) ", "51-100(Moderate)", "101-150(Unhealthy for sensitive group) ", "151-200(Unhealthy)", "201-300(Very Unhealthy)", "301-500(Hazardous)", "Data Not Available"]              

				
				
// Load in my states data!
d3.json(url, function(data) {
// Load GeoJSON data and merge with states data
d3.json("static/js/us-states.json", function(json) {
d3.select("#statesvg").selectAll("*").remove();


svg.append("text")
    .attr("class", "x axis-label")
    .attr("x", width / 2)
    .attr("y", height - 20)
    .attr("font-size", "15px")
    .attr("font-weight", "bold")
    .attr("text-anchor", "middle")
    .text("Air Quality Index Intensity 2000 - 2019 ");

// Bind the data to the SVG and create one path per GeoJSON feature
svg.selectAll("path")
	.data(json.features)
	.enter()
	.append("path")
	.attr("d", path)
	.style("stroke", "#fff")
	.style("stroke-width", "1")
	.style("fill", function(d){ 
				if(data[d.properties.name]) {
					return color(data[d.properties.name].AQI);
				}
				else 
					return "grey"})
	.on("mouseover", function(d) {      
    	d3.select(".tooltip").transition().duration(200).style("opacity", .9);      
			
			d3.select(".tooltip").html(tooltipHtml(d.properties.name, data[d.properties.name]))  
				.style("left", (d3.event.pageX) + "px")     
				.style("top", (d3.event.pageY - 28) + "px");
	})   

    // fade out tooltip on mouse out               
    .on("mouseout", function(d) {       
        d3.select(".tooltip").transition().duration(500).style("opacity", 0);      

    });

	svg.append("text").text(year)
			.attr("x", 500)
			.attr("y", 100)
			.style("font-size", "30px")
			.style('fill', 'lightblue')
		
		 
     
// Modified Legend Code from Mike Bostock: http://bl.ocks.org/mbostock/3888852
	var legend = svg.selectAll("g.legend")
					.data(ext_color_domain)
					.enter().append("g")
  
	var ls_w = 20, ls_h = 20;
	

	legend.append("rect")
			.attr("x", width - 180)
			.attr("y", function(d, i){ return  (height - 50) -(i*ls_h) - 2*ls_h;})
			.attr("width", ls_w)
			.attr("height", ls_h)
			.style("fill", function(d, i) { return color(d); })
			.style("opacity", 0.8);
	legend.append("text")
			.attr("x", width - 150 )
			.attr("y", function(d, i){ return (height - 50)- (i*ls_h) - ls_h - 4;})
			.attr("font-size", "12px")
			.text(function(d, i){ return legend_labels[i]; });
	});


});
}

function tooltipHtml(n, d){	/* function to create html content string in tooltip div. */
		return "<h4>"+n+"</h4><table>"+
			"<tr><td>AQI</td><td>"+(d.AQI)+"</td></tr>"+
			"<tr><td>CO AQI</td><td>"+(d['CO AQI'])+"</td></tr>"+
			"<tr><td>O3 AQI</td><td>"+(d['O3 AQI'])+"</td></tr>"+
			"<tr><td>NO2 AQI</td><td>"+(d['NO2 AQI'])+"</td></tr>"+
			"<tr><td>SO2 AQI</td><td>"+(d['SO2 AQI'])+"</td></tr>"+
			"</table>";
	}

	
	
function tooltipHtml1(n, d){	/* function to create html content string in tooltip div. */
		return "<h4>"+n+"</h4><table>"+
			"<tr><td>AQI</td><td>"+(d.AQI)+"</td></tr>"+
			"<tr><td>CO AQI</td><td>"+(d['CO AQI'])+"</td></tr>"+
			"<tr><td>O3 AQI</td><td>"+(d['O3 AQI'])+"</td></tr>"+
			"<tr><td>NO2 AQI</td><td>"+(d['NO2 AQI'])+"</td></tr>"+
			"<tr><td>SO2 AQI</td><td>"+(d['SO2 AQI'])+"</td></tr>"+
			"</table>";
	}
