<template lang="pug">
  v-col(cols="12")
    v-text-field(
      dense
      v-model="bank"
      label="Наименование банка"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    bank: {
      set (bank) {
        this.$store.commit('contragents/SET_CONTRAGENT', { bank })
      },
      get () {
        return this.$store.state.contragents.detail.bank
      }
    }
  }
}
</script>
