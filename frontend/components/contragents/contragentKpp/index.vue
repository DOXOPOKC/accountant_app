<template lang="pug">
  v-col(cols="12")
    v-text-field(
      v-model="kpp"
      label="КПП"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    kpp: {
      set (kpp) {
        this.$store.commit('contragents/SET_CONTRAGENT', { kpp })
      },
      get () {
        return this.$store.state.contragents.detail.kpp
      }
    }
  }
}
</script>
