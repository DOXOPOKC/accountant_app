<template lang="pug">
  v-col(cols="4")
    v-text-field(
      dense
      v-model="passportNumber"
      label="Номер паспорта"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    passportNumber: {
      set (passportNumber) {
        this.$store.commit('contragents/SET_CONTRAGENT', { passport_number: passportNumber })
      },
      get () {
        return this.$store.state.contragents.detail.passport_number
      }
    }
  }
}
</script>
