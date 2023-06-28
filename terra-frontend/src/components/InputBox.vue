<template>
  <div class="col-4">
    <form>
      <div id="InputBox" tabindex="0">
        <label aria-labelledby="InputBox" class="col-3" tabindex="0"
          >{{ label }}
          <input
            id="InputBox"
            name="InputBox"
            type="number"
            placeholder="0"
            step="0.01"
            min="0"
            max="1"
            class="form-control"
            v-bind:value="value"
            v-on:input="$emit('input', $event.target.value)"
            tabindex="0" />
          {{ value }}
        </label>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  props: ["value", "label"]
}
</script>
