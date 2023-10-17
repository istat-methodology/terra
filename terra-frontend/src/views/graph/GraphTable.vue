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
    pagination
  
    scopedSlots={{ label: ({ label }) => {  return <th>{nome}</th>; } }}
    columnHeaderSlot={{ label: <i>Custom label Header</i> }}
  -->
  <CDataTable
    id="metricsTable"
    ref="metricsTable"
    v-if="data"
    :items="data"
    :fields="fields"
    :sorterValue="sorterValue"
    column-filter
    :items-per-page="10"
    sorter
    hover
    pagination
    :noItemsView="{
      noResults: this.$t('graph.table.no_filtering_results_available'),
      noItems: this.$t('graph.table.no_items_available')
    }">
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
      const table = this.$refs.metricsTable
      if (table.$el.children[0].children[0].children[0].children) {
        const thead = table.$el.children[0].children[0].children[0].children
        const tr_0 = thead[0].children
        const tr_1 = thead[1].children
        if (tr_0) {
          for (let i = 0; i <= 4; i++) {
            tr_0[i].children[1].ariaLabel =
              this.$t("graph.table.order_field") + tr_0[i].ariaLabel

            tr_1[i].children[0].ariaLabel =
              this.$t("graph.table.search_field") + tr_0[i].ariaLabel
            tr_1[i].children[0].title =
              this.$t("graph.table.search_field") + tr_0[i].ariaLabel
          }
        }
      }
    }
  },
  mounted() {
    //this.fixSortingTable()
  },
  updated() {
    this.fixSortingTable()
  }
}
</script>
