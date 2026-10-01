<template>
  <CSidebar
    fixed
    :minimize="minimize"
    :show="show"
    @update:show="
      (value) => $store.commit('coreui/set', ['sidebarShow', 'responsive'])
    "
    ><div>
      <a class="sr-only sr-only-focusable" href="#list-content">{{
        $t("common.goto_context")
      }}</a>
    </div>
    <CSidebarBrand>
      <a
        href="https://www.istat.it/it/"
        target="_blank"
        tabindex="0"
        :title="$t('sidebar.goto_istat')"
        :aria_label="$t('sidebar.opens_goto_istat')">
        <CImg
          src="../img/LogoIstatCompleto.png"
          style="max-width: 100%"
          alt="" />
      </a>
    </CSidebarBrand>
    <div
      class="c-sidebar-nav h-100"
      style="overflow: auto"
      role="navigation"
      :aria-label="$t('sidebar.main_menu_aria_label')">
      <div class="c-sidebar-nav-item" id="list-content">
        <a
          @click="handleHome"
          @keypress="handleHome"
          class="c-sidebar-nav-link"
          :class="{ 'c-active': isHome }"
          tabindex="0"
          :title="$t('sidebar.home')"
          :aria-current="'false'">
          <CIcon
            name="cil-home"
            class="c-sidebar-nav-icon"
            alt=""
            :title="$t('sidebar.home')" />{{ $t("sidebar.home") }}
        </a>
      </div>
      <div class="c-sidebar-nav-item">
        <a
          @click="handleNews()"
          @keypress="handleNews()"
          class="c-sidebar-nav-link"
          :class="{ 'c-active c-active-danger': isNews }"
          :title="$t('sidebar.news')"
          :aria-current="'false'"
          tabindex="0">
          <CIcon
            name="cil-newspaper"
            class="c-sidebar-nav-icon"
            alt=""
            :title="$t('sidebar.news')" />
          {{ $t("sidebar.news") }}
        </a>
      </div>
      <div class="c-sidebar-nav-item">
        <a
          @click="handleDownload()"
          @keypress="handleDownload()"
          class="c-sidebar-nav-link"
          :class="{ 'c-active c-active-danger': isDownloadData }"
          :title="$t('sidebar.download')"
          :aria-current="'false'"
          tabindex="0">
          <CIcon
            name="cil-cloud-download"
            class="c-sidebar-nav-icon"
            alt=""
            :title="$t('sidebar.download')" />
          {{ $t("sidebar.download") }}
        </a>
      </div>
      <!--div class="c-sidebar-nav-item">
        <a
          @click="handleAPI()"
          @keypress="handleAPI()"
          class="c-sidebar-nav-link"
          :class="{ 'c-active c-active-danger': false }"
          :title="$t('sidebar.api')"
          :aria-current="'false'"
          tabindex="0">
          <CIcon
            name="cil-star"
            class="c-sidebar-nav-icon"
            alt=""
            :title="$t('sidebar.api')" />
          {{ $t("sidebar.api") }}
        </a>
      </div-->
      <div class="c-sidebar-nav-title pb-2">
        {{ $t("sidebar.analysis") }}
      </div>
      <div class="c-sidebar-nav-item">
        <a
          @click="handleMap"
          @keypress="handleMap"
          class="c-sidebar-nav-link"
          :class="{ 'c-active c-active-primary': isMap }"
          tabindex="0"
          :title="$t('sidebar.map')"
          :aria-current="'false'">
          <CIcon
            name="cil-location-pin"
            class="c-sidebar-nav-icon"
            alt=""
            :title="$t('sidebar.map')" />
          {{ $t("sidebar.map") }}
        </a>
      </div>
      <div class="c-sidebar-nav-item">
        <a
          @click="handleGraphExtraUe()"
          @keypress="handleGraphExtraUe()"
          class="c-sidebar-nav-link"
          :class="{ 'c-active c-active-success': isGraph }"
          :title="$t('sidebar.graphExtra')"
          :aria-current="'false'"
          tabindex="0">
          <CIcon
            name="cil-graph"
            class="c-sidebar-nav-icon"
            alt=""
            :title="$t('sidebar.graphExtra')" />{{ $t("sidebar.graphExtra") }}
        </a>
      </div>
      <div class="c-sidebar-nav-item">
        <a
          @click="handleGraphIntraUe()"
          @keypress="handleGraphIntraUe()"
          class="c-sidebar-nav-link"
          :class="{ 'c-active c-active-success': isGraphIntra }"
          :title="$t('sidebar.graphWorld')"
          :aria-current="'false'"
          tabindex="0">
          <CIcon
            name="cil-graph"
            class="c-sidebar-nav-icon"
            alt=""
            :title="$t('sidebar.graphWorld')" />{{ $t("sidebar.graphWorld") }}
        </a>
      </div>
      <div class="c-sidebar-nav-item">
        <a
          @click="handleTimeSeries()"
          @keypress="handleTimeSeries()"
          class="c-sidebar-nav-link"
          :class="{ 'c-active c-active-warning': isPolicy }"
          :title="$t('sidebar.timeseries')"
          :aria-current="$t('sidebar.timeseries')"
          tabindex="0">
          <CIcon
            name="cil-chart-line"
            class="c-sidebar-nav-icon"
            alt=""
            :title="$t('sidebar.timeseries')" />
          {{ $t("sidebar.timeseries") }}
        </a>
      </div>
      <div class="c-sidebar-nav-item">
        <a
          @click="handleTrade()"
          @keypress="handleTrade()"
          class="c-sidebar-nav-link"
          :class="{ 'c-active c-active-danger': isTrade }"
          :title="$t('sidebar.trade')"
          :aria-current="'false'"
          tabindex="0">
          <CIcon
            name="cil-layers"
            class="c-sidebar-nav-icon"
            alt=""
            :title="$t('sidebar.trade')" />
          {{ $t("sidebar.trade") }}
        </a>
      </div>
      <div class="sidebar-resources">
        <div class="c-sidebar-nav-item">
          <a
            class="c-sidebar-nav-link sidebar-resource-link"
            href="https://github.com/istat-methodology/terra"
            target="_blank"
            rel="noopener noreferrer"
            :title="$t('sidebar.repository')"
            :aria-label="$t('sidebar.opens_repository')">
            <CIcon name="cib-github" class="c-sidebar-nav-icon" alt="" />
            {{ $t("sidebar.repository") }}
          </a>
        </div>
        <div class="c-sidebar-nav-item">
          <a
            class="c-sidebar-nav-link sidebar-resource-link"
            href="https://www.cambridge.org/core/journals/world-trade-review/article/exploring-the-complexity-of-international-trade-networks-with-terra/58E2D97F1A1A4179E52C602F9450C4FE"
            target="_blank"
            rel="noopener noreferrer"
            :title="$t('sidebar.paper')"
            :aria-label="$t('sidebar.opens_paper')">
            <CIcon name="cil-description" class="c-sidebar-nav-icon" alt="" />
            {{ $t("sidebar.paper") }}
          </a>
        </div>
        <div class="data-update" :title="$t('common.update') + lastLoadedData">
          <CIcon
            name="cil-tags"
            alt=""
            :title="$t('common.update') + lastLoadedData" />
          {{ $t("common.update") }}
          {{ lastLoadedData }}
        </div>
      </div>
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
      isMobility: "isMobility",
      isNews: "isNews",
      isDownloadData: "isDownloadData"
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
      if (this.$route.path !== "/timeseries") {
        this.$router.push({ name: "TimeSeries" })
      }
    },
    handleTrade() {
      this.$router.push({ name: "Trade" })
    },
    handleNews() {
      this.$router.push({ name: "News" })
    },
    handleDownload() {
      this.$router.push({ name: "DownloadData" })
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
  display: flex;
  align-items: center;
  padding: 0.45rem 1rem;
  font-size: 0.8125rem;
  line-height: 1.25;
}
.data-update .c-icon {
  flex: 0 0 auto;
  margin-right: 0.45rem;
}
.sidebar-resources {
  margin-top: auto;
  flex-shrink: 0;
  padding-top: 0.5rem;
}
.sidebar-resource-link {
  padding: 0.45rem 1rem;
  font-size: 0.8125rem;
  line-height: 1.25;
}
.sidebar-resource-link .c-sidebar-nav-icon {
  flex: 0 0 auto;
  width: 1.1rem;
  margin-left: 0 !important;
  margin-right: 0.45rem;
}
.c-sidebar-nav-link:hover {
  cursor: pointer;
}
.c-sidebar-nav-title {
  margin-top: 0;
}
.c-sidebar .c-sidebar-nav-dropdown-toggle .c-sidebar-nav-icon,
.c-sidebar .c-sidebar-nav-link .c-sidebar-nav-icon {
  color: white;
}
a.sr-only.sr-only-focusable {
  color: white;
}
</style>
