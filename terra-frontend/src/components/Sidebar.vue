<template>
  <CSidebar
    role="complementary"
    fixed
    :minimize="minimize"
    :show="show"
    @update:show="
      (value) => $store.commit('coreui/set', ['sidebarShow', 'responsive'])
    ">
    <CSidebarBrand>
      <a
        href="https://www.istat.it/it/"
        target="_blank"
        aria-label="Istat"
        tabindex="1">
        <CImg
          src="../img/LogoIstatCompleto.png"
          style="max-width: 100%"
          :alt="$t('sidebar.logo_istat')"
          aria-label="Logo Istat" />
      </a>
    </CSidebarBrand>
    <ul
      class="c-sidebar-nav h-100"
      role="navigation"
      aria-label="Main"
      style="overflow: hidden">
      <li class="c-sidebar-nav-item" role="navigation" aria-label="Home">
        <a
          @click="handleHome"
          class="c-sidebar-nav-link"
          :class="{ 'c-active': isHome }"
          tabindex="2">
          <CIcon
            name="cil-home"
            class="c-sidebar-nav-icon"
            alt="Home"
            title="Home" />{{ $t("sidebar.home") }}
        </a>
      </li>
      <li
        class="c-sidebar-nav-title pb-2"
        role="navigation"
        aria-label="Analisi">
        {{ $t("sidebar.analysis") }}
      </li>
      <li class="c-sidebar-nav-item" role="navigation" aria-label="Mappa">
        <a
          @click="handleMap"
          class="c-sidebar-nav-link"
          :class="{ 'c-active c-active-primary': isMap }"
          tabindex="3">
          <CIcon
            name="cil-location-pin"
            class="c-sidebar-nav-icon"
            title="Map" />
          {{ $t("sidebar.map") }}
        </a>
      </li>
      <li class="c-sidebar-nav-item" role="navigation" aria-label="Grafo Extra">
        <a
          @click="handleGraphExtraUe()"
          class="c-sidebar-nav-link"
          :class="{ 'c-active c-active-success': isGraph }"
          tabindex="4">
          <CIcon
            name="cil-graph"
            class="c-sidebar-nav-icon"
            title="GraphExtraUe" />{{ $t("sidebar.graphExtra") }}
        </a>
      </li>
      <li class="c-sidebar-nav-item" role="navigation" aria-label="Grafo Intra">
        <a
          @click="handleGraphIntraUe()"
          class="c-sidebar-nav-link"
          :class="{ 'c-active c-active-success': isGraphIntra }"
          tabindex="5">
          <CIcon
            name="cil-graph"
            class="c-sidebar-nav-icon"
            title="GraphIntraUe" />{{ $t("sidebar.graphWorld") }}
        </a>
      </li>
      <li
        class="c-sidebar-nav-item"
        role="navigation"
        aria-label="Serie storica">
        <a
          @click="handleTimeSeries()"
          class="c-sidebar-nav-link"
          :class="{ 'c-active c-active-warning': isPolicy }"
          tabindex="6">
          <CIcon
            name="cil-chart-line"
            class="c-sidebar-nav-icon"
            title="TimeSeries" />
          {{ $t("sidebar.timeseries") }}
        </a>
      </li>
      <li class="c-sidebar-nav-item" role="navigation" aria-label="Paniere">
        <a
          @click="handleTrade()"
          class="c-sidebar-nav-link"
          :class="{ 'c-active c-active-danger': isTrade }"
          tabindex="7">
          <CIcon name="cil-layers" class="c-sidebar-nav-icon" title="Trade" />
          {{ $t("sidebar.trade") }}
        </a>
      </li>
    </ul>
    <span
      role="region"
      class="data-update"
      :aria-label="$t('common.update') + lastLoadedData">
      <CIcon name="cil-tags" title="Update" /> {{ $t("common.update") }}
      {{ lastLoadedData }}</span
    >
  </CSidebar>
</template>
<script>
import { mapGetters } from "vuex"
export default {
  data() {
    return {
      title: process.env.VUE_APP_TITLE
    }
  },
  computed: {
    ...mapGetters("coreui", {
      show: "sidebarShow",
      minimize: "sidebarMinimize",
      isHome: "isHome",
      isMap: "isMap",
      isGraph: "isGraph",
      isGraphIntra: "isGraphIntra",
      isPolicy: "isPolicy",
      isTrade: "isTrade",
      isMobility: "isMobility"
    }),
    ...mapGetters("metadata", ["appVersion"]),
    ...mapGetters("metadata", ["lastLoadedData"])
  },
  methods: {
    handleHome() {
      this.$router.push({ name: "Home" })
    },
    handleMap() {
      this.$router.push({ name: "Map" })
    },
    handleGraphExtraUe() {
      this.$router.push({ name: "GraphExtraUe" })
    },
    handleGraphIntraUe() {
      this.$router.push({ name: "GraphIntraUe" })
    },
    handleTimeSeries() {
      this.$router.push({ name: "TimeSeries" })
    },
    handleTrade() {
      this.$router.push({ name: "Trade" })
    }
  }
}
</script>
<style scoped>
.brand {
  font-size: 1.2rem;
}
.c-active-primary {
  border-left: 3px solid#321fdb;
}
.c-active-success {
  border-left: 3px solid#2eb85c;
}
.c-active-warning {
  border-left: 3px solid#f9b115;
}
.c-active-danger {
  border-left: 3px solid#e55353;
}
a:hover {
  text-decoration: none;
}
.data-update {
  position: absolute;
  bottom: 0;
  padding: 0.8445rem 1rem;
}
</style>
