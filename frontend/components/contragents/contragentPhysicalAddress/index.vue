<template lang="pug">
  v-col(cols="12")
    v-text-field(
      v-model="physical_address"
      label="Фактический адрес"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    physical_address: {
      set (physicalAddress) {
        this.$store.commit('contragents/SET_CONTRAGENT', { physical_address: physicalAddress })
      },
      get () {
        return this.$store.state.contragents.detail.physical_address
      }
    }
  }
}
</script>
