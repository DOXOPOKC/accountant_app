<template lang="pug">
  v-col(cols="2")
    v-text-field(
      v-model="number_contract"
      label="Номер контракта"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    number_contract: {
      set (numberContract) {
        this.$store.commit('contragents/SET_CONTRAGENT', { number_contract: numberContract })
      },
      get () {
        return this.$store.state.contragents.detail.number_contract
      }
    }
  }
}
</script>
