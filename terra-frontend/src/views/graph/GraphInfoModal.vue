<template>
  <CModal
    :aria-label="
      isMainModal
        ? $t('graph.modal.main.title')
        : $t('graph.modal.filter.title')
    "
    :title="
      isMainModal
        ? $t('graph.modal.main.title')
        : $t('graph.modal.filter.title')
    "
    :show="isHelpModal"
    @update:show="closeModal"
    size="lg"
    tabindex="0">
    <p
      v-html="
        isMainModal
          ? $t('graph.modal.main.subtitle') +
            $t('graph.modal.main.body') +
            $t('graph.modal.metrics.subtitle') +
            $t('graph.modal.metrics.body') +
            $t('graph.modal.metrics.keywords')
          : $t('graph.modal.filter.body') + $t('graph.modal.filter.keywords')
      "></p>
    <template #footer>
      <CButton
        color="primary"
        shape="square"
        size="sm"
        @click="closeModal"
        :title="$t('common.close')"
        :aria-label="$t('common.close')"
        tabindex="0"
        >{{ $t("common.close") }}</CButton
      >
    </template>
  </CModal>
</template>
<script>
export default {
  name: "GraphInfoModal",
  props: {
    isHelp: {
      type: Boolean,
      default: false
    },
    isMain: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    isHelpModal: {
      get() {
        return this.isHelp
      },
      set(value) {
        this.$emit("showHelp", value)
      }
    },
    isMainModal: {
      get() {
        return this.isMain
      },
      set(value) {
        this.$emit("showMain", value)
      }
    }
  },
  methods: {
    closeModal() {
      this.$emit("closeModal")
    }
  }
}
</script>
