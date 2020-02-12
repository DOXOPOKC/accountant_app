<template lang="pug">
  v-col(cols="12")
    v-select(
      disabled
      item-text="name"
      item-value="id"
      v-model="norm_value"
      :items="classTypes"
      label="Норматив"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    norm_value: {
      set (normValue) {
        this.$store.commit('contragents/SET_CONTRAGENT', { norm_value: normValue })
      },
      get () {
        return this.$store.state.contragents.detail.norm_value
      }
    }
  }
}
// dropdown
// endpoint : http://localhost/api/norms/ { id: 1, name: "string" }
</script>
