<template>
  <CHeader with-subheader light tabindex="0">
    <CToggler
      in-header
      class="ml-3 d-lg-none"
      @click="$store.dispatch('coreui/toggleSidebarMobile')"
      @keypress="$store.dispatch('coreui/toggleSidebarMobile')"
      :aria-label="$t('header.toggler')"
      :title="
        sidebarShow === false ? $t('header.no_toggler') : $t('header.toggler')
      "
      tabindex="0" />
    <CToggler
      in-header
      class="ml-3 d-md-down-none"
      @click="$store.dispatch('coreui/toggleSidebarDesktop')"
      @keypress="$store.dispatch('coreui/toggleSidebarDesktop')"
      :aria-label="$t('header.no_toggler')"
      :title="
        sidebarShow === false ? $t('header.no_toggler') : $t('header.toggler')
      "
      tabindex="0" />

    <CHeaderNav class="mr-auto" tabindex="-1">
      <CHeaderNavItem tabindex="-1">
        <CImg
          src="../img/LogoTerraFull.png"
          style="max-width: 95%"
          class="d-md-down-none"
          :alt="$t('header.logo_terra')"
          :title="$t('header.logo_terra')"
          :aria-label="$t('header.logo_terra')"
          tabindex="0" />
        <CImg
          src="../img/LogoTerraShort.png"
          style="max-width: 80%"
          class="d-lg-none"
          :alt="$t('header.logo_terra')"
          :title="$t('header.logo_terra')"
          :aria-label="$t('header.logo_terra')"
          tabindex="0" />
      </CHeaderNavItem>
    </CHeaderNav>

    <CHeaderNav tabindex="-1">
      <CHeaderNavItem tabindex="-1">
        <CImg
          src="../img/LogoSTSP.png"
          style="max-width: 90%"
          class="d-md-down-none mr-3"
          :alt="$t('header.logo_statistica_sp')"
          :title="$t('header.logo_statistica_sp')"
          :aria-label="$t('header.logo_statistica_sp')"
          tabindex="0" />
        <CImg
          src="../img/LogoSTSP.png"
          style="max-width: 80%"
          class="d-lg-none"
          :alt="$t('header.logo_statistica_sp')"
          :title="$t('header.logo_statistica_sp')"
          :aria-label="$t('header.logo_statistica_sp')"
          tabindex="0" />
        <CButtonGroup
          role="group"
          class="mr-lang"
          aria-label="$t('common.select_language')">
          <CButton
            color="primary"
            variant="ghost"
            square
            size="sm"
            :class="{ active: selectedIt }"
            @click="selectLanguage('it')"
            @keypress="selectLanguage('it')"
            :aria-label="$t('common.language_it')"
            :title="$t('common.language_it')"
            tabindex="0"
            >IT</CButton
          >
          <CButton
            color="primary"
            variant="ghost"
            square
            size="sm"
            :class="{ active: selectedEn }"
            @click="selectLanguage('en')"
            @keypress="selectLanguage('en')"
            :aria-label="$t('common.language_en')"
            :title="$t('common.language_en')"
            tabindex="0"
            >EN</CButton
          >
        </CButtonGroup>
      </CHeaderNavItem>
    </CHeaderNav>
  </CHeader>
</template>

<script>
import { mapGetters } from "vuex"

export default {
  data() {
    return {
      currentState: false,
      langs: ["it", "en"],
      selectedIt: false,
      selectedEn: false
    }
  },
  computed: {
    ...mapGetters("metadata", ["lastLoadedData"]),
    ...mapGetters("coreui", ["isItalian", "sidebarShow"])
  },
  methods: {
    selectLanguage(lan) {
      this.$i18n.locale = lan
      this.selectedIt = lan == "it" ? true : false
      this.selectedEn = lan == "en" ? true : false
      //update page language
      const html = document.documentElement
      html.setAttribute("lang", lan)
      //store language
      this.$store.dispatch("coreui/setLanguage", lan)
    }
  },
  created() {
    this.selectedIt = this.isItalian
    this.selectedEn = !this.isItalian
    this.currentState = !this.currentState
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
.dropdown-item a:hover {
  color: #321fdb;
  text-decoration: none;
}
.dropdown-item.active,
.dropdown-item:active {
  text-decoration: none;
  color: #321fdb;
  background-color: #fff;
}
.dropdown-item:hover {
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
