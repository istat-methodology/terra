import { axiosHack } from "@/http"
export const newsService = {
  findAll
}

function findAll() {
  return axiosHack
    .get("/news")
    .then((res) => {
      var data = res.data ? res.data : {}
      //console.log(data);
      return data
    })
    .catch((err) => {
      throw err
    })
}
