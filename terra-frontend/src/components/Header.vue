<template>
  <CHeader fixed with-subheader light>
    <CToggler
      in-header
      class="ml-3 d-lg-none"
      @click="$store.dispatch('coreui/toggleSidebarMobile')" />
    <CToggler
      in-header
      class="ml-3 d-md-down-none"
      @click="$store.dispatch('coreui/toggleSidebarDesktop')" />

    <CHeaderNav class="mr-auto">
      <CHeaderNavItem>
        <CImg
          src="../img/LogoTerraFull.png"
          style="max-width: 80%"
          class="d-md-down-none" />
        <CImg
          src="../img/LogoTerraShort.png"
          style="max-width: 80%"
          class="d-lg-none" />
      </CHeaderNavItem>
    </CHeaderNav>
    <CHeaderNav>
      <CHeaderNavItem>
        <CImg src="../img/LogoSTSP.png" style="max-width: 75%" />
      </CHeaderNavItem>
      <CButtonGroup role="group" class="mr-lang">
        <CButton
          color="primary"
          variant="ghost"
          square
          size="sm"
          :class="{ active: selectedIt }"
          @click="selectLanguage('it')"
          >IT</CButton
        >
        <CButton
          color="primary"
          variant="ghost"
          square
          size="sm"
          :class="{ active: selectedEn }"
          @click="selectLanguage('en')"
          >EN</CButton
        >
      </CButtonGroup>
    </CHeaderNav>
  </CHeader>
</template>

<script>
import { mapGetters } from "vuex"

export default {
  data() {
    return {
      langs: ["it", "en"],
      selectedIt: false,
      selectedEn: false
    }
  },
  computed: {
    ...mapGetters("metadata", ["lastLoadedData"]),
    ...mapGetters("coreui", ["isItalian"])
  },
  methods: {
    selectLanguage(lan) {
      this.$i18n.locale = lan
      this.selectedIt = lan == "it" ? true : false
      this.selectedEn = lan == "en" ? true : false
      this.$store.dispatch("coreui/setLanguage", lan)
      //update classifications
      this.$store.dispatch("classification/getClassifications")
      //redirect to Home
      if (this.$router.currentRoute.path != "/") this.$router.push("/")
      this.$store.dispatch("message/success", this.$t("common.update_cls"))
    }
  },
  created() {
    this.selectedIt = this.isItalian
    this.selectedEn = !this.isItalian
  }
}
</script>

<style scoped>
.title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #321fdb;
}
.c-header-nav {
  padding-left: 0.5rem;
}
.c-icon {
  margin-right: 0.4rem;
}
.b-0 > .material-design-icon__svg {
  bottom: 0;
}
.dropdown-item a {
  color: #4f5d73;
}
.dropdown-item a:active,
.dropdown-item a:hover,
.dropdown-item a:focus {
  color: #321fdb;
  text-decoration: none;
}
.dropdown-item.active,
.dropdown-item:active {
  text-decoration: none;
  color: #321fdb;
  background-color: #fff;
}
.dropdown-item:hover,
.dropdown-item:focus {
  text-decoration: none;
  color: #321fdb;
  background-color: #fff;
}
.btn-group .active {
  color: #fff;
  background-color: #321fdb;
  border-color: #321fdb;
}
.mr-lang {
  margin-right: 2.5rem;
  text-align: right;
}
@media (max-width: 450px) {
  .mr-lang {
    margin-right: 0.9rem;
    text-align: right;
  }
}
.mr-title {
  margin-right: 2.5rem;
  text-align: center;
}
.ul-lang {
  margin-right: 2rem;
  list-style: none;
}
.ul-lang .nav-link {
  padding: 1rem 0.5rem;
  color: #636f83;
}
.ul-lang .nav-link:hover {
  color: #321fdb;
  text-decoration: underline;
  text-decoration-color: #321fdb;
}
</style>
