export default {
  data: () => ({
    optionsNorm: {
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        display: false
      },
      title: {
        display: true,
        text: "",
        fontColor: "#404040",
        fontSize: 16,
        fontWeight: "bold",
        verticalAlign: "top",
        horizontalAlign: "center",
        padding: 0,
        fontFamily: "'Helvetica Neue',Helvetica,Arial,sans-serif"
      },
      scales: {
        xAxes: [
          {
            scaleLabel: {
              display: true,
              fontSize: 16,
              fontWeight: "bold",
              fontFamily: "'Helvetica Neue',Helvetica,Arial,sans-serif",
              labelString: "THEORETICAL QUANTILES"
            },
            ticks: {
              stepSize: 1
            }
          }
        ],
        yAxes: [
          {
            scaleLabel: {
              display: true,
              fontSize: 16,
              fontWeight: "bold",
              fontFamily: "'Helvetica Neue',Helvetica,Arial,sans-serif",
              labelString: "SAMPLE QUANTILIES"
            },
            ticks: {
              stepSize: 1
            }
          }
        ]
      }
    },
    optionsACF: {
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        display: false
      },
      title: {
        display: true,
        text: "",
        fontColor: "#404040",
        fontSize: 16,
        fontWeight: "bold",
        verticalAlign: "top",
        horizontalAlign: "center",
        padding: 0,
        fontFamily: "'Helvetica Neue',Helvetica,Arial,sans-serif"
      },
      scales: {
        xAxes: [
          {
            scaleLabel: {
              display: true,
              fontSize: 16,
              fontWeight: "bold",
              fontFamily: "'Helvetica Neue',Helvetica,Arial,sans-serif",
              labelString: "Lag"
            },
            ticks: {
              stepSize: 0.1
            }
          }
        ],
        yAxes: [
          {
            scaleLabel: {
              display: true,
              fontSize: 16,
              fontWeight: "bold",
              fontFamily: "'Helvetica Neue',Helvetica,Arial,sans-serif",
              labelString: "ACF"
            },
            ticks: {
              stepSize: 0.1
            }
          }
        ]
      }
    }
  }),
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
          yAxes: [
            {
              display: true,
              gridLines: {
                display: true
              },
              scaleLabel: {
                display: true,
                labelString: ""
              },
              ticks: {
                // For a category axis, the val is the index so the lookup via getLabelForValue is needed
                callback: function (val) {
                  return val.toLocaleString(locale)
                }
              }
            }
          ],
          xAxes: [
            {
              display: true,
              gridLines: {
                display: true
              },
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
