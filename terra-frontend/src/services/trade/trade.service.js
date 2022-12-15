import { axiosHack } from "@/http"
import store from "@/store"
export const tradeService = {
  findByName
}

function findByName(filter) {
  const lan = store.getters["coreui/language"]
  const endpoint =
    filter.seriesType == 1
      ? filter.type == 1
        ? filter.flow == 1
          ? "importQuoteValue_" + lan
          : "exportQuoteValue_" + lan
        : filter.flow == 1
        ? "importQuoteQuantity_" + lan
        : "exportQuoteQuantity_" + lan
      : filter.type == 1
      ? filter.flow == 1
        ? "importValue_" + lan
        : "exportValue_" + lan
      : filter.flow == 1
      ? "importQuantity_" + lan
      : "exportQuantity_" + lan
  return axiosHack
    .get("/" + endpoint + "/" + filter.country)
    .then((res) => {
      var data = res.data ? res.data : {}
      //console.log(data);
      return data
    })
    .catch((err) => {
      throw err
    })
}
