<template lang="pug">
  v-col(cols="2")
    v-text-field(
      dense
      v-model.number="inn"
      label="ИНН"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    inn: {
      set (inn) {
        this.$store.commit('contragents/SET_CONTRAGENT', { inn })
      },
      get () {
        return this.$store.state.contragents.detail.inn
      }
    }
  }
}
</script>
