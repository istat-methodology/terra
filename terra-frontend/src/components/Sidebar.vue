<template>
  <CSidebar
    fixed
    :minimize="minimize"
    :show="show"
    @update:show="
      (value) => $store.commit('coreui/set', ['sidebarShow', 'responsive'])
    ">
    <CSidebarBrand to="/">
      <earth-icon class="icon-2x" />
      <span class="brand c-sidebar-brand-full ml-2">{{ title }}</span>
    </CSidebarBrand>
    <ul class="c-sidebar-nav h-100">
      <li class="c-sidebar-nav-item">
        <router-link
          tag="a"
          :to="{ name: 'Home' }"
          class="c-sidebar-nav-link"
          :class="{ 'c-active': isHome }">
          <CIcon name="cil-home" class="c-sidebar-nav-icon" />{{
            $t("sidebar.home")
          }}
          <span class="badge badge-primary"> Ver: {{ appVersion }}</span>
        </router-link>
      </li>
      <li class="c-sidebar-nav-title">Analysis</li>
      <li class="c-sidebar-nav-item">
        <router-link
          tag="a"
          :to="{ name: 'Map' }"
          class="c-sidebar-nav-link"
          :class="{ 'c-active c-active-primary': isMap }">
          <CIcon name="cil-location-pin" class="c-sidebar-nav-icon" />
          {{ $t("sidebar.map") }}
        </router-link>
      </li>
      <li class="c-sidebar-nav-item">
        <router-link
          tag="a"
          :to="{ name: 'GraphExtraUe' }"
          class="c-sidebar-nav-link"
          :class="{ 'c-active c-active-success': isGraph }">
          <CIcon name="cil-graph" class="c-sidebar-nav-icon" />{{
            $t("sidebar.graphExtra")
          }}
        </router-link>
      </li>
      <li class="c-sidebar-nav-item">
        <router-link
          tag="a"
          :to="{ name: 'GraphIntraUe' }"
          class="c-sidebar-nav-link"
          :class="{ 'c-active c-active-success': isGraphIntra }">
          <CIcon name="cil-graph" class="c-sidebar-nav-icon" />{{
            $t("sidebar.graphWorld")
          }}
        </router-link>
      </li>
      <li class="c-sidebar-nav-item">
        <router-link
          tag="a"
          :to="{ name: 'TimeSeries' }"
          class="c-sidebar-nav-link"
          :class="{ 'c-active c-active-warning': isPolicy }">
          <CIcon name="cil-chart-line" class="c-sidebar-nav-icon" />
          {{ $t("sidebar.timeseries") }}
        </router-link>
      </li>
      <li class="c-sidebar-nav-item">
        <router-link
          tag="a"
          :to="{ name: 'Trade' }"
          class="c-sidebar-nav-link"
          :class="{ 'c-active c-active-danger': isTrade }">
          <CIcon name="cil-layers" class="c-sidebar-nav-icon" />
          {{ $t("sidebar.trade") }}
        </router-link>
      </li>
    </ul>
    <div class="brand c-sidebar-brand-full text-center">
      <CImg
        src="../img/LogoCircolareSperiStat.png"
        class="mb-3 p-0"
        style="max-width: 50%" />
    </div>
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
    ...mapGetters("metadata", ["appVersion"])
  }
}
</script>
<style scoped>
.brand {
  font-size: 2rem;
  padding-left: 1rem;
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
.brand {
  padding-left: 0 !important;
}
.text-green {
  color: #76b729;
  font-size: 1.6rem;
  font-family: Verdana;
  text-shadow: 0.05rem 0.05rem #6fb2ffb6;
}
a:hover {
  text-decoration: none;
}
</style>
