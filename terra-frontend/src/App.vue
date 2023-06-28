<template>
  <div id="app">
    <div class="c-app">
      <app-sidebar tabindex="-1" />
      <CWrapper>
        <app-toast tabindex="-1" />
        <app-header tabindex="-1" />
        <div class="c-body" tabindex="-1">
          <main class="c-main">
            <CContainer fluid>
              <transition name="fade" mode="out-in">
                <router-view
                  :key="$route.fullPath"
                  v-if="isMetaLoaded"></router-view>
              </transition>
            </CContainer>
            <div class="disclaimer" role="note" v-if="isHome">
              {{ $t("landing.disclaimer") }}
            </div>
          </main>
          <app-footer />
        </div>
      </CWrapper>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import Header from "@/components/Header"
import Footer from "@/components/Footer"
import Sidebar from "@/components/Sidebar"
import Toast from "@/components/Toast"
export default {
  name: "App",
  components: {
    "app-header": Header,
    "app-footer": Footer,
    "app-sidebar": Sidebar,
    "app-toast": Toast
  },
  data: () => ({
    isMetaLoaded: false
  }),
  computed: {
    ...mapGetters("coreui", ["isHome"]),
    ...mapGetters("metadata", ["appVersion"]),
    ...mapGetters("metadata", ["lastLoadedData"])
  },
  created() {
    //Clear messages
    this.$store.dispatch("message/clear")
    this.$store.dispatch("coreui/clearContext")
    // load metadata
    this.$store.dispatch("metadata/getMetadata").then(() => {
      // load classifications
      this.$store.dispatch("classification/getClassifications").then(() => {
        this.isMetaLoaded = true
      })
    })
  }
}
</script>
<style lang="scss">
// Import Main styles for this application
@import "./assets/scss/style";

//Transition
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.disclaimer {
  position: relative;
  bottom: 0;
  font-weight: 600;
  font-size: 0.8rem;
  padding: 1rem 1.8rem 1.2rem 1.8rem;
}
</style>
