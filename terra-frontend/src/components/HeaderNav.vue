<template>
  <div class="c-subheader-nav mfe-2" v-if="isHome" tabindex="0"></div>
</template>

<script>
import { mapGetters } from "vuex"

export default {
  computed: {
    ...mapGetters("coreui", ["isHome"])
  },
  watch: {
    $route(to) {
      if (to.path == "/metadata") {
        this.$store.dispatch("coreui/clearContext")
      }
    }
  }
}
</script>
