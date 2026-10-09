export function getTimeseriesMeasureColumn(varType) {
  return varType?.id === 2 ? "QUANTITY_IN_KG" : "VALUE_IN_EUROS"
}

export const PROVISIONAL_LAST_VALUE_THRESHOLD = 0.5

export function filterAnomalousLastPeriod({
  dates,
  byPartner,
  partnerIds,
  dataTypeId = null,
  threshold = PROVISIONAL_LAST_VALUE_THRESHOLD
}) {
  const safeDates = Array.isArray(dates) ? dates : []
  if (safeDates.length < 3) {
    return {
      dates: safeDates,
      byPartner,
      removed: false,
      removedDate: null,
      referenceAverage: null
    }
  }

  let referenceAverage = null
  const hasAnomalousLastValue = (partnerIds || []).some((partnerId) => {
    const series = byPartner?.[partnerId]?.series
    if (!Array.isArray(series) || series.length !== safeDates.length)
      return false

    const numericSeries = series.map((value) => Number(value))
    const previousValues = numericSeries.slice(0, -1).filter(Number.isFinite)
    const lastValue = numericSeries[numericSeries.length - 1]
    if (!previousValues.length || !Number.isFinite(lastValue)) return false

    let isAnomalous = false

    if (Number(dataTypeId) === 2 && series.length >= 13) {
      // Raw monthly values are seasonal: require the provisional month to be
      // below both the previous month and the same month of the previous year.
      const previousYearValue = numericSeries[numericSeries.length - 13]
      const previousMonthValue = numericSeries[numericSeries.length - 2]
      if (
        Number.isFinite(previousYearValue) &&
        Number.isFinite(previousMonthValue) &&
        lastValue < previousYearValue &&
        lastValue < previousMonthValue
      ) {
        const historicalReference = Math.max(
          previousYearValue,
          previousMonthValue
        )
        isAnomalous =
          historicalReference !== 0 &&
          (historicalReference - lastValue) / Math.abs(historicalReference) >
            threshold
      }
    } else {
      const previousMinimum = Math.min(...previousValues)
      if (lastValue >= previousMinimum) return false

      const historicalScale =
        Math.abs(previousMinimum) || Math.max(...previousValues.map(Math.abs))
      if (historicalScale === 0) return false

      isAnomalous = (previousMinimum - lastValue) / historicalScale > threshold
    }

    if (isAnomalous) {
      referenceAverage =
        previousValues.reduce((sum, value) => sum + value, 0) /
        previousValues.length
    }
    return isAnomalous
  })

  if (!hasAnomalousLastValue) {
    return {
      dates: safeDates,
      byPartner,
      removed: false,
      removedDate: null,
      referenceAverage: null
    }
  }

  return {
    dates: safeDates.slice(0, -1),
    byPartner: Object.fromEntries(
      Object.entries(byPartner || {}).map(([partnerId, partnerData]) => [
        partnerId,
        {
          ...partnerData,
          series: Array.isArray(partnerData?.series)
            ? partnerData.series.slice(0, -1)
            : partnerData?.series
        }
      ])
    ),
    removed: true,
    removedDate: safeDates[safeDates.length - 1],
    referenceAverage
  }
}

export function getTimeseriesHeaders(varType) {
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
    "PERIOD",
    "YEAR",
    "MONTH",
    getTimeseriesMeasureColumn(varType)
  ]
}

export function buildTimeseriesCsvRows({
  country,
  partners,
  flow,
  product,
  dataType,
  varType,
  dates,
  byPartner
}) {
  const measureColumn = getTimeseriesMeasureColumn(varType)
  const productCode = String(product?.id ?? "")
  const productDescription = (product?.descr || "").replace(
    `${productCode} - `,
    ""
  )

  return (partners || []).flatMap((partner) => {
    const series = byPartner?.[partner.id]?.series
    if (!Array.isArray(series)) return []

    return (dates || []).map((date, index) => {
      const period = String(date || "")
        .slice(0, 7)
        .replace("-", "")
      return {
        DECLARANT_ISO: country?.country || "",
        DECLARANT_NAME: country?.name || "",
        PARTNER_ISO: partner.id,
        PARTNER_NAME: partner.descr,
        FLOW_CODE: flow?.id ?? "",
        FLOW_LABEL: flow?.descr || "",
        PRODUCT_CODE: productCode,
        PRODUCT_DESCRIPTION: productDescription,
        PRODUCT_LEVEL: productCode === "00" ? 0 : productCode.length,
        SERIES_TYPE_CODE: dataType?.id ?? "",
        SERIES_TYPE_LABEL: dataType?.descr || "",
        PERIOD: period,
        YEAR: period.slice(0, 4),
        MONTH: period.slice(4, 6),
        [measureColumn]: series[index]
      }
    })
  })
}
