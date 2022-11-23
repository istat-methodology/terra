import { metadataService } from "@/services"
import { replaceAllProdId } from "@/common"

const state = {
  loaded: false,
  countries: [],
  transports: [],
  partners: [],
  productsCPA: [],
  productsIntra: [],
  productsExtra: [],
  dataType: [
    {
      id: 1,
      descr_en: "Yearly variation series",
      descr_it: "Variazioni tendenziali"
    },
    {
      id: 2,
      descr_en: "Raw data series",
      descr_it: "Dati grezzi"
    }
  ],
  varType: [
    {
      id: 1,
      descr_en: "Euro",
      descr_it: "Euro"
    },
    {
      id: 2,
      descr_en: "Kilograms",
      descr_it: "Chilogrammi"
    }
  ],
  flows: [
    {
      id: 1,
      descr_en: "Import",
      descr_it: "Import"
    },
    {
      id: 2,
      descr_en: "Export",
      descr_it: "Export"
    }
  ],
  weights: [
    {
      id: 1,
      descr: true
    },
    {
      id: 2,
      descr: false
    }
  ]
}
const mutations = {
  SET_CLS_LOADED(state, loaded) {
    state.loaded = loaded
  },
  SET_COUNTRIES(state, countries) {
    state.countries = countries
  },
  SET_PRODUCTS(state, products) {
    state.products = products
  },
  SET_PRODUCT_PLUS(state, productPlus) {
    state.productPlus = productPlus
  },
  SET_TRANSPORTS(state, transports) {
    state.transports = transports
  },
  SET_PARTNERS(state, partners) {
    state.partners = partners
  },
  SET_BECS(state, becs) {
    state.becs = becs
  },
  SET_PRODUCTS_CPA(state, productsCPA) {
    state.productsCPA = productsCPA
  },
  SET_PRODUCTS_INTRA(state, productsIntra) {
    state.productsIntra = productsIntra
  },
  SET_PRODUCTS_EXTRA(state, productsExtra) {
    state.productsExtra = productsExtra
  }
}
const actions = {
  getClassifications({ dispatch, commit, rootGetters }) {
    const lan = rootGetters["coreui/language"]
    return Promise.all([
      dispatch("getCountries", lan),
      dispatch("getProductsCPA", lan),
      dispatch("getProductsIntra", lan),
      dispatch("getProductsExtra", lan),
      dispatch("getTransports", lan),
      dispatch("getPartners", lan)
    ]).then(() => {
      commit("SET_CLS_LOADED", true)
      return true
    })
  },
  getCountries({ commit }, lan) {
    return metadataService
      .getClassification("countries", lan)
      .then((data) => {
        commit("SET_COUNTRIES", data)
      })
      .catch((err) => {
        console.log(err)
      })
  },
  getProductsCPA({ commit }, lan) {
    return metadataService
      .getClassification("productsCPA", lan)
      .then((data) => {
        commit(
          "SET_PRODUCTS_CPA",
          data.map((prod) => {
            return {
              id: prod.id,
              descr: prod.id + " - " + prod.descr
            }
          })
        )
      })
      .catch((err) => {
        console.log(err)
      })
  },
  getProductsIntra({ commit }, lan) {
    return metadataService
      .getClassification("productsIntra", lan)
      .then((data) => {
        const prods = replaceAllProdId(data)
        commit(
          "SET_PRODUCTS_INTRA",
          prods.map((prod) => {
            return {
              id: prod.id,
              descr: prod.id + " - " + prod.descr
            }
          })
        )
      })
      .catch((err) => {
        console.log(err)
      })
  },
  getProductsExtra({ commit }, lan) {
    return metadataService
      .getClassification("productsExtra", lan)
      .then((data) => {
        const prods = replaceAllProdId(data)
        commit(
          "SET_PRODUCTS_EXTRA",
          prods.map((prod) => {
            return {
              id: prod.id,
              descr: prod.id + " - " + prod.descr
            }
          })
        )
      })
      .catch((err) => {
        console.log(err)
      })
  },
  getTransports({ commit }, lan) {
    return metadataService
      .getClassification("transports", lan)
      .then((data) => {
        //Add 'All' to the list of transports
        data.push({
          id: 99,
          descr: "All"
        })
        commit("SET_TRANSPORTS", data)
      })
      .catch((err) => {
        console.log(err)
      })
  },
  getPartners({ commit }, lan) {
    return metadataService
      .getClassification("partners", lan)
      .then((data) => {
        commit("SET_PARTNERS", data)
      })
      .catch((err) => {
        console.log(err)
      })
  }
}
const getters = {
  clsLoaded: (state) => {
    return state.loaded
  },
  countries: (state) => {
    return state.countries
  },
  productsCPA: (state) => {
    return state.productsCPA
  },
  productsIntra: (state) => {
    return state.productsIntra
  },
  productsExtra: (state) => {
    return state.productsExtra
  },
  transports: (state) => {
    return state.transports
  },
  flows: (state, getters, rootState, rootGetters) => {
    const lan = rootGetters["coreui/language"]
    const descrKey = "descr_" + lan
    return state.flows.map((obj) => {
      return {
        id: obj.id,
        descr: obj[descrKey]
      }
    })
  },
  dataTypes: (state, getters, rootState, rootGetters) => {
    const lan = rootGetters["coreui/language"]
    const descrKey = "descr_" + lan
    return state.dataType.map((obj) => {
      return {
        id: obj.id,
        descr: obj[descrKey]
      }
    })
  },
  varTypes: (state, getters, rootState, rootGetters) => {
    const lan = rootGetters["coreui/language"]
    const descrKey = "descr_" + lan
    return state.varType.map((obj) => {
      return {
        id: obj.id,
        descr: obj[descrKey]
      }
    })
  },
  partners: (state) => {
    return state.partners
  },
  timeNext: (state) => {
    return state.timeNext
  }
}
export const classification = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
