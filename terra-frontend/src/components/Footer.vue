<template>
  <CFooter :fixed="false" tabindex="-1">
    <span class="ml-3 float-left">
      <a
        class="d-inline"
        href="https://ec.europa.eu/eurostat/comext/newxtweb/"
        target="_blank"
        tabindex="0"
        title="EUROSTAT COMEXT"
        :aria_label="$t('footer.opens_goto_eurostat')">
        EUROSTAT COMEXT</a
      >
    </span>
    <span class="ml-auto float-center">
      <a
        class="d-inline"
        @click="handlePrivacy()"
        @keypress="handlePrivacy()"
        tabindex="0"
        title="Privacy"
        >Privacy</a
      ><span class="ml-2 mr-2"><strong>/</strong></span>
      <a
        class="d-inline"
        target="_blank"
        href="https://form.agid.gov.it/view/848a565e-df60-43d3-93b4-325c4d995ec3"
        tabindex="0"
        :title="$t('footer.link_accessibility')"
        :aria_label="$t('footer.opens_goto_accessibility')">
        {{ $t("footer.link_accessibility") }}
      </a>
    </span>
    <span class="ml-auto mr-3 float-right">
      <a
        class="d-inline"
        target="_blank"
        :href="$t('common.footer.user_manual')"
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
  text-decoration: underline !important;
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
