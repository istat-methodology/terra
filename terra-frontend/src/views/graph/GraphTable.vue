<template>
  <CDataTable
    id="metricsTable"
    v-if="data"
    :items="data"
    :fields="fields"
    :sorterValue="sorterValue"
    column-filter
    :items-per-page="10"
    sorter
    hover
    pagination />
</template>
<script>
export default {
  name: "GraphTable",
  props: {
    data: {
      type: Array,
      default: () => null
    },
    fields: {
      type: Array,
      default: () => []
    },
    sorterValue: {
      type: Object,
      default: () => ({ column: null, asc: true })
    }
  }
}
</script>
