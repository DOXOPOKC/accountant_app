<template lang="pug">
  v-col(cols="12")
    v-text-field(
      disabled
      v-model="legal_address"
      label="Юридический адрес"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    legal_address: {
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
