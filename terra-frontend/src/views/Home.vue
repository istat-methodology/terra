<template>
  <div class="row">
    <div class="col-sm-6 col-md-4">
      <div class="card">
        <header class="card-header">
          <CIcon name="cil-location-pin" />{{ $t("landing.map.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.map.body')"></p>
          <p class="section-link">
            <router-link :to="{ name: 'Map' }" custom v-slot="{ navigate }">
              <a @click="navigate" @keypress.enter="navigate" role="link">
                {{ $t("landing.map.link") }}
              </a>
            </router-link>
          </p>
        </div>
      </div>
    </div>
    <div class="col-sm-6 col-md-4">
      <div class="card">
        <header class="card-header">
          <CIcon name="cil-graph" />
          {{ $t("landing.graph.extra-ue.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.graph.extra-ue.body')"></p>
          <p class="section-link">
            <router-link
              :to="{ name: 'GraphExtraUe' }"
              custom
              v-slot="{ navigate }">
              <a @click="navigate" @keypress.enter="navigate" role="link">
                {{ $t("landing.graph.extra-ue.link") }}
              </a>
            </router-link>
          </p>
        </div>
      </div>
    </div>
    <div class="col-sm-6 col-md-4">
      <div class="card">
        <header class="card-header">
          <CIcon name="cil-graph" />
          {{ $t("landing.graph.intra-ue.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.graph.intra-ue.body')"></p>
          <p class="section-link">
            <router-link
              :to="{ name: 'GraphIntraUe' }"
              custom
              v-slot="{ navigate }">
              <a @click="navigate" @keypress.enter="navigate" role="link">
                {{ $t("landing.graph.intra-ue.link") }}
              </a>
            </router-link>
          </p>
        </div>
      </div>
    </div>
    <div class="col-sm-6 col-md-4">
      <div class="card">
        <header class="card-header">
          <CIcon name="cil-chart-line" />
          {{ $t("landing.timeseries.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.timeseries.body')"></p>
          <p class="section-link">
            <router-link
              :to="{ name: 'TimeSeries' }"
              custom
              v-slot="{ navigate }">
              <a @click="navigate" @keypress.enter="navigate" role="link">
                {{ $t("landing.timeseries.link") }}
              </a>
            </router-link>
          </p>
        </div>
      </div>
    </div>
    <div class="col-sm-6 col-md-4">
      <div class="card">
        <header class="card-header">
          <CIcon name="cil-layers" />
          {{ $t("landing.trade.title") }}
        </header>
        <div class="card-body">
          <p v-html="$t('landing.trade.body')"></p>
          <p class="section-link">
            <router-link :to="{ name: 'Trade' }" custom v-slot="{ navigate }">
              <a @click="navigate" @keypress.enter="navigate" role="link">
                {{ $t("landing.trade.link") }}
              </a>
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
    // load metadata
    this.$store.dispatch("metadata/getMetadata").then(() => {
      // load classifications
      this.$store.dispatch("classification/getClassifications")
    })
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
a:not([href]) {
  text-decoration: none;
  background-color: transparent;
  color: #321fdb;
}
a:not([href]):hover {
  text-decoration: underline;
  cursor: pointer;
}
</style>
