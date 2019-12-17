function updateLineChart() {

  var statecounty = document.getElementById('state-county').value;
  console.log(statecounty)
  d3.select("#linechart").selectAll("*").remove();
  d3.select("#tooltip1").selectAll("*").remove();
  var url = 'http://app215371.herokuapp.com/monthlydata?state=' + statecounty.split('-')[0] + '&county=' + statecounty.split('-')[1]
	console.log(url)
    var glines
      var mouseG
      var tooltip

      var parseDate = d3.timeParse("%Y-%m")
      var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]

      var margin = {top: 80, right: 200, bottom: 40, left: 80}
      var width = 2200 - margin.left - margin.right
      var height = 500 - margin.top - margin.bottom

      var lineOpacity = 1
      var lineStroke = "2px"

      var axisPad = 6 // axis formatting
      var R = 6 //legend marker

      var category =[ 'NO2-AQI' ,'SO2-AQI' ,'CO-AQI', 'O3-AQI' ];

      // since Category B and E are really close to each other, assign them diverging colors
      var color = d3.scaleOrdinal()
        .domain(category)
        .range([ "#dfc27d", "#80cdc1", "#018571", "#a6611a"])
      d3.json(url, data => {
	    res = []
        data.map((d,i) => {

		for (key = 0 ;key < 4 ; key++) {
			arr = {
				date : parseDate(d.month),
				'polutant': category[key],
				'State' : d.State,
				'County' : d.County,
				'reading': +d[category[key]]
			}
			res.push(arr)
		}
        })

        var xScale = d3.scaleTime()
          .domain(d3.extent(res, d=>d.date))
          .range([0, width])

        function roundToNearest10K(x) {
          return Math.round(x / 1000) * 1000        }

        var yScale = d3.scaleLinear()
          .domain([0, roundToNearest10K(d3.max(res, d => d['reading']))])
          .range([height, 0]);

        var svg = d3.select("#linechart")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append('g')
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        // x label 
        svg.append("text")
        .attr("class", "x axis-label")
        .attr("x", width / 2)
        .attr("y", height + 40)
        .attr("font-size", "15px")
        .attr("font-weight", "bold")
        .attr("text-anchor", "middle")
        .text("Trends of pollutants ( 2000 - 2019) ");

        // CREATE AXES // 
        // render axis first before lines so that lines will overlay the horizontal ticks
        var xAxis = d3.axisBottom(xScale).ticks(d3.timeYear.every(1)).tickSizeOuter(axisPad*2).tickSizeInner(axisPad*2)
        var yAxis = d3.axisLeft(yScale).ticks(10, "s").tickSize(-width) //horizontal ticks across svg width

        svg.append("g")
          .attr("class", "x axis")
          .attr("transform", `translate(0, ${height})`)
          .call(xAxis)
          .call(g => {
            var years = xScale.ticks(d3.timeYear.every(1))
            var xshift = (width/(years.length))/2 
            g.selectAll("text").attr("transform", `translate(${xshift}, 0)`) //shift tick labels to middle of interval
              .style("text-anchor", "middle")
              .attr("y", axisPad)
              .attr('fill', '#A9A9A9')

            g.selectAll("line")
              .attr('stroke', '#A9A9A9')
  
            g.select(".domain")
              .attr('stroke', '#A9A9A9')

          })

        svg.append("g")
          .attr("class", "y axis")
          .call(yAxis)
          .call(g => {
            g.selectAll("text")
            .style("text-anchor", "middle")
            .attr("x", -axisPad*2)
            .attr('fill', '#A9A9A9')

            g.selectAll("line")
              .attr('stroke', '#A9A9A9')
              .attr('stroke-width', 0.7) // make horizontal tick thinner and lighter so that line paths can stand out
              .attr('opacity', 0.3)

            g.select(".domain").remove()

           })
          .append('text')
            .attr('x', 50)
            .attr("y", -10)
            .attr("fill", "#A9A9A9")
            .text("AQI :  > 200 ")


        // CREATE LEGEND // 
        var svgLegend = svg.append('g')
            .attr('class', 'gLegend')
            .attr("transform", "translate(" + (width + 20) + "," + 0 + ")")

        var legend = svgLegend.selectAll('.legend')
          .data(category)
          .enter().append('g')
            .attr("class", "legend")
            .attr("transform", function (d, i) {return "translate(0," + i * 20 + ")"})

        legend.append("circle")
            .attr("class", "legend-node")
            .attr("cx", 0)
            .attr("cy", 0)
            .attr("r", R)
            .style("fill", d=>color(d))

        legend.append("text")
            .attr("class", "legend-text")
            .attr("x", R*2)
            .attr("y", R/2)
            .style("fill", "#A9A9A9")
            .style("font-size", 12)
            .text(d=>d)

        // line generator 
        var line = d3.line()
          .x(d => xScale(d.date))
          .y(d => yScale(d['reading']))

        renderChart() // inital chart render (set default to Bidding Exercise 1 data)

        updateChart()


        function updateChart() {

          var res_nested = d3.nest()
            .key(d=>d.polutant)
            .entries(res)

          glines.select('.line') //select line path within line-group (which represents a vehicle category), then bind new data 
            .data(res_nested)
            .transition().duration(750)
            .attr('d', function(d) {
              return line(d.values)
            })

          mouseG.selectAll('.mouse-per-line')
            .data(res_nested)

          mouseG.on('mousemove', function () { 
              var mouse = d3.mouse(this)
              updateTooltipContent(mouse, res_nested)
            })
        }

        function renderChart() {


          var res_nested = d3.nest() // necessary to nest data so that keys represent each vehicle category
            .key(d=>d.polutant)
            .entries(res)

          // APPEND MULTIPLE LINES //
          var lines = svg.append('g')
            .attr('class', 'lines')

          glines = lines.selectAll('.line-group')
            .data(res_nested).enter()
            .append('g')
            .attr('class', 'line-group')

          glines  
            .append('path')
              .attr('class', 'line')  
              .attr('d', d => line(d.values))
              .style('stroke', (d, i) => color(i))
              .style('fill', 'none')
              .style('opacity', lineOpacity)
              .style('stroke-width', lineStroke)


          // APPEND CIRCLE MARKERS //
          //var gcircle = lines.selectAll("circle-group")
            //.data(res_nested).enter()
            //.append("g")
            //.attr('class', 'circle-group')

          //gcircle.selectAll("circle")
            //.data(d => d.values).enter()
            //.append("g")
            //.attr("class", "circle")  
            //.append("circle")
            //.attr("cx", d => xScale(d.date))
            //.attr("cy", d => yScale(d.reading))
            //.attr("r", 2)

          // CREATE HOVER TOOLTIP WITH VERTICAL LINE //
          tooltip = d3.select("#tooltip1").append("div")
            .attr('id', 'tooltip')
            .style('position', 'absolute')
            .style("background-color", "#D3D3D3")
            .style('padding', 6)
            .style('display', 'none')

          mouseG = svg.append("g")
            .attr("class", "mouse-over-effects");

          mouseG.append("path") // create vertical line to follow mouse
            .attr("class", "mouse-line")
            .style("stroke", "#A9A9A9")
            .style("stroke-width", lineStroke)
            .style("opacity", "0");

          var lines = document.getElementsByClassName('line');

          var mousePerLine = mouseG.selectAll('.mouse-per-line')
            .data(res_nested)
            .enter()
            .append("g")
            .attr("class", "mouse-per-line");

          mousePerLine.append("circle")
            .attr("r", 4)
            .style("stroke", function (d) {
              return color(d.key)
            })
            .style("fill", "none")
            .style("stroke-width", lineStroke)
            .style("opacity", "0");

          mouseG.append('svg:rect') // append a rect to catch mouse movements on canvas
            .attr('width', width) 
            .attr('height', height)
            .attr('fill', 'none')
            .attr('pointer-events', 'all')
            .on('mouseout', function () { // on mouse out hide line, circles and text
              d3.select(".mouse-line")
                .style("opacity", "0");
              d3.selectAll(".mouse-per-line circle")
                .style("opacity", "0");
              d3.selectAll(".mouse-per-line text")
                .style("opacity", "0");
              d3.selectAll("#tooltip")
                .style('display', 'none')

            })
            .on('mouseover', function () { // on mouse in show line, circles and text
              d3.select(".mouse-line")
                .style("opacity", "1");
              d3.selectAll(".mouse-per-line circle")
                .style("opacity", "1");
              d3.selectAll("#tooltip")
                .style('display', 'block')
            })
            .on('mousemove', function () { // update tooltip content, line, circles and text when mouse moves
              var mouse = d3.mouse(this)

              d3.selectAll(".mouse-per-line")
                .attr("transform", function (d, i) {
                  var xDate = xScale.invert(mouse[0]) // use 'invert' to get date corresponding to distance from mouse position relative to svg
                  var bisect = d3.bisector(function (d) { return d.date; }).left // retrieve row index of date on parsed csv
                  var idx = bisect(d.values, xDate);

                  d3.select(".mouse-line")
                    .attr("d", function () {
                      var data = "M" + xScale(d.values[idx].date) + "," + (height);
                      data += " " + xScale(d.values[idx].date) + "," + 0;
                      return data;
                    });
                  return "translate(" + xScale(d.values[idx].date) + "," + yScale(d.values[idx].reading) + ")";

                });

              updateTooltipContent(mouse, res_nested)

            })

          }

      function updateTooltipContent(mouse, res_nested) {

        sortingObj = []
        res_nested.map(d => {
          var xDate = xScale.invert(mouse[0])
          var bisect = d3.bisector(function (d) { return d.date; }).left
          var idx = bisect(d.values, xDate)
          sortingObj.push({key: d.values[idx].polutant, reading: d.values[idx].reading, State: d.values[idx].State, County: d.values[idx].County, year: d.values[idx].date.getFullYear(), month: monthNames[d.values[idx].date.getMonth()]})
        })

        sortingObj.sort(function(x, y){
           return d3.descending(x.reading, y.reading);
        })

        var sortingArr = sortingObj.map(d=> d.key)

        var res_nested1 = res_nested.slice().sort(function(a, b){
          return sortingArr.indexOf(a.key) - sortingArr.indexOf(b.key) // rank vehicle category based on price of reading
        })
        tooltip.html(sortingObj[0].month + "-" + sortingObj[0].year + " (State:" + sortingObj[0].State + ', County: ' +  sortingObj[0].County +  ')')
          .style('display', 'block')
          .style('left', (d3.event.pageX + 20) + 'px')
          .style('top', (d3.event.pageY - 20) + 'px')
          .style('font-size', '14px')
          .selectAll()
          .data(res_nested1).enter() // for each vehicle category, list out name and price of reading
          .append('div')
          .style('font-size', 10)
          .html(d => {
            var xDate = xScale.invert(mouse[0])
            var bisect = d3.bisector(function (d) { return d.date; }).left
            var idx = bisect(d.values, xDate)
            return d.key.substring(0, 3) + " " + d.key.slice(-1) + ": " + d.values[idx].reading.toString()
          })
      }

    })
}