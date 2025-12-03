<template>
  <div class="row">
    <h1 class="sr-only">{{ $t("landing.download.title") }}</h1>
    <div class="col-12">
      <CCard :title="'TERRA - ' + $t('download.card.title')">
        <CCardHeader>
          <span class="card-title" role="heading" aria-level="2">
            <CIcon
              name="cil-newspaper"
              :title="$t('download.card.title')"
              alt="" />
            {{ $t("download.card.title") }}
          </span>
        </CCardHeader>
        <CCardBody>
          <div class="col-sm-6 col-md-3">
            <CCard class="card-filter" :title="$t('download.form.title')">
              <CCardHeader>
                <span class="card-filter-title" role="heading" aria-level="2">{{
                  $t("download.form.title")
                }}</span>
              </CCardHeader>
              <CCardBody>
                <CButton
                  color="primary"
                  shape="square"
                  size="sm"
                  @click="handleSubmit"
                  class="mt-2 ml-3"
                  :title="$t('common.submit')"
                  >{{ $t("common.submit") }}</CButton
                >
              </CCardBody>
            </CCard>
          </div>
          <CDataTable
            id="downloadTable"
            ref="downloadTable"
            v-if="download"
            :items="download"
            :fields="downloadFields"
            column-filter
            :items-per-page="10"
            sorter
            hover
            pagination
            @filtered-items-change="setPage()"
            @page-change="setPage()"
            :noItemsView="{
              noResults: this.$t('common.table.no_filtering_results_available'),
              noItems: this.$t('common.table.no_items_available')
            }">
            <template #id="{ item }">
              <td headers="head_0">
                {{ item.id }}
              </td>
            </template>
            <template #date="{ item }">
              <td headers="head_1">
                {{ item.date }}
              </td>
            </template>
            <template #text="{ item }">
              <td headers="head_2">
                {{ item.text }}
              </td>
            </template>
            <template #type="{ item }">
              <td headers="head_3">
                {{ item.type }}
              </td>
            </template>
          </CDataTable>
          <span class="no-visible">{{ page_number }}</span>
          <circle-spin v-if="!this.download" class="circle-spin"></circle-spin>
        </CCardBody>
      </CCard>
    </div>
  </div>
</template>
<script>
import { mapGetters } from "vuex"
import { Context } from "@/common"

import spinnerMixin from "@/components/mixins/spinner.mixin"

export default {
  name: "download",
  components: {},
  mixins: [spinnerMixin],
  data() {
    return {
      page_number: 0,
      //Spinner
      spinner: false
    }
  },
  watch: {
    language() {
      this.$store.dispatch("message/success", this.$t("common.update_cls"))
      this.$store.dispatch("classification/getClassifications").then(() => {
        this.fixLanguageAccessibility()
        this.$store.dispatch("download/findAll").then(() => {
          this.fixHeaderTableForAccessibility()
          this.spinnerStart(false)
        })
      })
    }
  },
  computed: {
    ...mapGetters("coreui", ["language"]),
    ...mapGetters("download", ["download"]),
    downloadFields() {
      return [
        {
          key: "date",
          label: this.$t("download.table.date"),
          _style: "width:15%;"
        },
        {
          key: "text",
          label: this.$t("download.table.text"),
          _style: "width:70%;"
        },
        {
          key: "type",
          label: this.$t("download.table.type"),
          _style: "width:15%;"
        }
      ]
    }
  },
  methods: {
    spinnerStart(bool) {
      this.spinner = bool
    },
    fixLanguageAccessibility() {
      setTimeout(() => {
        document.querySelectorAll(".vs__clear ").forEach((element) => {
          element.setAttribute("title", this.$t("common.clear_selected"))
          element.setAttribute("aria-label", this.$t("common.clear_selected"))
        })
        document.querySelectorAll(".vs__deselect").forEach((element) => {
          element.setAttribute("title", this.$t("common.clear_selected"))
          element.setAttribute("aria-label", this.$t("common.clear_selected"))
        })
      }, 300)
    },
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
          element.textContent = "Terra - " + this.$t("landing.download.title")
        })
      }, 300)
    },
    fixSortingTable() {
      if (this.$refs.downloadTable) {
        const table = this.$refs.downloadTable
        if (table.$el.children[0].children[0].children[0].children) {
          const thead = table.$el.children[0].children[0].children[0].children

          if (thead[0].children && thead[1].children) {
            const tr_0 = thead[0].children
            const tr_1 = thead[1].children
            //console.log(tr_0.length - 1)
            const tr_len = tr_0.length - 1
            if (tr_0) {
              for (let i = 0; i <= tr_len; i++) {
                if (tr_0[i].children[1]) {
                  tr_0[i].children[1].ariaLabel =
                    this.$t("common.table.order_field") + tr_0[i].innerText
                  tr_0[i].children[1].role = "button"
                }
                if (tr_0[i].children[0]) {
                  tr_1[i].children[0].ariaLabel =
                    this.$t("common.table.search_field") + tr_0[i].innerText
                  tr_1[i].children[0].title =
                    this.$t("common.table.search_field") + tr_0[i].innerText
                }
              }
            }
          }
        }
      }
    },
    fixBodyTable() {
      if (this.$refs.downloadTable) {
        const table = this.$refs.downloadTable
        const tBody = table.$el.children[0].children[0].children[1]
        tBody.ariaLive = "polite"
        if (tBody.children[0].children[0].children[0]) {
          if (
            tBody.children[0].children[0].children[0].className ==
            "text-center my-5"
          ) {
            tBody.children[0].children[0].children[0].role = "alert"
            //console.log(tBody.children[0].children[0].children[0].role)
          }
        }
      }
    },
    fixNavTable() {
      if (this.$refs.downloadTable) {
        const table = this.$refs.downloadTable
        if (table.$el.children[1]) {
          const nav = table.$el.children[1]
          nav.ariaLabel = this.$t("common.table.pagination")
          if (nav.children[0].children) {
            let nav_buttons = nav.children[0].children
            const next_button = nav_buttons.length - 2
            const last_button = nav_buttons.length - 1
            nav_buttons[0].children[0].ariaLabel = this.$t(
              "common.table.go_to_first_page"
            )
            nav_buttons[0].children[0].title = this.$t(
              "common.table.go_to_first_page"
            )
            nav_buttons[1].children[0].ariaLabel = this.$t(
              "common.table.go_to_previous_page"
            )
            nav_buttons[1].children[0].title = this.$t(
              "common.table.go_to_previous_page"
            )
            nav_buttons[next_button].children[0].ariaLabel = this.$t(
              "common.table.go_to_next_page"
            )
            nav_buttons[next_button].children[0].title = this.$t(
              "common.table.go_to_next_page"
            )
            nav_buttons[last_button].children[0].ariaLabel = this.$t(
              "common.table.go_to_last_page"
            )
            nav_buttons[last_button].children[0].title = this.$t(
              "common.table.go_to_last_page"
            )
            for (let i = 2; i <= nav_buttons.length - 3; i++) {
              if (nav_buttons[i].className == "active page-item") {
                nav_buttons[i].children[0].ariaLabel =
                  this.$t("common.table.current_page") +
                  nav_buttons[i].children[0].innerText
                nav_buttons[i].children[0].title =
                  this.$t("common.table.current_page") +
                  nav_buttons[i].children[0].innerText
              } else {
                nav_buttons[i].children[0].ariaLabel =
                  this.$t("common.table.go_to_page") +
                  nav_buttons[i].children[0].innerText
                nav_buttons[i].children[0].title =
                  this.$t("common.table.go_to_page") +
                  nav_buttons[i].children[0].innerText
              }
            }
          }
        }
      }
    },
    setPage() {
      if (this.page_number > 10) this.page_number = 0
      this.page_number = this.page_number + 1
    },
    fixHeaderTableForAccessibility() {
      setTimeout(() => {
        var thead = document
          .getElementById("downloadTable")
          .querySelector("thead > tr")
        thead.querySelectorAll("th").forEach((element, index) => {
          element.setAttribute("id", "head_" + index)
          element.setAttribute("title", element.innerText)
          element.setAttribute("aria-label", element.innerText)
        })
      }, 300)
    }
  },
  mounted() {
    this.fixSortingTable()
    this.fixNavTable()
    this.fixBodyTable()
    this.fixASidebarMenu()
  },
  updated() {
    this.fixSortingTable()
    this.fixNavTable()
    this.fixBodyTable()
    this.fixASidebarMenu()
  },
  created() {
    this.spinnerStart(true)
    this.$store.dispatch("coreui/setContext", Context.download)
    this.fixMetaTitle()
    this.$store.dispatch("download/findAll").then(() => {
      this.fixHeaderTableForAccessibility()
      this.spinnerStart(false)
    })
  }
}
</script>
<style scoped>
.card-body {
  padding: 0.2rem 1.25rem;
}

.no-visible {
  display: none;
}
</style>
