import { axiosHack } from "@/http"
import store from "@/store"

export const newsService = {
  findAll
}

function findAll() {
  const lan = store.getters["coreui/language"]
  return axiosHack
    .get("/news", { params: { lang: lan } })
    .then((res) => {
      var data = res.data ? res.data : {}
      //console.log(data);
      return data
    })
    .catch((err) => {
      throw err
    })
}