<template>
  <div class="row">
    <h1 class="sr-only">
      {{ $t("common.acronym") }}
    </h1>
    <div class="col-sm-6 col-md-4">
      <div class="card" :title="$t('landing.map.title')">
        <header class="card-header" role="heading" aria-level="2">
          <CIcon
            name="cil-location-pin"
            :title="$t('landing.map.title')"
            alt="" />{{ $t("landing.map.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.map.body')"></p>
          <p class="section-link">
            <a
              @click="handleMap"
              @keypress="handleMap"
              tabindex="0"
              :title="$t('landing.map.link')">
              {{ $t("landing.map.link") }}
            </a>
          </p>
        </div>
      </div>
    </div>
    <div class="col-sm-6 col-md-4">
      <div class="card" :title="$t('landing.graph.extra-ue.title')">
        <header class="card-header" role="heading" aria-level="2">
          <CIcon
            name="cil-graph"
            :title="$t('landing.graph.extra-ue.title')"
            alt="" />
          {{ $t("landing.graph.extra-ue.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.graph.extra-ue.body')"></p>
          <p class="section-link">
            <a
              @click="handleGraphExtraUe()"
              @keypress="handleGraphExtraUe()"
              tabindex="0"
              :title="$t('landing.graph.extra-ue.link')"
              >{{ $t("landing.graph.extra-ue.link") }}
            </a>
          </p>
        </div>
      </div>
    </div>
    <div class="col-sm-6 col-md-4">
      <div class="card" :title="$t('landing.graph.intra-ue.title')">
        <header class="card-header" role="heading" aria-level="2">
          <CIcon
            name="cil-graph"
            :title="$t('landing.graph.intra-ue.title')"
            alt="" />
          {{ $t("landing.graph.intra-ue.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.graph.intra-ue.body')"></p>
          <p class="section-link">
            <a
              @click="handleGraphIntraUe()"
              @keypress="handleGraphIntraUe()"
              tabindex="0"
              :title="$t('landing.graph.intra-ue.link')">
              {{ $t("landing.graph.intra-ue.link") }}
            </a>
          </p>
        </div>
      </div>
    </div>
    <div class="col-sm-6 col-md-4">
      <div class="card" :title="$t('landing.timeseries.title')">
        <header class="card-header" role="heading" aria-level="2">
          <CIcon
            name="cil-chart-line"
            :title="$t('landing.timeseries.title')"
            alt="" />
          {{ $t("landing.timeseries.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.timeseries.body')"></p>
          <p class="section-link">
            <a
              @click="handleTimeSeries()"
              @keypress="handleTimeSeries()"
              tabindex="0"
              :title="$t('landing.timeseries.link')">
              {{ $t("landing.timeseries.link") }}
            </a>
          </p>
        </div>
      </div>
    </div>
    <div class="col-sm-6 col-md-4">
      <div class="card" :title="$t('landing.trade.title')">
        <header class="card-header" role="heading" aria-level="2">
          <CIcon name="cil-layers" :title="$t('landing.trade.title')" alt="" />
          {{ $t("landing.trade.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.trade.body')"></p>
          <p class="section-link">
            <a
              @click="handleTrade()"
              @keypress="handleTrade()"
              tabindex="0"
              :title="$t('landing.trade.link')">
              {{ $t("landing.trade.link") }}
            </a>
          </p>
        </div>
      </div>
    </div>
    <div class="col-sm-6 col-md-4">
      <div class="card" :title="$t('landing.news.title')">
        <header class="card-header" role="heading" aria-level="2">
          <CIcon
            name="cil-newspaper"
            :title="$t('landing.news.title')"
            alt="" />
          {{ $t("landing.news.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.news.body')"></p>
          <p class="section-link">
            <a
              @click="handleNews()"
              @keypress="handleNews()"
              tabindex="0"
              :title="$t('landing.news.link')">
              {{ $t("landing.news.link") }}
            </a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Context } from "@/common"
export default {
  name: "Home",
  data() {
    return {
      title: process.env.VUE_APP_TITLE
    }
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
    },
    handleNews() {
      this.$router.push({ name: "News" })
    },
    fixASidebarMenu() {
      setTimeout(() => {
        document.querySelectorAll(".c-sidebar-nav-link").forEach((element) => {
          element.setAttribute("aria-current", "false")
        })
      }, 300)
      setTimeout(() => {
        document
          .querySelectorAll(".c-sidebar-nav-link.c-active")
          .forEach((element) => {
            element.setAttribute("aria-current", "page")
          })
      }, 300)
    },
    fixMetaTitle() {
      setTimeout(() => {
        document.querySelectorAll("title").forEach((element) => {
          element.textContent = "Terra - Home"
        })
      }, 300)
    }
  },
  created() {
    this.$store.dispatch("coreui/setContext", Context.Home)
    this.fixMetaTitle()
    this.fixASidebarMenu()
  }
}
</script>
<style scoped>
.material-design-icon > .material-design-icon__svg {
  bottom: -0.17rem;
}
.card-body {
  padding-bottom: 0.5rem;
}
a {
  text-decoration: underline;
}
a:not([href]) {
  background-color: transparent;
  color: #321fdb;
}
a:not([href]):hover {
  text-decoration: underline;
  cursor: pointer;
}
</style>
