import { filterAnomalousLastPeriod } from "./timeseries"

export function getMapHeaders() {
  return [
    "DECLARANT_ISO",
    "DECLARANT_NAME",
    "FLOW_CODE",
    "FLOW_LABEL",
    "PERIOD",
    "YEAR",
    "MONTH",
    "VALUE_YOY_CHANGE_PERCENT"
  ]
}

export function buildMapCsvRows({ series, flow, getCountryName }) {
  const safeSeries = Array.isArray(series) ? series : []
  if (!safeSeries.length) return { rows: [], removedPeriod: null }

  const periodEntries = Object.keys(safeSeries[0])
    .filter((key) => /^\d{4}-?(0[1-9]|1[0-2])$/.test(key))
    .map((sourceKey) => ({
      sourceKey,
      period: sourceKey.replace("-", "")
    }))
    .sort((a, b) => a.period.localeCompare(b.period))
  const periods = periodEntries.map(({ period }) => period)
  const sourceKeyByPeriod = Object.fromEntries(
    periodEntries.map(({ sourceKey, period }) => [period, sourceKey])
  )
  const byCountry = Object.fromEntries(
    safeSeries.map((countrySeries) => [
      countrySeries.country,
      {
        series: periods.map(
          (period) => countrySeries[sourceKeyByPeriod[period]]
        )
      }
    ])
  )
  const filtered = filterAnomalousLastPeriod({
    dates: periods,
    byPartner: byCountry,
    partnerIds: safeSeries.map((countrySeries) => countrySeries.country)
  })

  return {
    removedPeriod: filtered.removed
      ? `${filtered.removedDate.slice(0, 4)}-${filtered.removedDate.slice(4)}`
      : null,
    rows: safeSeries.flatMap((countrySeries) =>
      filtered.dates.map((period) => {
        const sourceKey = sourceKeyByPeriod[period]
        return {
          DECLARANT_ISO: countrySeries.country || "",
          DECLARANT_NAME: getCountryName(countrySeries.country) || "",
          FLOW_CODE: flow?.id ?? "",
          FLOW_LABEL: flow?.descr || "",
          PERIOD: period,
          YEAR: period.slice(0, 4),
          MONTH: period.slice(4, 6),
          VALUE_YOY_CHANGE_PERCENT: countrySeries[sourceKey]
        }
      })
    )
  }
}
