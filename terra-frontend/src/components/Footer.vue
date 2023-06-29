<template>
  <CFooter :fixed="false" tabindex="-1" role="contentinfo">
    <div>
      <span class="mr-1 text-dark"
        ><a
          href="https://www.terra.statlab.it"
          target="_blank"
          :aria-label="$t('common.acronym')"
          tabindex="0">
          <span class="acronym d-md-down-none">
            {{ $t("common.acronym") }}</span
          ></a
        >
      </span>
    </div>
    <div class="ml-auto">
      <span class="mr-1 d-md-down-none">{{ $t("common.footer.source") }}</span>
      <a
        href="http://epp.eurostat.ec.europa.eu/newxtweb/"
        target="_blank"
        aria-label="EUROSTAT COMEXT"
        tabindex="0"
        >EUROSTAT COMEXT</a
      >
    </div>
    <div class="ml-auto">
      <a
        target="_blank"
        :aria-label="$t('header.userguide')"
        href="https://istatcosmostorage.blob.core.windows.net/public/Terra_Manuale.pdf"
        tabindex="0">
        {{ $t("header.userguide") }}
      </a>
    </div>
  </CFooter>
</template>

<style scoped>
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
