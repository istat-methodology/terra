const makeColor = (color) => ({ border: color, background: color })

// Compact palette for charts that normally contain only a few series.
const timeSeriesPalette = [
  "#2e6fbb",
  "#e66101",
  "#159947",
  "#c43c82",
  "#00a6a6",
  "#d62728",
  "#7556a5",
  "#b07d00",
  "#8c564b",
  "#5f6b7a"
].map(makeColor)

// Extended palette for the complete product basket. Hues are interleaved so
// neighbouring products remain distinguishable.
const tradePalette = [
  "#2e6fbb",
  "#e66101",
  "#159947",
  "#c43c82",
  "#00a6a6",
  "#d62728",
  "#7556a5",
  "#b07d00",
  "#8c564b",
  "#4d7c0f",
  "#0072b2",
  "#e7298a",
  "#ca8a04",
  "#00876c",
  "#b33c2e",
  "#6b6ecf",
  "#a05a00",
  "#2f8f9d",
  "#9c3f96",
  "#507d2a",
  "#d1495b",
  "#386cb0",
  "#be7c4d",
  "#0081a7",
  "#a23b72",
  "#64748b",
  "#7f6000"
].map(makeColor)

export default {
  data: () => ({
    currentTimeSeriesColor: 0,
    timeSeriesPalette,
    tradePalette
  }),
  methods: {
    getTimeSeriesColor() {
      const color =
        this.timeSeriesPalette[
          this.currentTimeSeriesColor % this.timeSeriesPalette.length
        ]
      this.currentTimeSeriesColor++
      return color
    },
    getTradeColor(productIndex) {
      const index = Number.isInteger(productIndex) ? productIndex : 0
      return this.tradePalette[index % this.tradePalette.length]
    },
    clearTimeSeriesColors() {
      this.currentTimeSeriesColor = 0
    }
  }
}
