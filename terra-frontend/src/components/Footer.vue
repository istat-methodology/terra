<template>
  <CFooter :fixed="false" tabindex="-1" role="contentinfo">
    <span class="ml-3 float-left">
      <a
        class="d-inline"
        href="https://ec.europa.eu/eurostat/comext/newxtweb/"
        target="_blank"
        aria-label="EUROSTAT COMEXT"
        tabindex="0"
        title="EUROSTAT COMEXT"
        >EUROSTAT COMEXT</a
      >
    </span>
    <span class="ml-auto float-center">
      <a
        class="d-inline"
        @click="handlePrivacy()"
        @keypress="handlePrivacy()"
        tabindex="0"
        aria-label="Privacy"
        title="Privacy"
        >Privacy</a
      ><span class="ml-2 mr-2"><strong>/</strong></span>
      <a
        class="d-inline"
        @click="handlePrivacy()"
        @keypress="handlePrivacy()"
        tabindex="0"
        aria-label="Accessibility"
        title="Accessibility"
        >Accessibility</a
      >
    </span>
    <span class="ml-auto mr-3 float-right">
      <a
        class="d-inline"
        target="_blank"
        :aria-label="$t('header.userguide')"
        href="https://istatcosmostorage.blob.core.windows.net/public/Terra_Manuale.pdf'"
        tabindex="0"
        :title="$t('header.userguide')">
        {{ $t("header.userguide") }}
      </a>
    </span>
  </CFooter>
</template>
<script>
export default {
  data() {
    return {}
  },
  methods: {
    handlePrivacy() {
      this.$router.push({ name: "Privacy" })
    }
  }
}
</script>
<style scoped>
.d-inline {
  display: inline !important;
  color: #321fdb !important;
  background-color: transparent !important;
}
.d-inline:hover {
  cursor: pointer !important ;
  display: inline !important;
  text-decoration: underline !important;
  color: #28353a !important;
  background-color: transparent !important;
}
</style>
