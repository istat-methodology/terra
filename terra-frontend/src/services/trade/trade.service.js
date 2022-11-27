import { axiosHack } from "@/http"
export const tradeService = {
  findByName
}

function findByName(filter, lan) {
  const endpoint =
    filter.type == 1
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
