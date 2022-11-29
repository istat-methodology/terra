<template>
  <div class="row w-100 justify-content-center mt-3">
    <div class="col-6">
      <div class="clearfix">
        <h1 class="float-left display-3 mr-4">500</h1>
        <h4 class="pt-3">{{ $t("common.error.main") }}</h4>
        <p class="text-muted">
          {{ $t("common.error.txt") }}
        </p>
      </div>
      <div class="clearfix mb-3">
        <h4 class="pt-3">{{ $t("common.error.error") }}</h4>
        <p class="text-muted">{{ msg }}</p>
      </div>
      <div class="clearfix mb-3">
        <router-link tag="a" to="/">
          <CIcon name="cilHome"></CIcon>
          <span>&nbsp;{{ $t("common.error.goHome") }}</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"

export default {
  name: "Error",
  computed: {
    ...mapGetters("error", ["msg"])
  }
}
</script>
