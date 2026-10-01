<template>
  <div class="row">
    <h1 class="sr-only">
      {{ $t("common.acronym") }}
    </h1>
    <section class="col-12" :aria-label="$t('landing.featured.aria_label')">
      <div class="featured-card">
        <div class="featured-item featured-item--repository">
          <div class="featured-heading">
            <CIcon name="cil-terminal" alt="" />
            <h2>{{ $t("landing.featured.repository.title") }}</h2>
          </div>
          <p>{{ $t("landing.featured.repository.body") }}</p>
          <a
            href="https://github.com/istat-methodology/terra"
            target="_blank"
            rel="noopener noreferrer"
            :aria-label="$t('landing.featured.repository.aria_label')">
            {{ $t("landing.featured.repository.link") }}
            <span aria-hidden="true">↗</span>
          </a>
        </div>
        <div class="featured-item featured-item--publication">
          <div class="featured-heading">
            <CIcon name="cil-newspaper" alt="" />
            <h2>{{ $t("landing.featured.publication.title") }}</h2>
            <span class="open-access">Open Access</span>
          </div>
          <p>
            {{ $t("landing.featured.publication.body_before") }}
            <cite
              >Exploring the Complexity of International Trade Networks with
              TERRA</cite
            >,
            {{ $t("landing.featured.publication.body_after") }}
          </p>
          <a
            href="https://www.cambridge.org/core/journals/world-trade-review/article/exploring-the-complexity-of-international-trade-networks-with-terra/58E2D97F1A1A4179E52C602F9450C4FE"
            target="_blank"
            rel="noopener noreferrer"
            :aria-label="$t('landing.featured.publication.aria_label')">
            {{ $t("landing.featured.publication.link") }}
            <span aria-hidden="true">↗</span>
          </a>
        </div>
      </div>
    </section>
    <div class="col-sm-6 col-md-4">
      <!--div class="card" :title="$t('landing.map.title')">
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
      </div-->
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
            alt="" />{{ $t("landing.graph.extra-ue.title") }}
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
.featured-card {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.45fr);
  margin-bottom: 1.5rem;
  overflow: hidden;
  background: #fff;
  border: 1px solid #d8dbe0;
  border-top: 4px solid #86bc25;
  border-radius: 0.25rem;
  box-shadow: 0 1px 1px 0 rgba(60, 75, 100, 0.14);
}
.featured-item {
  padding: 1.15rem 1.5rem 1.2rem;
}
.featured-item + .featured-item {
  border-left: 1px solid #d8dbe0;
}
.featured-heading {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.65rem;
  color: #3c4b64;
}
.featured-heading h2 {
  margin: 0;
  font-size: 1.08rem;
  font-weight: 700;
}
.featured-item p {
  margin-bottom: 0.65rem;
  color: #4f5d73;
}
.featured-item a {
  font-weight: 600;
  text-decoration: underline;
}
.open-access {
  display: inline-block;
  padding: 0.15rem 0.5rem;
  color: #31520b;
  background: #e9f4d7;
  border-radius: 1rem;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}
@media (max-width: 767.98px) {
  .featured-card {
    grid-template-columns: 1fr;
  }
  .featured-item + .featured-item {
    border-top: 1px solid #d8dbe0;
    border-left: 0;
  }
}
</style>
