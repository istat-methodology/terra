// store/modules/download.js

// importa la service (adatta il path al tuo progetto)
import { fetchData } from "@/services"

const state = () => ({
  data: {}, // ultima risposta
  loading: false, // stato richiesta
  error: null // errore richiesta
})

const getters = {
  data: (s) => s.data,
  loading: (s) => s.loading,
  error: (s) => s.error,
  hasData: (s) => s.data && Object.keys(s.data).length > 0
}

const mutations = {
  SET_LOADING(state, value) {
    state.loading = value
  },
  SET_DATA(state, value) {
    state.data = value || {}
  },
  SET_ERROR(state, value) {
    state.error = value
  },
  RESET(state) {
    state.data = {}
    state.loading = false
    state.error = null
  }
}

const actions = {
  /**
   * payload:
   * {
   *   product_class: "cpa" | "nstr",
   *   period: Number,
   *   country: String,
   *   partner: String | null,
   *   product: String,
   *   flow: 1 | 2,
   *   criterion: 1 | 2,
   *   transport: Array | null
   * }
   */
  async fetchData({ commit }, payload) {
    commit("SET_LOADING", true)
    commit("SET_ERROR", null)

    try {
      const data = await fetchData(payload)
      commit("SET_DATA", data)
      return data // utile per chi chiama: await dispatch(...)
    } catch (err) {
      commit("SET_ERROR", err)
      commit("SET_DATA", {})
      throw err
    } finally {
      commit("SET_LOADING", false)
    }
  },

  reset({ commit }) {
    commit("RESET")
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
