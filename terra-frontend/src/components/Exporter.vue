<template>
  <div>
    <span v-if="iam == null">
      <div class="dropdown" :title="$t('common.exporter')">
        <button
          class="btn btn-outline dropdown-toggle"
          type="button"
          :aria-label="$t('common.exporter')"
          data-toggle="dropdown"
          :aria-expanded="toggle ? 'false' : 'true'"
          v-click-outside="dropdownClose"
          @click="dropdownToggle">
          {{ $t("common.exporter") }}
        </button>
        <span :class="toggle ? 'dropdown-menu-hide' : 'dropdown-menu-show'">
          <a
            v-for="item in options"
            :key="item"
            :title="getTitle(item)"
            class="dropdown-item"
            @click="download(item)"
            @keypress="download(item)"
            tabindex="0"
            >{{ item }}</a
          >
        </span>
      </div>
    </span>
    <a
      class="control-btn exporter block"
      role="button"
      :title="getTitle('csv')"
      v-if="iam == 'map'"
      @click="download('csv')"
      @keypress="download(item)"
      ><strong>D</strong></a
    >
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import jsPDF from "jspdf"
import html2canvas from "html2canvas"
import { saveAs } from "file-saver"

import Vue from "vue"
Vue.directive("click-outside", {
  bind(el, binding, vnode) {
    el.clickOutsideEvent = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        vnode.context[binding.expression](event)
      }
    }
    document.body.addEventListener("click", el.clickOutsideEvent)
  },
  unbind(el) {
    document.body.removeEventListener("click", el.clickOutsideEvent)
  }
})

export default {
  name: "exporter",
  computed: {
    ...mapGetters("classification", ["getCountryName"])
  },
  props: {
    filename: {
      Type: String,
      default: () => ""
    },
    data: {
      Type: Array,
      default: () => []
    },
    fields: {
      Type: Array,
      default: () => []
    },
    header: {
      Type: Array,
      default: () => null
    },
    filter: {
      Type: Array,
      default: () => null
    },
    options: {
      Type: Array,
      default: () => ["jpeg", "png", "pdf", "json", "csv"]
    },
    source: {
      Type: String,
      default: () => ""
    },
    timePeriod: {
      Type: Array,
      default: () => null
    },
    iam: {
      Type: String,
      default: () => null,
      required: false
    },
    nodes: {
      Type: Array,
      default: () => null
    },
    edges: {
      Type: Array,
      default: () => null
    }
  },
  data: () => ({
    toggle: true
  }),
  methods: {
    getTitle(typeformat) {
      return "Download " + typeformat
    },
    download(type) {
      switch (type) {
        case "json":
          this.toJSON(this.data[0], this.filename + "." + type)
          break
        case "csv":
          this.toCSV(this.data[0], this.filename + "." + type)
          break
        case "jpeg":
          this.toJPEG(this.data[1], this.filename + "." + type)
          break
        case "png":
          this.toPNG(this.data[1], this.filename + "." + type)
          break
        case "pdf":
          this.toPDF(this.data[1], this.filename + "." + type)
          break

        default:
          break
      }
    },
    toBody(id) {
      html2canvas(this.getCanvas(id), { useCORS: true }).then((canvas) => {
        document.body.appendChild(canvas)
      })
    },
    toJSON(data, filename) {
      var jsonData = {}
      if (this.source == "graph") {
        jsonData = data
      } else {
        let dat = []
        for (let i = 0; i < data.datasets.length; i++) {
          let obj = {}
          obj[data.datasets[i].label] = data.datasets[i].data
          dat.push(obj)
        }
        jsonData = JSON.stringify(dat)
      }
      const blob = new Blob([jsonData], { type: "text/plain" })
      saveAs(blob, filename)
    },

    toCSV(data, filename) {
      const columnDelimiter = ";"
      const rowDelimiter = "\n"
      let result = ""
      let row = ""
      if (data) {
        if (this.source == "table") {
          const cols = Object.keys(data[0])
          const lenCols = Object.keys(data[0]).length

          if (this.filter) {
            this.filter.forEach((row) => {
              let ln = ""
              for (const col in row) {
                ln += row[col]
                ln += columnDelimiter
              }
              result += ln.slice(0, -1) //remove last column delimiter
              //add column delimiters
              if (lenCols > 1)
                result += Array(lenCols - 1)
                  .fill("")
                  .join(columnDelimiter)
              result += rowDelimiter
            })
            //add empty row
            result += Array(lenCols).fill("").join(columnDelimiter)
            result += rowDelimiter
          }
          if (this.header) {
            row = ""
            this.header.forEach((obj) => {
              row += obj
              row += columnDelimiter
            })
            result += row.slice(0, -1) //remove last column delimiter
            result += rowDelimiter
          }

          //const cols = Object.keys(data[0]) //get keys from first element
          data.forEach((obj) => {
            row = ""
            cols.forEach((col) => {
              //if (this.fields != col) {
              row += obj[col]
              row += columnDelimiter
              //}
            })
            result += row.slice(0, -1) //remove last column delimiter
            result += rowDelimiter
          })
        } else if (this.source == "map") {
          const cols = Object.keys(data[0]) //get keys from first element
          //header map data
          row = ""
          row += "country name"
          row += columnDelimiter
          cols.forEach((col) => {
            row += col
            row += columnDelimiter
          })
          result += row.slice(0, -1) //remove last column delimiter
          result += rowDelimiter

          data.forEach((obj) => {
            row = ""
            //name
            row += this.getCountryName(obj["country"])
            row += columnDelimiter
            cols.forEach((col) => {
              //if (this.fields != col) {
              row += obj[col]
              row += columnDelimiter
              //}
            })
            result += row.slice(0, -1) //remove last column delimiter
            result += rowDelimiter
          })
        } else if (this.source == "graph") {
          row = ""
          row = "Terra - Graph"
          row += columnDelimiter
          result += row.slice(0, -1) //remove last column delimiter
          result += rowDelimiter

          row = ""
          row = "edges"
          row += columnDelimiter
          result += row.slice(0, -1) //remove last column delimiter
          result += rowDelimiter

          row = ""
          row += "from"
          row += columnDelimiter
          row += "to"
          row += columnDelimiter
          result += row.slice(0, -1) //remove last column delimiter
          result += rowDelimiter

          for (var edgeId in this.edges) {
            row = ""
            row += this.edges[edgeId].from
            row += columnDelimiter
            row += this.edges[edgeId].to

            row += columnDelimiter
            result += row.slice(0, -1) //remove last column delimiter
            result += rowDelimiter
          }

          row = ""
          row = "nodes"
          row += columnDelimiter
          result += row.slice(0, -1) //remove last column delimiter
          result += rowDelimiter

          row = ""
          row += "id"
          row += columnDelimiter
          row += "country"
          row += columnDelimiter
          row += "x"
          row += columnDelimiter
          row += "y"
          row += columnDelimiter
          result += row.slice(0, -1) //remove last column delimiter
          result += rowDelimiter

          for (var nodeId in this.nodes) {
            row = ""
            row += this.nodes[nodeId].id
            row += columnDelimiter
            row += this.nodes[nodeId].label
            row += columnDelimiter
            row += this.nodes[nodeId].x
            row += columnDelimiter
            row += this.nodes[nodeId].y
            row += columnDelimiter
            result += row.slice(0, -1) //remove last column delimiter
            result += rowDelimiter
          }
        } else if (this.source == "matrix") {
          const obj = {}
          //Add filters
          if (this.filter) {
            this.filter.forEach((row) => {
              let ln = ""
              for (const col in row) {
                ln += row[col]
                ln += columnDelimiter
              }
              result += ln.slice(0, -1) //remove last column delimiter
              //add column delimiters
              result += Array(data.length).fill("").join(columnDelimiter)
              result += rowDelimiter
            })
          }
          //Add empty row
          result += Array(data.length + 1)
            .fill("")
            .join(columnDelimiter)
          result += rowDelimiter

          if (this.timePeriod)
            obj["time"] = this.timePeriod.map((t) => {
              return t.isoDate
            })
          data.forEach((col) => {
            obj[col.dataname.replaceAll(";", ",")] = col.value //replace ; with , in product label
          })
          const cols = Object.keys(obj)
          result += cols.join(columnDelimiter)
          result += rowDelimiter
          for (var idx = 0; idx < obj[Object.keys(obj)[0]].length; idx++) {
            row = ""
            cols.forEach((col) => {
              row += obj[col][idx]
              row += columnDelimiter
            })
            result += row.slice(0, -1).replaceAll(".", ",") //remove last column delimiter and change decimal separator
            result += rowDelimiter
          }
        } else {
          data.datasets.forEach((dataset) => {
            const rows = dataset.data
            const cols = Object.keys(rows[0])
            result += dataset.label.replaceAll(";", ",") //replace ; with , in product label
            if (cols.length > 0) {
              result += rowDelimiter
              result += cols.join(columnDelimiter)
              result += rowDelimiter
              rows.forEach((obj) => {
                row = ""
                cols.forEach((key) => {
                  row += obj[key]
                  row += columnDelimiter
                })
                result += row.slice(0, -1) //remove last column delimiter
                result += rowDelimiter
              })
            } else {
              rows.forEach((el) => {
                result += columnDelimiter
                result += el
              })
              result += rowDelimiter
            }
          })
        }
      }
      const blob = new Blob([result], { type: "text/plain" })
      saveAs(blob, filename)
    },
    toJPEG(id, filename) {
      html2canvas(this.getCanvas(id), {
        useCORS: true
      }).then((canvas) => {
        const imgData = canvas.toDataURL("image/jpeg", 1.0)
        saveAs(imgData, filename)
      })
    },
    toPNG(id, filename) {
      html2canvas(this.getCanvas(id), {
        useCORS: true
      }).then((canvas) => {
        const imgData = canvas.toDataURL("image/png")
        saveAs(imgData, filename)
      })
    },
    toPDF(id, filename) {
      let pdf = new jsPDF("l", "px")
      html2canvas(this.getCanvas(id), {
        useCORS: true
      }).then((canvas) => {
        const imgData = canvas.toDataURL("image/png")
        const pageWidth = pdf.internal.pageSize.getWidth()
        const pageHeight = pdf.internal.pageSize.getHeight()
        const ratio = (pageWidth - 40) / canvas.width
        const canvasWidth = canvas.width * ratio
        const canvasHeight = canvas.height * ratio
        const marginX = (pageWidth - canvasWidth) / 2
        const marginY = (pageHeight - canvasHeight) / 2
        pdf.text(filename, 20, 20)
        pdf.addImage(
          imgData,
          "JPEG",
          marginX,
          marginY,
          canvasWidth,
          canvasHeight
        )
        pdf.save(filename)
      })
    },
    getCanvas(id) {
      return this.source == "graph"
        ? document.getElementById(id).querySelector("canvas")
        : document.getElementById(id)
    },
    dropdownToggle() {
      this.toggle = !this.toggle
    },
    dropdownClose() {
      this.toggle = true
    }
  }
}
</script>
<style>
.block {
  display: block;
  position: static;
}
.dropdown-toggle {
  cursor: pointer !important;
  color: #321fdb !important;
  text-decoration: underline !important;
}
.dropdown-toggle:hover {
  text-decoration: underline !important;
  color: #231698;
}

.dropdown-menu-show {
  position: absolute;
  top: 120%;
  z-index: 1000;
  float: left;
  min-width: 6.6rem;
  padding: 0.5rem 0;
  font-size: 0.875rem;
  text-align: left;
  list-style: none;
  background-clip: padding-box;
  border: 1px solid;
  border-radius: 0.25rem;
  color: #3c4b64;
  background-color: #fff;
  border-color: #d8dbe0;
  left: 0;
}
.dropdown-menu-show:focus {
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(50, 31, 219, 0.25);
}

.dropdown-menu-hide {
  display: none;
}
.dropdown-item.active,
.dropdown-item:active {
  text-decoration: none !important;
  color: #321fdb !important;
  background-color: #d8dbe0 !important;
}
.dropdown-item:hover {
  cursor: pointer;
}
.icon-size {
  font-size: 1.5em;
}
</style>
