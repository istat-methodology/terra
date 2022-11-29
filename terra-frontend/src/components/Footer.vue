<template>
  <CFooter :fixed="false">
    <div>
      <span class="mr-1 text-dark"
        ><a href="https://www.terra.statlab.it" target="_blank"
          >TERRA <span class="acronym"> - {{ $t("common.acronym") }}</span></a
        >
      </span>
    </div>
    <div class="ml-auto">
      <span class="mr-1 d-md-down-none">{{ $t("common.footer.source") }}</span>
      <a href="http://epp.eurostat.ec.europa.eu/newxtweb/" target="_blank"
        >EUROSTAT COMEXT</a
      >
    </div>
  </CFooter>
</template>
