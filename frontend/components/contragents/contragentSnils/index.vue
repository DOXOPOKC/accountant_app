<template lang="pug">
  v-col(cols="12")
    v-text-field(
      dense
      v-model.number="snils"
      label="Снилс"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    snils: {
      set (snils) {
        this.$store.commit('contragents/SET_CONTRAGENT', { snils })
      },
      get () {
        return this.$store.state.contragents.detail.snils
      }
    }
  }
}
</script>
