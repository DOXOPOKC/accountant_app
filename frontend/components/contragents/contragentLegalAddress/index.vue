<template lang="pug">
  v-col(cols="12")
    v-textarea(
      readonly
      auto-grow
      rows="1"
      v-model="legalAddress"
      label="Юридический адрес"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    legalAddress: {
      set (legalAddress) {
        this.$store.commit('contragents/SET_CONTRAGENT', { legal_address: legalAddress })
      },
      get () {
        return this.$store.state.contragents.detail.legal_address
      }
    }
  }
}
// disabled
</script>
