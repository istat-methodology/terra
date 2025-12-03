import { downloadService } from "@/services"
const state = {
  download: null
}
const mutations = {
  SET_JSON_DOWNLOAD(state, download) {
    state.download = download
  }
}
const actions = {
  findAll({ commit }) {
    return downloadService
      .findAll()
      .then((data) => {
        commit("SET_JSON_DOWNLOAD", data)
      })
      .catch((err) => {
        console.log(err)
      })
  }
}
const getters = {
  download: (state) => {
    return state.download
  }
}
export const download = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
