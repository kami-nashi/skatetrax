var DEFAULT_COLORS1 = ['#f08700', '#f49f0a', '#efca08', '#00a6a6', '#bbdef0'];
var DEFAULT_COLORS2 = ['#7fb7be', '#357266', '#dacc3e', '#bc2c1a', '#7d1538'];
var SKATETRAX_COLORS1 = ["#3d86e8", "#d816e0"];
var default_colors3 = ["#3e95cd","#8e5ea2","#3cba9f","#e8c3b9","#c45850","#4cc5b7"];
var ctx00 = document.getElementById("doughnut-chart00").getContext('2d');

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

getJSON(apiUrl_budget, function(err, data) {
  if (err !== null) {
    alert('Something went wrong: ' + err);
  } else {
    for (let i=0; i<data.length; ++i) {
      datas = data;

    }
  myPieChart = new Chart(ctx00, {
	type: 'doughnut',
	data: {
		datasets: [
      {
        backgroundColor: ["#3d86e8", "#d816e0"],
        data: [data[0], data[1]], //coach time vs ice time
        label: 'Practice & Coach Costs',
        labels: [ "Coaching Cost","Ice Time Cost"],
      },{
        backgroundColor: ["#70db70", "#009900"],
        data: [data[2], data[3]], //equipment vs maintenance
        label: 'Costs of equipment and maintaining it',
        labels: ["Equipment Cost","Maintenance Cost"],
      },{
        backgroundColor: ["#ff7c43","#ffa55b","#febd72","#ffa00e"],
        data: [data[4], data[5], data[6], data[7]], //comp vs Performance vs tests vs membership
        label: 'Costs of fees associated with events',
        labels: ["Competition Fees","Performance Fees", "Test Fees", "Membership Fees"],
      },{
        backgroundColor: ["#00e0ff", "#0080a6"],
        data: [data[8], data[9]], //class fees vs camp fees
        label: 'Costs of group learning',
        labels: ["Class Fees","Camp Fees"],
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
			text: 'Financial Totals'
		},
		animation: {
			animateScale: true,
			animateRotate: true
		},
		plugins: {
			doughnutlabel: {
				labels: [
					{
						text: 'Total:',
            font: {
            weight: 'bold',
          },
					},
          {
            text: '$' + data[10],
          },
				]
			}
		}
	},
});

}});
