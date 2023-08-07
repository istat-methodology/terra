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
  }
}
</script>
