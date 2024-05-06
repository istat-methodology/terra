<template>
  <div class="row">
    <h1 class="sr-only">
      {{ $t("common.acronym") }}
    </h1>
    <div>
      <h1>Manutenzione sito in corso. Ci scusiamo per il disagio.</h1>
      <p></p>
      <h1>Website maintenance in progress.</h1>
    </div>
  </div>
</template>

<script>
import { Context } from "@/common"
export default {
  name: "Maintenance",
  data() {
    return {
      title: process.env.VUE_APP_TITLE
    }
  },
  methods: {
    fixASidebarMenu() {
      setTimeout(() => {
        document.querySelectorAll(".c-sidebar-nav-link").forEach((element) => {
          element.setAttribute("aria-current", "false")
        })
      }, 300)
      setTimeout(() => {
        document
          .querySelectorAll(".c-sidebar-nav-link.c-active")
          .forEach((element) => {
            element.setAttribute("aria-current", "page")
          })
      }, 300)
    },
    fixMetaTitle() {
      setTimeout(() => {
        document.querySelectorAll("title").forEach((element) => {
          element.textContent = "Terra - Home"
        })
      }, 300)
    }
  },
  created() {
    this.$store.dispatch("coreui/setContext", Context.Maintenance)
    this.fixMetaTitle()
    this.fixASidebarMenu()
  }
}
</script>
<style scoped>
.material-design-icon > .material-design-icon__svg {
  bottom: -0.17rem;
}
.card-body {
  padding-bottom: 0.5rem;
}
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
