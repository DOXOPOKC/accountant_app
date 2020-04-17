<template lang="pug">
  v-col(cols="2")
    v-text-field(
      v-model="opf"
      label="ОПФ"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    opf: {
      set (opf) {
        this.$store.commit('contragents/SET_CONTRAGENT', { opf })
      },
      get () {
        return this.$store.state.contragents.detail.opf
      }
    }
  }
}
</script>
