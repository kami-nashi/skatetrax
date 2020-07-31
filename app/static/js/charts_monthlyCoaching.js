var DEFAULT_COLORS1 = ['#f08700', '#f49f0a', '#efca08', '#00a6a6', '#bbdef0'];
var DEFAULT_COLORS2 = ['#7fb7be', '#357266', '#dacc3e', '#bc2c1a', '#7d1538'];
var SKATETRAX_COLORS1 = ["#3d86e8", "#d816e0"];
var ctx = document.getElementById("doughnut-chart3").getContext('2d');

var iceTimes = [];
var coachTimes = [];

var getJSON = function(url, callback) {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);
  xhr.responseType = 'json';
  xhr.onload = function() {
    var status = xhr.status;
    if (status === 200) {
      callback(null, xhr.response);
    } else {
      callback(status, xhr.response);
    }
  };
  xhr.send();
};

getJSON(apiUrl_monthlyPie, function(err, data) {
  if (err !== null) {
    alert('Something went wrong: ' + err);
  } else {
      iceTimes.push(data[0]),
      coachTimes.push(data[1])
}});

new Chart(ctx, {
	type: 'doughnut',
	data: {
		datasets: [

      {
        backgroundColor: ["#3d86e8", "#d816e0"],
        data: [ 1,2],
        label: 'Training & Practice Costs',
        labels: ["Training Costs","Practice Costs"],
      },{
        backgroundColor: ["#3d86e8", "#d816e0"],
        data: [1,2],//[apiUrl_monthlyPie[2],apiUrl_monthlyPie[0]],
        label: 'Training & Practice Hours',
        labels: ["Training Hours","Practice Hours"],
      },
     ]

	},
	options: {
		responsive: true,
		legend: {
			display: false,
			position: 'top',
		},
		title: {
			display: false,
			fontSize: 20,
			text: 'Multiple lines of text'
		},
		animation: {
			animateScale: true,
			animateRotate: true
		},
		plugins: {
			doughnutlabel: {
				labels: [
					{
						text: 'Hours Practiced: ' + iceTimes,
					},
					{
						text: 'Hours Coached: ' + coachTimes,
						color: 'grey'
					},
					{
						text: 'Practice Costs: $' + 3,//apiUrl_monthlyPie[2],
						//color: 'red'
					},
					{
						text: 'Coach Costs: $' + 4,//apiUrl_monthlyPie[0],
						//color: 'green'
					}
				]
			}
		}
	},
  tooltips: {
callbacks: {
 label: function(tooltipItem, data) {
   var dataset = data.datasets[tooltipItem.datasetIndex];
   var index = tooltipItem.index;
   return dataset.labels[index] + ": " + dataset.data[index];
 }
}
}
});
