const state = {
  code: null,
  msg: null,
  serverError: false
}

const mutations = {
  SET_CODE(state, code) {
    state.code = code
  },
  SET_MSG(state, msg) {
    state.msg = msg
  },
  SET_SERVER_ERROR(state, isError) {
    state.serverError = isError
  }
}

const actions = {
  serverError({ commit }, error) {
    commit("SET_CODE", error.status)
    commit("SET_MSG", error.message)
    commit("SET_SERVER_ERROR", true)
  }
}

const getters = {
  code: (state) => {
    return state.code
  },
  msg: (state) => {
    return state.msg
  },
  serverError: (state) => {
    return state.serverError
  }
}

export const error = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
