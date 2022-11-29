import { axiosHack } from "@/http"
import store from "@/store"

import {
  defaultTimeSeriesForm,
  defaultGraphExtraForm,
  defaultGraphIntraForm,
  defaultTradeForm
} from "@/common"
export const metadataService = {
  getMetadata,
  getClassification,
  getTimeSeriesDefault,
  getGraphDefault,
  getGraphExtraDefault,
  getGraphIntraDefault,
  getTradeDefault
}

function getMetadata() {
  return axiosHack
    .get("/metadata")
    .then((res) => {
      var data = res.data ? res.data : {}
      return data
    })
    .catch((err) => {
      throw err
    })
}

function getClassification(classification) {
  const lan = store.getters["coreui/language"]
  return axiosHack
    .get("/" + classification + "_" + lan)
    .then((res) => {
      var data = res.data ? res.data : {}
      //console.log(data);
      return data
    })
    .catch((err) => {
      throw err
    })
}

function getTimeSeriesDefault() {
  const lan = store.getters["coreui/language"]
  return new Promise(function (resolve) {
    setTimeout(() => resolve(defaultTimeSeriesForm(lan)), 200)
  })
}

function getGraphDefault(isIntra) {
  return isIntra ? getGraphIntraDefault() : getGraphExtraDefault()
}

function getGraphExtraDefault() {
  const lan = store.getters["coreui/language"]
  return new Promise(function (resolve) {
    setTimeout(() => resolve(defaultGraphExtraForm(lan)), 200)
  })
}

function getGraphIntraDefault() {
  const lan = store.getters["coreui/language"]
  return new Promise(function (resolve) {
    setTimeout(() => resolve(defaultGraphIntraForm(lan)), 200)
  })
}

function getTradeDefault() {
  const lan = store.getters["coreui/language"]
  return new Promise(function (resolve) {
    setTimeout(() => resolve(defaultTradeForm(lan)), 200)
  })
}
