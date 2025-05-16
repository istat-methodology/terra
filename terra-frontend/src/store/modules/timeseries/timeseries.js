import { timeseriesService } from "@/services"
import { isArrayNull } from "@/common"
const state = {
  timeseriesChart: null,
  timeseriesCharts: null,
  statusMain: "",
  statusACF: "",
  statusNorm: ""
}
const mutations = {
  SET_TIMESERIES_CHART(state, timeseriesChart) {
    state.timeseriesChart = timeseriesChart
  },
  SET_TIMESERIES_CHARTS(state, timeseriesCharts) {
    state.timeseriesCharts = timeseriesCharts
  },
  SET_TIMESERIES_STATUS_MAIN(state, statusMain) {
    state.statusMain = statusMain
  },
  SET_TIMESERIES_STATUS_ACF(state, statusACF) {
    state.statusACF = statusACF
  },
  SET_TIMESERIES_STATUS_NORM(state, statusNorm) {
    state.statusNorm = statusNorm
  }
}
const actions = {
  findByFilters({ commit }, form) {
    return timeseriesService
      .findByFilters(form)
      .then((data) => {
        var statusMain =
          data["diagMain"] && isArrayNull(data["diagMain"]["series"]) == false
            ? data["statusMain"]
            : "00"
        commit("SET_TIMESERIES_STATUS_MAIN", statusMain)
        if (statusMain == "01") {
          commit("SET_TIMESERIES_CHARTS", data)
        } else {
          commit("SET_TIMESERIES_CHARTS", [])
        }
      })
      .catch((err) => {
        console.log(err)
      })
  },
  async findByFiltersMultiPartners({ commit }, form) {
    const partners = Array.isArray(form.partner) ? form.partner : [form.partner]

    const byPartner = {}
    let statusMain = "00"
    let commonDate = null

    for (const p of partners) {
      const singleForm = {
        ...form,
        partner: p
      }
      try {
        const data = await timeseriesService.findByFilters(singleForm)
        const hasSeries =
          data?.diagMain &&
          Array.isArray(data.diagMain.series) &&
          data.diagMain.series.length > 0
        if (hasSeries) {
          if (!commonDate && Array.isArray(data.diagMain.date)) {
            commonDate = data.diagMain.date
          }
          byPartner[p] = {
            series: data.diagMain.series
          }
          statusMain = "01" // partner return valid data
        }
      } catch (error) {
        console.error(`Error for partner ${p}:`, error)
      }
    }
    const result = {
      statusMain,
      diagMain: {
        date: commonDate || [],
        byPartner
      }
    }
    commit("SET_TIMESERIES_STATUS_MAIN", result.statusMain)
    if (statusMain === "01") {
      commit("SET_TIMESERIES_CHARTS", result)
    } else {
      commit("SET_TIMESERIES_CHARTS", [])
    }
    return result
  }
}
const getters = {
  statusMain: (state) => {
    return state.statusMain
  },
  timeseriesChart: (state) => {
    return state.timeseriesChart ? state.timeseriesChart : null
  },
  timeseriesCharts: (state) => {
    return state.timeseriesCharts ? state.timeseriesCharts : null
  }
}
export const timeseries = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
