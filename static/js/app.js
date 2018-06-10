var url = "/names";
var select = document.getElementById('selDataset')

//code to populate the drop down with list of sample 
Plotly.d3.json(url, function (error, response) {
    var data = response;
    for (var i=0; i< data.length; i++){
        var option = document.createElement('option');
        option.innerHTML = data[i];
        select.appendChild(option);
    }
    optionChanged(data[0])
});


//code to create pie chart, meta data sample key/value pairs and bubble chart. 
function optionChanged(sample) {
    var url1 = "/otu" ;
    var url2 = `/metadata/${sample}`;
    var url3 = `/wfreq/${sample}`;
    var url4 = `/samples/${sample}`;

    Plotly.d3.json(url2, function (error, response) {
        var value = ""
        for (i in response) {
            value += "<p>" + i + ":" + response[i] + "</p>";
        }
        document.getElementById("sample_metadata").innerHTML = value;
    });
    Plotly.d3.json(url1, function(error, data){
        var otu_values = data;
        Plotly.d3.json(url4, function(error, data){
            var otu_id = data[0].otu_ids.slice(0, 10);
            var sample_values = data[0].sample_values.slice(0,10);
            var otu_desc = []
            for (i in sample_values){
                j = sample_values[i]
                otu_desc.push(otu_values[j-1])
            }
            pie_data = [{
                "labels": otu_id,
                "values": sample_values,
                "type": "pie",
                "hovertext":otu_desc
                }];
            var layout = {
                title: "Belly Button Sample Size Pie Chart",
                height: 600,
                width: 680,
                margin: { t: 30, b:100 },
                showlegend:true}
            var PIE = document.getElementById('pie');
            Plotly.newPlot(PIE, pie_data, layout);
            bubble_data =[{
                x: data[0].otu_ids,
                y: data[0].sample_values,
                mode: 'markers',
                marker: {
                    size: data[0].sample_values,
                    color: data[0].otu_ids
                }
                }];
            var bubble_layout = {
                title: 'Belly Button Bubble Chart -- OTU vs Sample Size',
                showlegend: true,
                height: 600
                };
            var BUBBLE = document.getElementById('bubble');
            Plotly.newPlot(BUBBLE, bubble_data, bubble_layout);
        });
    })

};
