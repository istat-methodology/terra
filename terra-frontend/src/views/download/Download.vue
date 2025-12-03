<template>
  <div class="download-page">
    <h1 class="page-title">Download dati</h1>

    <div class="filters-container">
      <div class="filters-column">
        <div class="form-group">
          <label for="serie">Serie</label>
          <select id="serie" v-model="filters.serie">
            <option
              v-for="opt in options.serie"
              :key="opt.value"
              :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="tipoDati">Tipo dati</label>
          <select id="tipoDati" v-model="filters.tipoDati">
            <option
              v-for="opt in options.tipoDati"
              :key="opt.value"
              :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="flusso">Flusso</label>
          <select id="flusso" v-model="filters.flusso">
            <option
              v-for="opt in options.flusso"
              :key="opt.value"
              :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="paese">Paese</label>
          <select id="paese" v-model="filters.paese">
            <option
              v-for="opt in options.paesi"
              :key="opt.value"
              :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>
      </div>

      <div class="filters-column">
        <div class="form-group">
          <label for="partner">Partner</label>
          <select id="partner" v-model="filters.partner">
            <option
              v-for="opt in options.partner"
              :key="opt.value"
              :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="prodotto">Prodotti CPA 2.1</label>
          <select id="prodotto" v-model="filters.prodotto">
            <option
              v-for="opt in options.prodotti"
              :key="opt.value"
              :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>

        <div class="form-group form-group-inline">
          <div>
            <label for="periodoDa">Periodo da</label>
            <input id="periodoDa" v-model="filters.periodoDa" type="month" />
          </div>
          <div>
            <label for="periodoA">Periodo a</label>
            <input id="periodoA" v-model="filters.periodoA" type="month" />
          </div>
        </div>

        <div class="form-group">
          <label>Formato file</label>
          <div class="radio-group">
            <label>
              <input type="radio" value="csv" v-model="filters.formato" />
              CSV
            </label>
            <label>
              <input type="radio" value="xlsx" v-model="filters.formato" />
              Excel (XLSX)
            </label>
            <label>
              <input type="radio" value="json" v-model="filters.formato" />
              JSON
            </label>
          </div>
        </div>
      </div>
    </div>

    <div class="actions">
      <button class="btn secondary" @click="resetFilters">Reset filtri</button>
      <button class="btn primary" :disabled="isDownloading" @click="download">
        <span v-if="!isDownloading">Scarica dati</span>
        <span v-else>Preparazione download...</span>
      </button>
    </div>

    <p v-if="errorMessage" class="message error">{{ errorMessage }}</p>
    <p v-if="successMessage" class="message success">{{ successMessage }}</p>
  </div>
</template>

<script>
export default {
  name: "DownloadPage",
  data() {
    return {
      isDownloading: false,
      errorMessage: "",
      successMessage: "",
      filters: {
        serie: "diff12",
        tipoDati: "euro",
        flusso: "import",
        paese: "italia",
        partner: "tutti",
        prodotto: "tutti",
        periodoDa: "",
        periodoA: "",
        formato: "csv"
      },
      options: {
        serie: [
          { value: "diff12", label: "Serie delle differenze a 12 mesi" },
          { value: "livelli", label: "Livelli mensili" }
        ],
        tipoDati: [
          { value: "euro", label: "Euro" },
          { value: "kg", label: "Chilogrammi" },
          { value: "indice", label: "Indice" }
        ],
        flusso: [
          { value: "import", label: "Import" },
          { value: "export", label: "Export" }
        ],
        paesi: [
          { value: "italia", label: "Italia" },
          { value: "ue27", label: "UE27" },
          { value: "mondo", label: "Mondo" }
        ],
        partner: [
          { value: "tutti", label: "Tutti i paesi" },
          { value: "ue27", label: "UE27" },
          { value: "extraue", label: "Extra UE" }
        ],
        prodotti: [
          { value: "tutti", label: "00 - Tutti i prodotti" },
          { value: "01", label: "01 - Prodotti agricoli" },
          { value: "02", label: "02 - Prodotti manifatturieri" }
        ]
      }
    }
  },
  methods: {
    resetFilters() {
      this.filters.periodoDa = ""
      this.filters.periodoA = ""
      this.filters.formato = "csv"
      this.successMessage = ""
      this.errorMessage = ""
    },
    buildQuery() {
      const params = new URLSearchParams()
      Object.entries(this.filters).forEach(([k, v]) => {
        if (v !== "" && v != null) {
          params.append(k, v)
        }
      })
      return params.toString()
    },
    async download() {
      this.errorMessage = ""
      this.successMessage = ""
      this.isDownloading = true

      try {
        const queryString = this.buildQuery()
        const url = `/api/download?${queryString}`

        console.log("Chiamata download:", url)

        this.successMessage = "Richiesta di download inviata con successo."
      } catch (err) {
        this.errorMessage =
          "Si è verificato un errore durante la preparazione del download."
      } finally {
        this.isDownloading = false
      }
    }
  }
}
</script>

<style scoped>
.download-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem 2rem 3rem;
}

.page-title {
  font-size: 1.7rem;
  margin-bottom: 1.5rem;
}

.filters-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  background: #ffffff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.filters-column {
  flex: 1 1 280px;
  min-width: 260px;
}

.form-group {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
}

.form-group-inline {
  display: flex;
  gap: 1rem;
}

.form-group label {
  font-size: 0.9rem;
  margin-bottom: 0.3rem;
}

select,
input[type="month"] {
  padding: 0.45rem 0.6rem;
  border-radius: 4px;
  border: 1px solid #cccccc;
  font-size: 0.9rem;
}

.radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.9rem;
}

.actions {
  margin-top: 1.5rem;
  display: flex;
  gap: 0.8rem;
  justify-content: flex-end;
}

.btn {
  border: none;
  border-radius: 4px;
  padding: 0.55rem 1rem;
  font-size: 0.9rem;
  cursor: pointer;
}

.btn.primary {
  background-color: #0053a6;
  color: white;
}

.btn.primary:disabled {
  opacity: 0.7;
  cursor: default;
}

.btn.secondary {
  background-color: #eeeeee;
}

.message {
  margin-top: 1rem;
  font-size: 0.9rem;
}

.message.error {
  color: #b00020;
}

.message.success {
  color: #006400;
}

@media (max-width: 768px) {
  .filters-container {
    padding: 1rem;
  }
}
</style>
