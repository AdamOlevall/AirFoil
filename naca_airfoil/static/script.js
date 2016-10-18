var plotData;

$(document).ready(function(){
    
    $("#idForm").submit(function(e) {

	var url = ""; // route to our web service (http://{ip}:5000/naca/service)

	$.ajax({
            type: "POST",
            url: url,
            data: $("#idForm").serialize(), // serializes the form's elements.
            success: function(data)
            {
		plotData = [];
		var jsonData = JSON.parse(data);
		$.each(jsonData, function(key, value) {
		    //alert("key: " + key + " value: " + value);
		    plotData.push([key, parseInt(value)]);
		});
		plotGraph(plotData);
	    }
	});
		    	    
	e.preventDefault(); // avoid to execute the actual submit of the form.
    });
});

function plotGraph(data){
    console.log(data);
    $.jqplot('chartdiv', [data], {
	seriesDefaults: {
	    // make this a donut chart.
	    rendererOptions:{
		sliceMargin: 4,
		startAngle: 0,
		showDataLabels: true,
		dataLabels: 'value',
		totalLabel: true,
	    }
	},
	axes:{
	    xaxis:{
		label:'Angles',
		labelRenderer: $.jqplot.CanvasAxisLabelRenderer
	    },
	    yaxis:{
		label:'drag/lift',
		labelRenderer: $.jqplot.CanvasAxisLabelRenderer
	    }
	}
    });
    
}
