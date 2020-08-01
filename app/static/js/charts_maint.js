var SKATETRAX_COLORS1 = ["#009900","#70db70"];
var ctx10 = document.getElementById("doughnut-chart10").getContext('2d');

var hRemaining;
var hCurrent;
var hPrefs;

var myPieChart;
var chartLabels = [];
var datas = [];

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

getJSON(apiUrl_maintClock, function(err, data) {
  if (err !== null) {
    alert('Something went wrong: ' + err);
  } else {
    for (let i=0; i<data.length; ++i) {
      hRemaining = data[0];
      hCurrent = data[1];
      hPrefs = data[2];
      datas = [hRemaining,hCurrent,hPrefs];
    }
  myPieChart = new Chart(ctx10, {
	type: 'doughnut',
	data: {
		datasets: [
      {
        backgroundColor: SKATETRAX_COLORS1,
        data: [datas[0],datas[1]],
        label: 'Maintenance',
        labels: [ "Currently Hours","Remaining Hours"],
      },
     ]
	},
	options: {
		responsive: true,
		legend: {
			display: false,
			position: 'top',
		},
    tooltips: {
  callbacks: {
   label: function(tooltipItem, data) {
     var dataset = data.datasets[tooltipItem.datasetIndex];
     var index = tooltipItem.index;
     return dataset.labels[index] + ": " + dataset.data[index];
   }
  }
},
		title: {
			display: true,
			fontSize: 20,
			text: 'Maintenance Overview'
		},
		animation: {
			animateScale: true,
			animateRotate: true
		},
		plugins: {
			doughnutlabel: {
				labels: [
					{
						text: 'Hours On:',
            font: {
            weight: 'bold',
          },
					},
          {
            text: datas[0],
          },
					{
						text: 'Hours Remaining:',
            font: {
            weight: 'bold',
          },
					},
          {
            text: datas[1],
          }
				]
			}
		}
	},
});

}});
