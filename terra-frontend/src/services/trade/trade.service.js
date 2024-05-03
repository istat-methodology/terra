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
          ? "importQuoteValue"
          : "exportQuoteValue"
        : filter.flow == 1
        ? "importQuoteQuantity"
        : "exportQuoteQuantity"
      : filter.type == 1
      ? filter.flow == 1
        ? "importValue"
        : "exportValue"
      : filter.flow == 1
      ? "importQuantity"
      : "exportQuantity"
  return axiosHack
    .get("/" + endpoint, { params: { id: filter.country, lang: lan } })
    .then((res) => {
      var data = res.data ? res.data[0] : {}
      //console.log(data);
      return data
    })
    .catch((err) => {
      throw err
    })
}
