// Dynamyc Time default
export const monthDefault = {
  id: "202212",
  descr_en: "Dec 2022",
  descr_it: "Dic 2022"
}
export const trimesterDefault = {
  id: "202204",
  descr: "T4 2022"
}

export const frequencyDefault = "Monthly"

export const sliderDefault = monthDefault.id

//Graph percentage
export const percentageDefault = "80"

// Form defaults
export const dataTypeDefault = {
  id: 1,
  descr_en: "Lag 12 months differences",
  descr_it: "Serie delle differenze a 12 mesi"
}

export const varTypeDefault = {
  id: 1,
  descr_en: "Euro",
  descr_it: "Euro"
}

export const seriesTypeDefault = {
  id: 1,
  descr_en: "Share trend",
  descr_it: "Andamento delle quote"
}

export const flowDefault = {
  id: 1,
  descr_en: "Import",
  descr_it: "Import"
}

export const countryDefault = {
  id: "IT",
  descr_en: "Italy",
  descr_it: "Italia"
}

export const partnerDefault = {
  id: "AC",
  descr_en: "All countries",
  descr_it: "Tutti i paesi"
}

export const productCPADefault = {
  id: "00",
  descr_en: "00 - All products",
  descr_it: "00 - Tutti i prodotti"
}

/** Trade default */
export const idAllProducts = "00"

export const productCPA2Default = {
  id: "00",
  name_en: "All products",
  name_it: "All products",
  descr_en: "00 - All products",
  descr_it: "00 - Tutti i prodotti"
}

export const productExtraDefault = {
  id: "000",
  descr_en: "000 - All products",
  descr_it: "000 - Tutti i prodotti"
}

export const productIntraDefault = {
  id: "000",
  descr_en: "000 - All products",
  descr_it: "000 - Tutti i prodotti"
}

export const transportDefault = {
  id: 99,
  descr_en: "All transports",
  descr_it: "Tutti i mezzi di trasporto "
}

export const getDefaultForm = (lan) => {
  const descrKey = "descr_" + lan
  const nameKey = "name_" + lan
  const time = { id: monthDefault.id, descr: monthDefault[descrKey] }
  const dataType = { id: dataTypeDefault.id, descr: dataTypeDefault[descrKey] }
  const varType = { id: varTypeDefault.id, descr: varTypeDefault[descrKey] }
  const seriesType = {
    id: seriesTypeDefault.id,
    descr: seriesTypeDefault[descrKey]
  }
  const flow = { id: flowDefault.id, descr: flowDefault[descrKey] }
  const country = { country: countryDefault.id, name: countryDefault[descrKey] }
  const partner = { id: partnerDefault.id, descr: partnerDefault[descrKey] }
  const transport = {
    id: transportDefault.id,
    descr: transportDefault[descrKey]
  }
  const productCPA = {
    id: productCPADefault.id,
    descr: productCPADefault[descrKey]
  }
  const productCPA2 = {
    id: productCPA2Default.id,
    dataname: productCPA2Default[nameKey],
    displayName: productCPA2Default[descrKey]
  }
  const productIntra = {
    id: productIntraDefault.id,
    descr: productIntraDefault[descrKey]
  }
  const productExtra = {
    id: productExtraDefault.id,
    descr: productExtraDefault[descrKey]
  }
  return {
    time,
    dataType,
    varType,
    seriesType,
    flow,
    country,
    partner,
    transport,
    productCPA,
    productCPA2,
    productIntra,
    productExtra
  }
}

export const defaultTimeSeriesForm = (lan) => {
  const defaultForm = getDefaultForm(lan)
  return {
    dataType: defaultForm.dataType,
    varType: defaultForm.varType,
    flow: defaultForm.flow,
    country: defaultForm.country,
    partner: defaultForm.partner,
    productCPA: defaultForm.productCPA
  }
}

export const defaultGraphExtraForm = (lan) => {
  const defaultForm = getDefaultForm(lan)
  return {
    time: monthDefault,
    frequency: frequencyDefault,
    percentage: percentageDefault,
    transport: [defaultForm.transport],
    product: defaultForm.productExtra,
    flow: defaultForm.flow
  }
}

export const defaultGraphIntraForm = (lan) => {
  const defaultForm = getDefaultForm(lan)
  return {
    time: monthDefault,
    frequency: frequencyDefault,
    percentage: percentageDefault,
    transport: [],
    product: defaultForm.productIntra,
    flow: defaultForm.flow
  }
}

export const defaultTradeForm = (lan) => {
  const defaultForm = getDefaultForm(lan)
  return {
    idAllProducts: idAllProducts,
    varType: defaultForm.varType,
    seriesType: defaultForm.seriesType,
    flow: defaultForm.flow,
    country: defaultForm.country,
    product: [defaultForm.productCPA2]
  }
}
