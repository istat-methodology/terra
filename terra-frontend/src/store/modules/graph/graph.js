import { graphService } from "@/services"
import {
  getUInodes,
  buildMetrics,
  GRAY_PALETTE,
  MAX_EDGES_FOR_DETAIL,
  DENSE_EDGE_STYLE,
  getWeightClassQuantile,
  getEdgeWidthQuantile,
  getEdgeTooltip
} from "@/common"

const state = {
  nodes: [],
  edges: [],
  metrics: null,
  metricsTable: null
}
const mutations = {
  SET_NODES(state, nodes) {
    state.nodes = nodes
  },
  SET_EDGES(state, edges) {
    state.edges = edges
  },
  SET_METRICS(state, metrics) {
    state.metrics = metrics
  },
  SET_METRICS_TABLE(state, metricsTable) {
    state.metricsTable = metricsTable
  }
}
const actions = {
  clear({ commit }) {
    commit("SET_NODES", [])
    commit("SET_EDGES", [])
    commit("SET_METRICS", null)
    commit("SET_METRICS_TABLE", null)
  },
  postGraphExtra({ dispatch }, form) {
    return graphService
      .postGraphExtra(form)
      .then((data) => {
        return dispatch("store", data)
      })
      .catch((err) => {
        console.log(err)
      })
  },
  postGraphIntra({ dispatch }, form) {
    return graphService
      .postGraphIntra(form)
      .then((data) => {
        return dispatch("store", data)
      })
      .catch((err) => {
        console.log(err)
      })
  },
  store({ commit, rootGetters }, data) {
    if (data["STATUS"] == undefined) {
      commit(
        "SET_NODES",
        getUInodes(data.nodes, rootGetters["classification/partners"])
      )
      commit("SET_EDGES", data.edges)
      commit("SET_METRICS", data.metriche)
      commit(
        "SET_METRICS_TABLE",
        buildMetrics(data, rootGetters["classification/partners"])
      )
    }
    return data["STATUS"] == undefined ? "00" : data["STATUS"]
  }
}
const getters = {
  nodes: (state) => {
    return state.nodes ? state.nodes : []
  },
  edges: (state) => {
    if (!state.edges || state.edges.length === 0) return []

    // 🕸️ GRAFO TROPPO DENSO → stile unico
    if (state.edges.length > MAX_EDGES_FOR_DETAIL) {
      return state.edges.map((e) => ({
        ...e,
        color: {
          color: DENSE_EDGE_STYLE.color
        },
        width: DENSE_EDGE_STYLE.width
      }))
    }

    // 🔍 GRAFO LEGGIBILE → quantili
    const sortedWeights = [...state.edges]
      .map((e) => e.weight)
      .sort((a, b) => a - b)

    return state.edges.map((e) => {
      const cls = getWeightClassQuantile(e.weight, sortedWeights)

      return {
        ...e,
        color: {
          color: GRAY_PALETTE[cls]
        },
        width: getEdgeWidthQuantile(cls),
        title: getEdgeTooltip(e, cls)
      }
    })
  },
  metrics: (state) => {
    return state.metrics ? state.metrics : null
  },
  metricsTable: (state) => {
    return state.metricsTable ? state.metricsTable : []
  }
}
export const graph = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
