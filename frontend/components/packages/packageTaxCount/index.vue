<template lang="pug">
  v-col(cols="12")
    v-text-field(
      dense
      v-model.number="taxCount"
      label="Гос. пошлина"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    taxCount: {
      set (taxCount) {
        this.$store.commit('packages/SET_TAX', taxCount)
      },
      get () {
        return this.$store.state.packages.detail.tax_count
      }
    }
  }
}
</script>
