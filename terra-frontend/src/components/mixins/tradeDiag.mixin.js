export default {
  methods: {
    getOptions(isLegend, locale) {
      return {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          display: isLegend
        },
        tooltips: {
          //mode: "index",
          intersect: true,
          callbacks: {
            label: function (tooltipItem, data) {
              var label = data.datasets[tooltipItem.datasetIndex].label || ""
              if (label) {
                label += ": "
              }
              label += tooltipItem.yLabel.toLocaleString(locale)
              return label
            }
          }
        },
        hover: {
          mode: "nearest",
          intersect: true
        },
        scales: {
          xAxes: [
            {
              display: true,
              scaleLabel: {
                display: true,
                labelString: ""
              }
            }
          ],
          yAxes: [
            {
              display: true,
              scaleLabel: {
                display: true,
                labelString: ""
              }
            }
          ]
        }
      }
    }
  }
}
