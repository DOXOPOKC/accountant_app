<template lang="pug">
  v-col(cols="12")
    v-text-field(
      dense
      readonly
      v-model="dadata_name"
      label="Юридическое наименование"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    dadata_name: {
      set (dadataName) {
        this.$store.commit('contragents/SET_CONTRAGENT', { dadata_name: dadataName })
      },
      get () {
        return this.$store.state.contragents.detail.dadata_name
      }
    }
  }
}
// disabled
</script>
