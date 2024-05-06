import { newsService } from "@/services"
const state = {
  news: null
}
const mutations = {
  SET_JSON_NEWS(state, news) {
    state.news = news
  }
}
const actions = {
  findAll({ commit }) {
    return newsService
      .findAll()
      .then((data) => {
        commit("SET_JSON_NEWS", data)
      })
      .catch((err) => {
        console.log(err)
      })
  }
}
const getters = {
  news: (state) => {
    return state.news
  }
}
export const news = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}