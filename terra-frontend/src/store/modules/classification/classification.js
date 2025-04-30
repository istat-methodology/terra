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
      descr_en: "Lag 12 months differences",
      descr_it: "Serie delle differenze a 12 mesi"
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
  seriesType: [
    {
      id: 1,
      descr_en: "Share trend",
      descr_it: "Andamento delle quote"
    },
    {
      id: 2,
      descr_en: "Share variation",
      descr_it: "Variazioni delle quote"
    }
  ],
  flows: [
    /*{
      id: 0,
      descr_en: "Average",
      descr_it: "Media"
    },
    */
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
  ],
  collapse: [
    {
      id: 0,
      descr_en: "Yes",
      descr_it: "Si",
      value: true
    },
    {
      id: 1,
      descr_en: "No",
      descr_it: "No",
      value: false
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
  getClassifications({ dispatch, commit }) {
    return Promise.all([
      dispatch("getCountries"),
      dispatch("getProductsCPA"),
      dispatch("getProductsIntra"),
      dispatch("getProductsExtra"),
      dispatch("getTransports"),
      dispatch("getPartners")
    ]).then(() => {
      commit("SET_CLS_LOADED", true)
      return true
    })
  },
  getCountries({ commit }) {
    return metadataService
      .getClassification("countries")
      .then((data) => {
        commit("SET_COUNTRIES", data)
      })
      .catch((err) => {
        console.log(err)
      })
  },
  getProductsCPA({ commit }) {
    return metadataService
      .getClassification("productsCPA")
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
  getProductsIntra({ commit, rootGetters }) {
    const isItalian = rootGetters["coreui/isItalian"]
    return metadataService
      .getClassification("productsIntra")
      .then((data) => {
        const prods = replaceAllProdId(data, isItalian)
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
  getProductsExtra({ commit, rootGetters }) {
    const isItalian = rootGetters["coreui/isItalian"]
    return metadataService
      .getClassification("productsExtra")
      .then((data) => {
        const prods = replaceAllProdId(data, isItalian)
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
  getTransports({ commit, rootGetters }) {
    const isItalian = rootGetters["coreui/isItalian"]
    return metadataService
      .getClassification("transports")
      .then((data) => {
        //Add 'All' to the list of transports
        data.unshift({
          id: 99,
          descr: isItalian ? "Tutti i mezzi di trasporto" : "All transports"
        })
        commit("SET_TRANSPORTS", data)
      })
      .catch((err) => {
        console.log(err)
      })
  },
  getPartners({ commit }) {
    return metadataService
      .getClassification("partners")
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
  getCountryName: (state) => (code) => {
    const country = state.countries.find((ctr) => ctr.country == code)
    return country ? country.name : ""
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
  seriesTypes: (state, getters, rootState, rootGetters) => {
    const lan = rootGetters["coreui/language"]
    const descrKey = "descr_" + lan
    return state.seriesType.map((obj) => {
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
  },
  collapse: (state, getters, rootState, rootGetters) => {
    const lan = rootGetters["coreui/language"]
    const descrKey = "descr_" + lan
    return state.collapse.map((obj) => {
      return {
        id: obj.id,
        descr: obj[descrKey],
        value: obj.value
      }
    })
  }
}
export const classification = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
