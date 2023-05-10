<template>
  <div class="row">
    <div class="col-sm-6 col-md-4">
      <div class="card">
        <header class="card-header" role="heading" aria-level="1">
          <CIcon name="cil-location-pin" title="Map" />{{
            $t("landing.map.title")
          }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.map.body')"></p>
          <p class="section-link">
            <router-link tag="a" :to="{ name: 'Map' }">
              {{ $t("landing.map.link") }}
            </router-link>
          </p>
        </div>
      </div>
    </div>
    <div class="col-sm-6 col-md-4">
      <div class="card">
        <header class="card-header" role="heading" aria-level="1">
          <CIcon name="cil-graph" title="GraphExtraUe" />
          {{ $t("landing.graph.extra-ue.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.graph.extra-ue.body')"></p>
          <p class="section-link">
            <router-link tag="a" :to="{ name: 'GraphExtraUe' }">
              {{ $t("landing.graph.extra-ue.link") }}
            </router-link>
          </p>
        </div>
      </div>
    </div>
    <div class="col-sm-6 col-md-4">
      <div class="card">
        <header class="card-header" role="heading" aria-level="1">
          <CIcon name="cil-graph" title="GraphIntraUe" />
          {{ $t("landing.graph.intra-ue.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.graph.intra-ue.body')"></p>
          <p class="section-link">
            <router-link tag="a" :to="{ name: 'GraphIntraUe' }">
              {{ $t("landing.graph.intra-ue.link") }}
            </router-link>
          </p>
        </div>
      </div>
    </div>
    <div class="col-sm-6 col-md-4">
      <div class="card">
        <header class="card-header" role="heading" aria-level="1">
          <CIcon name="cil-chart-line" title="TimeSeries" />
          {{ $t("landing.timeseries.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.timeseries.body')"></p>
          <p class="section-link">
            <router-link tag="a" :to="{ name: 'TimeSeries' }">
              {{ $t("landing.timeseries.link") }}
            </router-link>
          </p>
        </div>
      </div>
    </div>
    <div class="col-sm-6 col-md-4">
      <div class="card">
        <header class="card-header" role="heading" aria-level="1">
          <CIcon name="cil-layers" title="Trade" />
          {{ $t("landing.trade.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.trade.body')"></p>
          <p class="section-link">
            <router-link tag="a" :to="{ name: 'Trade' }">
              {{ $t("landing.trade.link") }}
            </router-link>
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
  created() {
    this.$store.dispatch("coreui/setContext", Context.Home)
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
