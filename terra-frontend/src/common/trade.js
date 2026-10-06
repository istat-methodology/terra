export function getTradeMeasureColumn(seriesType, varType) {
  const measure = varType?.id === 2 ? "QUANTITY" : "VALUE"
  const metric = seriesType?.id === 2 ? "SHARE_CHANGE_PERCENT" : "SHARE_PERCENT"
  return `${measure}_${metric}`
}

export function getTradeHeaders(seriesType, varType) {
  return [
    "DECLARANT_ISO",
    "DECLARANT_NAME",
    "PARTNER_ISO",
    "PARTNER_NAME",
    "FLOW_CODE",
    "FLOW_LABEL",
    "PRODUCT_CODE",
    "PRODUCT_DESCRIPTION",
    "PRODUCT_LEVEL",
    "SERIES_TYPE_CODE",
    "SERIES_TYPE_LABEL",
    "MEASURE_TYPE_CODE",
    "MEASURE_TYPE_LABEL",
    "PERIOD",
    "YEAR",
    "MONTH",
    getTradeMeasureColumn(seriesType, varType)
  ]
}

export function buildTradeCsvRows({
  country,
  partnerName,
  flow,
  selectedProducts,
  products,
  seriesType,
  varType,
  periods
}) {
  const measureColumn = getTradeMeasureColumn(seriesType, varType)
  const selectedAll = (selectedProducts || []).some(
    (product) => product.id === "00"
  )
  const selectedNames = (selectedProducts || []).map(
    (product) => product.dataname
  )

  return (products || [])
    .filter(
      (product) => selectedAll || selectedNames.includes(product.dataname)
    )
    .flatMap((product) => {
      const productCode = String(product.productID ?? "")
      return (periods || []).map((period, index) => ({
        DECLARANT_ISO: country?.country || "",
        DECLARANT_NAME: country?.name || "",
        PARTNER_ISO: "AC",
        PARTNER_NAME: partnerName || "",
        FLOW_CODE: flow?.id ?? "",
        FLOW_LABEL: flow?.descr || "",
        PRODUCT_CODE: productCode,
        PRODUCT_DESCRIPTION: product.dataname || "",
        PRODUCT_LEVEL: productCode === "00" ? 0 : productCode.length,
        SERIES_TYPE_CODE: seriesType?.id ?? "",
        SERIES_TYPE_LABEL: seriesType?.descr || "",
        MEASURE_TYPE_CODE: varType?.id ?? "",
        MEASURE_TYPE_LABEL: varType?.descr || "",
        PERIOD: period.id,
        YEAR: period.id.slice(0, 4),
        MONTH: period.id.slice(4, 6),
        [measureColumn]: product.value?.[index]
      }))
    })
}
