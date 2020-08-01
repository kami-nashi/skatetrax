var DEFAULT_COLORS1 = ['#f08700', '#f49f0a', '#efca08', '#00a6a6', '#bbdef0'];
var DEFAULT_COLORS2 = ['#7fb7be', '#357266', '#dacc3e', '#bc2c1a', '#7d1538'];
var SKATETRAX_COLORS1 = ["#3d86e8", "#d816e0"];
var ctx1 = document.getElementById("doughnut-chart2").getContext('2d');

var myPieChart;
var chartLabels = [];
var mIceTimes;
var mCoachTimes;
var yIceTimes;
var yCoachTimes;
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

getJSON(apiUrl_monthlyCost, function(err, data) {
  if (err !== null) {
    alert('Something went wrong: ' + err);
  } else {
    for (let i=0; i<data.length; ++i) {
      mIceTimes = data[0];
      mCoachTimes = data[1];
      yIceTimes = data[2];
      yCoachTimes = data[3];
      datas = [mIceTimes, mCoachTimes,yIceTimes,yCoachTimes];

    }
  myPieChart = new Chart(ctx1, {
	type: 'doughnut',
	data: {
		datasets: [
      {
        backgroundColor: ["#d816e0", "#3d86e8"],
        data: [datas[3],datas[2]],
        label: 'Yearly Overview',
        labels: [ "Yearly Practice Cost","Yearly Coaching Cost"],
      },{
        backgroundColor: ["#d816e0", "#3d86e8"],
        data: [datas[1],datas[0]],
        label: 'Monthly Overview',
        labels: ["Monthly Practice Cost","Monthly Coaching Cost"],
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
			text: 'Cost Overview'
		},
		animation: {
			animateScale: true,
			animateRotate: true
		},
		plugins: {
			doughnutlabel: {
				labels: [
					{
						text: 'Monthly:',
            font: {
            weight: 'bold',
          },
					},
          {
            text: datas[0] + ' / ' + datas[1],
          },
					{
						text: 'Yearly:',
            font: {
            weight: 'bold',
          },
					},
          {
            text: datas[2] + ' / ' + datas[3],
          }
				]
			}
		}
	},
});

}});
