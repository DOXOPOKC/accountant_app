<template lang="pug">
  v-col(cols="12")
    v-text-field(
      dense
      v-model.number="personalNumber"
      label="Лицевой счет"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    personalNumber: {
      set (personalNumber) {
        this.$store.commit('contragents/SET_CONTRAGENT', { personal_number: personalNumber })
      },
      get () {
        return this.$store.state.contragents.detail.personal_number
      }
    }
  }
}
</script>
