import { axiosHack } from "@/http"
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

function getClassification(classification, lan) {
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

function getTimeSeriesDefault(lan) {
  return new Promise(function (resolve) {
    setTimeout(() => resolve(defaultTimeSeriesForm(lan)), 200)
  })
}

function getGraphDefault(isIntra, lan) {
  return isIntra ? getGraphIntraDefault(lan) : getGraphExtraDefault(lan)
}

function getGraphExtraDefault(lan) {
  return new Promise(function (resolve) {
    setTimeout(() => resolve(defaultGraphExtraForm(lan)), 200)
  })
}

function getGraphIntraDefault(lan) {
  return new Promise(function (resolve) {
    setTimeout(() => resolve(defaultGraphIntraForm(lan)), 200)
  })
}

function getTradeDefault(lan) {
  return new Promise(function (resolve) {
    setTimeout(() => resolve(defaultTradeForm(lan)), 200)
  })
}
