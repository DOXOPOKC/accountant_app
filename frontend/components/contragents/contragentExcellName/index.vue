<template lang="pug">
  v-col(cols="12")
    v-text-field(
      dense
      v-model="excellName"
      label="Наименование"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    excellName: {
      set (excellName) {
        this.$store.commit('contragents/SET_CONTRAGENT', { excell_name: excellName })
      },
      get () {
        return this.$store.state.contragents.detail.excell_name
      }
    }
  }
}
</script>
