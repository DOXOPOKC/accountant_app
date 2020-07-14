<template lang="pug">
  v-col(cols="12")
    v-text-field(
      dense
      v-model.number="debtPeriod"
      label="Кол-во месяцев"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    debtPeriod: {
      set (debtPeriod) {
        this.$store.commit('contragents/SET_CONTRAGENT', { debt_period: debtPeriod })
      },
      get () {
        return this.$store.state.contragents.detail.debt_period
      }
    }
  }
}
</script>
