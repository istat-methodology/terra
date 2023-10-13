<template>
  <!--CDataTable
    id="metricsTable"
    v-if="data"
    :items="data"
    :fields="fields"
    :sorterValue="sorterValue"
    column-filter
    :items-per-page="10"
    sorter
    hover
    pagination-->
  <CDataTable
    id="metricsTable"
    ref="metricsTable"
    v-if="data"
    :items="data"
    :fields="fields"
    :items-per-page="10"
    sorter
    hover
    pagination>
    <template #label="{ item }">
      <td headers="head_0">
        {{ item.label }}
      </td>
    </template>
    <template #name="{ item }">
      <td headers="head_1">
        {{ item.name }}
      </td>
    </template>
    <template #vulnerability="{ item }">
      <td headers="head_2">
        {{ item.vulnerability }}
      </td>
    </template>
    <template #hubness="{ item }">
      <td headers="head_3">
        {{ item.hubness }}
      </td>
    </template>
    <template #exportStrenght="{ item }">
      <td headers="head_4">
        {{ item.exportStrenght }}
      </td>
    </template>
  </CDataTable>
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
  },
  methods: {
    fixSortingTable() {
      var table = this.$refs.metricsTable
      console.log(table)
      var columns = table.columnNames
      console.log(columns)
      columns.forEach((colum, index) => {
        var i = index + 1
        this.setAriaLabel(table, colum, i)
      })
    },
    setAriaLabel(table, colum, i) {
      var svg = table.$el.__vue__.$children[i].$el
      console.log("table:" + table)
      console.log("column:" + colum)
      console.log("i:" + i)
      console.log("svg aria label init => " + svg.ariaLabel)
      svg.ariaLabel = this.$t("common.order_field") + colum
      console.log("svg aria label end => " + svg.ariaLabel)
    }
  },
  mounted() {
    this.fixSortingTable()
  },
  updated() {
    this.fixSortingTable()
  }
}
</script>
