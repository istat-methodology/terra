import { axiosR } from "@/http"
export const timeseriesService = {
  findByFilters
}

function findByFilters(form) {
  var object = {}
  object = {
    //flow=1&var=3&country=IT&partner=US&dataType=1&tipovar=1
    flow: form.flow,
    var: form.var,
    country: form.country,
    partner: form.partner,
    dataType: form.dataType,
    tipovar: form.varType
  }
  const params = object

  return axiosR
    .post("/itsa", params)
    .then((res) => {
      var data = res.data ? res.data : {}
      //console.log(data);
      return data
    })
    .catch((err) => {
      throw err
    })
}
