import { metadataService } from "@/services"
import { getPeriod, getTrimesterPeriod } from "@/common"
const state = {
  metadata: null
}
const mutations = {
  SET_METADATA(state, metadata) {
    state.metadata = metadata
  }
}
const actions = {
  getMetadata({ commit }) {
    return metadataService
      .getMetadata()
      .then((data) => {
        commit("SET_METADATA", data)
      })
      .catch((err) => {
        console.log(err)
      })
  }
}
const getters = {
  mapPeriod: (state, getters, rootState, rootGetters) => {
    const lan = rootGetters["coreui/language"]
    return state.metadata
      ? getPeriod(state.metadata.map.timeStart, state.metadata.map.timeEnd, lan)
      : null
  },
  graphPeriod: (state, getters, rootState, rootGetters) => {
    const lan = rootGetters["coreui/language"]
    return state.metadata
      ? getPeriod(
          state.metadata.graph.timeStart,
          state.metadata.graph.timeEnd,
          lan
        )
      : null
  },

  graphTrimesterPeriod: (state, getters, rootState, rootGetters) => {
    const lan = rootGetters["coreui/language"]
    return state.metadata
      ? getTrimesterPeriod(
          state.metadata.graph.timeStart,
          state.metadata.graph.timeEnd,
          lan
        )
      : null
  },
  graphExtraPeriod: (state, getters, rootState, rootGetters) => {
    const lan = rootGetters["coreui/language"]
    return state.metadata
      ? getPeriod(
          state.metadata.graphPlus.timeStart,
          state.metadata.graphPlus.timeEnd,
          lan
        )
      : null
  },
  graphExtraTrimesterPeriod: (state, getters, rootState, rootGetters) => {
    const lan = rootGetters["coreui/language"]
    return state.metadata
      ? getTrimesterPeriod(
          state.metadata.graphPlus.timeStart,
          state.metadata.graphPlus.timeEnd,
          lan
        )
      : null
  },
  tradePeriod: (state, getters, rootState, rootGetters) => {
    const lan = rootGetters["coreui/language"]
    return state.metadata
      ? getPeriod(
          state.metadata.trade.timeStart,
          state.metadata.trade.timeEnd,
          lan
        )
      : null
  },
  processingDay: (state) => {
    return state.metadata ? state.metadata.processingDay : ""
  },
  lastLoadedData: (state) => {
    return state.metadata
      ? state.metadata.lastLoadedData.replace(", ", "-")
      : ""
  },
  appVersion: (state) => {
    return state.metadata ? state.metadata.appVersion : ""
  },
  mapSeries: (state) => {
    return state.metadata ? state.metadata.map.timeSelected : ""
  },
  graphSeries: (state) => {
    return state.metadata ? state.metadata.graph.timeSelected : ""
  },
  tradeSeries: (state) => {
    return state.metadata ? state.metadata.trade.timeSelected : ""
  }
}
export const metadata = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
