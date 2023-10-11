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
      setTimeout(() => {
        this.setAriaLabel("head_0", 1)
        this.setAriaLabel("head_1", 2)
        this.setAriaLabel("head_2", 3)
        this.setAriaLabel("head_3", 4)
        this.setAriaLabel("head_4", 5)
      }, 3000)
    },
    setAriaLabel(tagId, i) {
      var element = document.getElementById(tagId)
      console.log("element:" + tagId)
      var svg = this.$el.__vue__.$children[i].$el
      console.log("svg: " + svg)
      svg.ariaLabel = this.$t("common.order_field") + element.innerText
      console.log("svg aria label : " + svg.ariaLabel)
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
