//import { axiosHack } from "@/http"
import { axiosPython } from "@/http"
import store from "@/store"

export function fetchData(payload) {
  const lang = store.getters["coreui/language"]

  return axiosPython
    .post("/downloadData", payload, {
      params: { lang }
    })
    .then((res) => {
      return res.data ? res.data : {}
    })
    .catch((err) => {
      throw err
    })
}
