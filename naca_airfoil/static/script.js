var plotData;
var plot;

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
    $('chartdiv').empty();
    console.log(data);
    if(plot) plot.destroy();
    plot = $.jqplot('chartdiv', [data], {
	
	seriesDefaults: {
	    // make this a donut chart.
	    rendererOptions:{
		showDataLabels: true,
		dataLabels: 'value',
		totalLabel: true,
	    }
	},
	axes:{
	    xaxis:{
		label:'Angles',
		labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
		min:0.0,
		max:100.0
	    },
	    yaxis:{
		label:'drag/lift',
		labelRenderer: $.jqplot.CanvasAxisLabelRenderer
	    }
	}
    });
    
}
