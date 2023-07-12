<template>
  <CFooter :fixed="false" tabindex="-1" role="contentinfo">
    <div>
      <span class="mr-1 text-dark">
        <a
          href="https://ec.europa.eu/eurostat/comext/newxtweb/"
          target="_blank"
          aria-label="EUROSTAT COMEXT"
          tabindex="0"
          >EUROSTAT COMEXT</a
        >
      </span>
    </div>
    <div class="ml-auto center">
      <p class="section-link">
        <router-link tag="a" :to="{ name: 'Privacy' }"> Privacy </router-link>
        <router-link tag="a" :to="{ name: 'Privacy' }">
          Accessibility
        </router-link>
      </p>
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
