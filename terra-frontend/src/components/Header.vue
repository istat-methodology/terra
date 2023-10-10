<template>
  <CHeader with-subheader light>
    <CToggler
      in-header
      class="ml-3 d-lg-none"
      @click="handleSidebarMobile"
      @keypress="handleSidebarMobile"
      :aria-label="
        sidebarShow === false ? $t('header.toggler') : $t('header.no_toggler')
      "
      :title="
        sidebarShow === false ? $t('header.toggler') : $t('header.no_toggler')
      "
      tabindex="0" />
    <CToggler
      in-header
      class="ml-3 d-md-down-none"
      @click="handleSidebarDesktop"
      @keypress="handleSidebarDesktop"
      :aria-label="
        sidebarShow === false ? $t('header.toggler') : $t('header.no_toggler')
      "
      :title="
        sidebarShow === false ? $t('header.toggler') : $t('header.no_toggler')
      "
      tabindex="0" />

    <CHeaderNav class="mr-auto" tabindex="-1">
      <CHeaderNavItem tabindex="-1">
        <CImg
          src="../img/LogoTerraFull.png"
          style="max-width: 70%"
          class="d-md-down-none"
          :alt="$t('header.logo_terra')"
          :title="$t('header.logo_terra')"
          :aria-label="$t('header.logo_terra')"
          tabindex="-1" />
        <CImg
          src="../img/LogoTerraShort.png"
          style="max-width: 80%"
          class="d-lg-none"
          :alt="$t('header.logo_terra')"
          :title="$t('header.logo_terra')"
          :aria-label="$t('header.logo_terra')"
          tabindex="-1" />
      </CHeaderNavItem>
    </CHeaderNav>

    <CHeaderNav tabindex="-1">
      <CHeaderNavItem tabindex="-1">
        <CImg
          src="../img/LogoSTSP.png"
          style="max-width: 50%"
          class="d-md-down-none mr-3"
          :alt="$t('header.logo_statistica_sp')"
          :title="$t('header.logo_statistica_sp')"
          :aria-label="$t('header.logo_statistica_sp')"
          tabindex="-1" />
        <CImg
          src="../img/LogoSTSP.png"
          style="max-width: 50%"
          class="d-lg-none"
          :alt="$t('header.logo_statistica_sp')"
          :title="$t('header.logo_statistica_sp')"
          :aria-label="$t('header.logo_statistica_sp')"
          tabindex="0" />
        <CButtonGroup role="group" class="mr-lang">
          <CButton
            color="primary"
            variant="ghost"
            square
            size="sm"
            :class="{ active: selectedIt }"
            @click="selectLanguage('it')"
            @keypress="selectLanguage('it')"
            :aria-label="
              $t('common.select_language') + $t('common.language_it')
            "
            :title="$t('common.select_language') + $t('common.language_it')"
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
            :aria-label="
              $t('common.select_language') + $t('common.language_en')
            "
            :title="$t('common.select_language') + $t('common.language_en')"
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
    },
    fixHeaderTableForAccessibility() {
      setTimeout(() => {
        document.querySelectorAll("th").forEach((element) => {
          element.setAttribute("title", element.innerText)
          element.setAttribute("aria-label", element.innerText)
        })
      }, 300)
    },
    handleSidebarDesktop() {
      this.$store.dispatch("coreui/toggleSidebarDesktop")
    },
    handleSidebarMobile() {
      this.$store.dispatch("coreui/toggleSidebarMobile")
    }
  },
  created() {
    this.selectedIt = this.isItalian
    this.selectedEn = !this.isItalian
    this.currentState = !this.currentState
    //this.fixHeaderTableForAccessibility()
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
  padding-left: 0.1rem;
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
  margin-right: 0rem;
  margin-left: 0.6rem;
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
.c-header .c-header-toggler {
  margin-top: 15px;
  margin-right: 5px;
  padding: 5px;
  max-height: 40px;
  max-width: 40px;
  border-radius: 0.2rem;
}
.c-header .c-header-toggler:focus {
  box-shadow: 0 0 0 0.2rem rgba(81, 65, 224, 0.5);
  margin-top: 15px;
  margin-right: 5px;
  padding: 5px;
  max-height: 40px;
  max-width: 40px;
  border-radius: 0.2rem;
}
</style>
