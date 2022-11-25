export const optionsTrade = {
  responsive: true,
  maintainAspectRatio: false,
  title: {
    display: false,
    text: ""
  },
  legend: {
    display: true
  },
  tooltips: {
    //mode: "index",
    intersect: true
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
