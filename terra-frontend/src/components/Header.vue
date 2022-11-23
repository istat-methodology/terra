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
        <span class="title mr-2">TERRA</span>
        <span class="acronym">imporT ExpoRt netwoRk Analysis</span>
      </CHeaderNavItem>
    </CHeaderNav>
    <CHeaderNav class="mr-lang">
      <CHeaderNavItem class="d-md-down-none">
        <span
          ><CIcon name="cil-tags" /> {{ $t("common.update") }}
          {{ lastLoadedData }}</span
        >
      </CHeaderNavItem>
      <CHeaderNavItem class="d-md-down-none">
        <a
          class="nav-link"
          target="_blank"
          href="https://istatcosmostorage.blob.core.windows.net/public/Terra_Manuale.pdf">
          {{ $t("header.userguide") }}
        </a>
      </CHeaderNavItem>
      <CButtonGroup role="group">
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
      selectedIt: true,
      selectedEn: false
    }
  },
  computed: {
    ...mapGetters("auth", ["isAuthenticated"]),
    ...mapGetters("metadata", ["lastLoadedData"])
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
  }
}
</script>

<style scoped>
.title {
  font-size: 1.2rem;
  font-weight: 500;
  color: #321fdb;
}
.acronym {
  font-size: 1rem;
  font-weight: 500;
  color: #3c4b64;
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
